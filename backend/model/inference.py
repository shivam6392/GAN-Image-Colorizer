import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from skimage.color import rgb2lab, lab2rgb
from .siggraph17 import SIGGRAPHGenerator
import os
import io

class Colorizer:
    def __init__(self, model_path="checkpoints/siggraph17-df00044c.pth", map_location='cpu'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net_G = SIGGRAPHGenerator().to(self.device)
        
        if model_path and os.path.exists(model_path):
            self.net_G.load_state_dict(torch.load(model_path, map_location=map_location))
            print(f"Loaded Siggraph17 model from {model_path}")
        else:
            print(f"Warning: Model path {model_path} not found. Running with random weights.")
        
        self.net_G.eval()

    def preprocess(self, img_bytes):
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        original_size = img.size
        
        # 1. Processing for Model Input (256x256)
        transform_model = transforms.Compose([
            transforms.Resize((256, 256), Image.BICUBIC),
        ])
        img_256 = transform_model(img)
        img_256_arr = np.array(img_256)
        img_256_lab = rgb2lab(img_256_arr).astype("float32")
        img_256_lab_t = transforms.ToTensor()(img_256_lab)
        
        # Siggraph17 expects L channel in range [0, 100]
        # ToTensor scales [0, 255] to [0, 1]. But rgb2lab output is [0, 100] for L?
        # No, skimage.color.rgb2lab returns L in [0, 100], a, b in [-128, 127] approx.
        # transforms.ToTensor() converts HWC [0, 255] uint8 to CHW [0.0, 1.0] float.
        # BUT if input is float array, ToTensor doesn't scale if it's already float?
        # Wait, if I pass float array to ToTensor, it might not scale unless it's uint8.
        # Let's verify. standard ToTensor scales only if valid image types.
        # If I convert numpy float32 to tensor:
        L_256 = torch.from_numpy(img_256_lab[:, :, [0]].transpose(2, 0, 1)) # 1, H, W
        
        # 2. Processing for High-Res Output (Original L Channel)
        img_arr = np.array(img)
        img_lab = rgb2lab(img_arr).astype("float32")
        L_original = img_lab[..., 0] # Keep as HxW numpy array
        
        return L_256.unsqueeze(0).to(self.device), L_original, original_size

    def predict(self, img_bytes):
        L_256, L_original, original_size = self.preprocess(img_bytes)
        
        with torch.no_grad():
            # Model expects L in range [0, 100]
            ab_256 = self.net_G(L_256)
            
        # Post-process ab channel
        ab_256 = ab_256.cpu() # 1, 2, 256, 256
        
        # Resize predicted ab to original size
        ab_upscaled = torch.nn.functional.interpolate(
            ab_256, size=(original_size[1], original_size[0]), mode='bilinear', align_corners=False
        )
        
        # Denormalize ab - Model already does unnormalization!
        ab_upscaled = ab_upscaled.squeeze(0).numpy().transpose(1, 2, 0) # HxWx2

        
        # Combine L_original (H, W) + ab_upscaled (H, W, 2)
        L_original_exp = L_original[..., np.newaxis] # H, W, 1
        Lab_final = np.concatenate([L_original_exp, ab_upscaled], axis=2)
        
        # Convert to RGB
        rgb_image = lab2rgb(Lab_final)
        
        # Convert to PIL
        img_final = Image.fromarray((rgb_image * 255).astype(np.uint8))
        return img_final

    # lab_to_rgb is no longer needed in this new flow but keeping it won't hurt, 
    # though we replaced the logic inside predict.
