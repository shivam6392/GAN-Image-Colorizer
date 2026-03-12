import os
import requests

onnx_url = "https://github.com/shivam6392/GAN-Image-Colorizer/releases/download/new_release/siggraph17.onnx"

base_dir = os.path.dirname(__file__)
onnx_path = os.path.join(base_dir, "checkpoints", "siggraph17.onnx")

def download_file(url, save_path):
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1024*1024: # Must be > 1MB to be valid
        print(f"Skipping download. Valid model file exists at {save_path}")
        return True
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    print(f"Downloading model from: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, stream=True, timeout=30, headers=headers)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            print(f"Download complete: {save_path} ({os.path.getsize(save_path) / 1024 / 1024:.2f} MB)")
            return True
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error during download: {e}")
        return False

def download_model():
    return download_file(onnx_url, onnx_path)

if __name__ == "__main__":
    download_model()
