import os
import requests

url = "https://colorizers.onrender.com/colorizers/siggraph17-df00044c.pth"
save_path = os.path.join(os.path.dirname(__file__), "checkpoints", "siggraph17-df00044c.pth")

def download_model():
    if os.path.exists(save_path):
        print(f"Model already exists at {save_path}")
        return

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    print(f"Downloading model from {url}...")
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("Download complete!")
    else:
        print(f"Failed to download model. Status code: {response.status_code}")

if __name__ == "__main__":
    download_model()
