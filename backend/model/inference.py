import os
import io
import numpy as np
from PIL import Image
import onnxruntime as ort

def rgb2lab(rgb):
    # rgb input is [0, 255] float
    rgb = rgb / 255.0
    # sRGB -> XYZ
    mask = rgb > 0.04045
    rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb[~mask] = rgb[~mask] / 12.92
    
    xyz_matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])
    xyz = np.dot(rgb, xyz_matrix.T)
    
    # XYZ -> Lab (D65)
    xyz[:, :, 0] /= 0.95047
    xyz[:, :, 1] /= 1.00000
    xyz[:, :, 2] /= 1.08883
    
    mask = xyz > 0.008856
    xyz[mask] = xyz[mask] ** (1/3)
    xyz[~mask] = (7.787 * xyz[~mask]) + (16/116)
    
    L = (116 * xyz[:, :, 1]) - 16
    a = 500 * (xyz[:, :, 0] - xyz[:, :, 1])
    b = 200 * (xyz[:, :, 1] - xyz[:, :, 2])
    
    return np.stack([L, a, b], axis=2)

def lab2rgb(lab):
    # Lab -> XYZ
    y = (lab[:, :, 0] + 16) / 116
    x = lab[:, :, 1] / 500 + y
    z = y - lab[:, :, 2] / 200
    
    xyz = np.stack([x, y, z], axis=2)
    mask = xyz > 0.206893 # (6/29)
    xyz[mask] = xyz[mask] ** 3
    xyz[~mask] = (xyz[~mask] - 16/116) / 7.787
    
    xyz[:, :, 0] *= 0.95047
    xyz[:, :, 1] *= 1.00000
    xyz[:, :, 2] *= 1.08883
    
    # XYZ -> sRGB
    rgb_matrix = np.array([
        [ 3.2404542, -1.5371385, -0.4985314],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0556434, -0.2040259,  1.0572252]
    ])
    rgb = np.dot(xyz, rgb_matrix.T)
    
    mask = rgb > 0.0031308
    rgb[mask] = 1.055 * (rgb[mask] ** (1/2.4)) - 0.055
    rgb[~mask] = 12.92 * rgb[~mask]
    
    return np.clip(rgb, 0, 1)

class Colorizer:
    def __init__(self, model_path="checkpoints/siggraph17.onnx"):
        if model_path and os.path.exists(model_path):
            print(f"Loading ONNX model from {model_path}")
            # Ensure ONNX Runtime runs sequentially on 1 thread to avoid Render Memory Spikes
            sess_options = ort.SessionOptions()
            sess_options.intra_op_num_threads = 1
            sess_options.inter_op_num_threads = 1
            
            # Aggressive memory optimization for Render 512MB limit
            sess_options.enable_mem_pattern = False
            sess_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            
            self.session = ort.InferenceSession(model_path, sess_options, providers=['CPUExecutionProvider'])
            self.input_name = self.session.get_inputs()[0].name
            
            # Explicitly clear memory after loading model
            import gc
            gc.collect()
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
