from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

# Path to your config
config_path = r"C:\Users\ghane\Desktop\Detection_project\code\data\config.yaml"

# Train with beginner-friendly settings
results = model.train(
    data=config_path,
    epochs=50,      # Increased from 30 (better learning)
    batch=8,        # Smaller batch = more stable
    imgsz=640,      # Standard image size
    device='cpu',   # Use CPU (avoid GPU issues)
    verbose=True    # Show progress
)

print("✅ Training complete!")