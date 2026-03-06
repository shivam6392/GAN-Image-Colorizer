import os
import requests

# We will ship the static .onnx graph directly in the Git Repository and bypass HTTP downloads.
save_path = os.path.join(os.path.dirname(__file__), "checkpoints", "siggraph17.onnx")

def download_model():
    if os.path.exists(save_path):
        print(f"ONNX Model already exists locally at {save_path}")
        return
    else:
        print(f"Error: ONNX Model missing at {save_path}")

if __name__ == "__main__":
    download_model()
