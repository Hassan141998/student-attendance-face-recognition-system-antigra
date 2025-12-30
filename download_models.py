import os
import requests

MODELS_URL = "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights"
TARGET_DIR = os.path.join("static", "models")

files = [
    "face_landmark_68_model-shard1",
    "face_landmark_68_model-weights_manifest.json",
    "face_recognition_model-shard1",
    "face_recognition_model-shard2",
    "face_recognition_model-weights_manifest.json",
    "ssd_mobilenetv1_model-shard1",
    "ssd_mobilenetv1_model-shard2",
    "ssd_mobilenetv1_model-weights_manifest.json",
    "tiny_face_detector_model-shard1",
    "tiny_face_detector_model-weights_manifest.json"
]

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

print(f"Downloading models to {TARGET_DIR}...")

for file_name in files:
    url = f"{MODELS_URL}/{file_name}"
    target_path = os.path.join(TARGET_DIR, file_name)
    
    if os.path.exists(target_path):
        print(f"Skipping {file_name} (already exists)")
        continue
        
    print(f"Downloading {file_name}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(target_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {file_name}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

print("Download complete.")
