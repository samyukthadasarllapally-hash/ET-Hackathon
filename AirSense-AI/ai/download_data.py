import kagglehub
import shutil
import os

# Download dataset
path = kagglehub.dataset_download("rohanrao/air-quality-data-in-india")
print("Downloaded to:", path)

# Copy city_day.csv to data/ folder
src = os.path.join(path, "city_day.csv")
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "aqi_dataset.csv")

os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy(src, dst)
print(f"Copied to: {dst}")
