import os
import requests

onnx_url = "https://github.com/shivam6392/GAN-Image-Colorizer/releases/download/v1.0.0/siggraph17.onnx"
onnx_data_url = "https://github.com/shivam6392/GAN-Image-Colorizer/releases/download/v1.0.0/siggraph17.onnx.data"

base_dir = os.path.dirname(__file__)
onnx_path = os.path.join(base_dir, "checkpoints", "siggraph17.onnx")
onnx_data_path = os.path.join(base_dir, "checkpoints", "siggraph17.onnx.data")

def download_file(url, save_path):
    if os.path.exists(save_path):
        print(f"Skipping download. File exists at {save_path}")
        return True
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    print(f"Downloading from {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        print(f"Download complete: {save_path}")
        return True
    else:
        print(f"Failed to download. Status code: {response.status_code}")
        return False

def download_model():
    success_1 = download_file(onnx_url, onnx_path)
    success_2 = download_file(onnx_data_url, onnx_data_path)
    if not (success_1 and success_2):
        print("Warning: One or more ONNX model files could not be downloaded!")

if __name__ == "__main__":
    download_model()
