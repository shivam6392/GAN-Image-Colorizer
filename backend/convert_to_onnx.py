import torch
from model.inference import Colorizer
import os

def export_to_onnx():
    print("Loading model...")
    # Load PyTorch model
    colorizer = Colorizer()
    model = colorizer.net_G
    model.eval()

    # Create dummy input: L channel is [1, 1, 256, 256]
    dummy_input = torch.randn(1, 1, 256, 256)
    
    # Export path
    export_path = os.path.join(os.path.dirname(__file__), "checkpoints", "siggraph17.onnx")
    
    print(f"Exporting to {export_path}...")
    torch.onnx.export(
        model, 
        dummy_input, 
        export_path, 
        export_params=True,
        opset_version=11, 
        do_constant_folding=True,
        input_names=['input_L'], 
        output_names=['output_ab'],
        dynamic_axes={'input_L': {0: 'batch_size'}, 'output_ab': {0: 'batch_size'}}
    )
    print("ONNX export complete!")

if __name__ == "__main__":
    export_to_onnx()
