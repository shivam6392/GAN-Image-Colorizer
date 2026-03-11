import torch
import os
from model.siggraph17 import SIGGRAPHGenerator

def export_to_onnx():
    print("Loading PyTorch model...")
    # Initialize the model architecture
    model = SIGGRAPHGenerator()
    
    # Load the weights
    weights_path = os.path.join(os.path.dirname(__file__), "checkpoints", "siggraph17-df00044c.pth")
    if not os.path.exists(weights_path):
        print(f"Error: Weights not found at {weights_path}")
        return

    # Load state dict
    state_dict = torch.load(weights_path, map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)
    model.eval()

    # Create dummy input: L channel is [B, 1, 256, 256]
    dummy_input = torch.randn(1, 1, 256, 256) 
    
    # Export path
    export_path = os.path.join(os.path.dirname(__file__), "checkpoints", "siggraph17.onnx")
    
    print(f"Exporting to {export_path}...")
    torch.onnx.export(
        model, 
        dummy_input, # input_A
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
