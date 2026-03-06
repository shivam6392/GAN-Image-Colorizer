import os
import io
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
import onnxruntime as ort

class Colorizer:
    def __init__(self, model_path="checkpoints/siggraph17.onnx"):
        if model_path and os.path.exists(model_path):
            print(f"Loading ONNX model from {model_path}")
            # Ensure ONNX Runtime runs sequentially on 1 thread to avoid Render Memory Spikes
            sess_options = ort.SessionOptions()
            sess_options.intra_op_num_threads = 1
            sess_options.inter_op_num_threads = 1
            self.session = ort.InferenceSession(model_path, sess_options, providers=['CPUExecutionProvider'])
            self.input_name = self.session.get_inputs()[0].name
        else:
            print(f"Warning: ONNX model {model_path} not found. Cannot colorize.")
            self.session = None

    def preprocess(self, img_bytes):
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        original_size = img.size
        
        # 1. Processing for Model Input (256x256)
        # Replacing torchvision transforms.Resize with PIL Resize
        img_256 = img.resize((256, 256), Image.BICUBIC)
        img_256_arr = np.array(img_256)
        
        # rgb2lab returns L in [0, 100] exactly as the model expects
        img_256_lab = rgb2lab(img_256_arr).astype(np.float32)
        
        # Extract L channel and transpose to [C, H, W] for the model
        L_256 = img_256_lab[:, :, 0] # H, W
        L_256 = L_256[np.newaxis, np.newaxis, :, :] # 1, 1, 256, 256
        
        # 2. Processing for High-Res Output (Original L Channel)
        img_arr = np.array(img)
        img_lab = rgb2lab(img_arr).astype(np.float32)
        L_original = img_lab[..., 0] # Keep as HxW numpy array
        
        return L_256, L_original, original_size

    def predict(self, img_bytes):
        if self.session is None:
            # Fallback if model missing, return original dummy image
            return Image.open(io.BytesIO(img_bytes)).convert("RGB")

        L_256, L_original, original_size = self.preprocess(img_bytes)
        
        # Run inference using ONNX Runtime
        ort_inputs = {self.input_name: L_256}
        ort_outs = self.session.run(None, ort_inputs)
        
        ab_256 = ort_outs[0] # output shape: [1, 2, 256, 256]
        
        # Resize predicted ab back to original size manually without PyTorch Functional
        # Transpose back to HWC for PIL to resize
        ab_256_hwc = ab_256[0].transpose(1, 2, 0) # 256, 256, 2
        
        # Separately resize `a` and `b` channels
        a_channel = Image.fromarray(ab_256_hwc[:, :, 0]).resize((original_size[0], original_size[1]), Image.BILINEAR)
        b_channel = Image.fromarray(ab_256_hwc[:, :, 1]).resize((original_size[0], original_size[1]), Image.BILINEAR)
        
        a_upscaled = np.array(a_channel)
        b_upscaled = np.array(b_channel)
        
        ab_upscaled = np.stack([a_upscaled, b_upscaled], axis=-1) # H, W, 2
        
        # Combine L_original (H, W) + ab_upscaled (H, W, 2)
        L_original_exp = L_original[..., np.newaxis] # H, W, 1
        Lab_final = np.concatenate([L_original_exp, ab_upscaled], axis=2)
        
        # Convert to RGB
        rgb_image = lab2rgb(Lab_final)
        
        # Convert to PIL and return
        img_final = Image.fromarray((rgb_image * 255).astype(np.uint8))
        return img_final
