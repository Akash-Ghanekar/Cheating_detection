# laptop_webcam.py - Simple laptop camera cheating detection
from ultralytics import YOLO
import cv2
import os

# Find your trained model automatically
def find_model():
    """Find the trained model file"""
    search_dirs = [
        r"C:\Users\ghane\Desktop\Detection_project\code\runs\detect",
        r"C:\Users\ghane\Desktop\Detection_project\runs\detect",
    ]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for folder in os.listdir(search_dir):
                if folder.startswith('train'):
                    model_path = os.path.join(search_dir, folder, 'weights', 'best.pt')
                    if os.path.exists(model_path):
                        print(f"✅ Found model: {model_path}")
                        return model_path
    return None

# Get model path
model_path = find_model()

if model_path is None:
    print("❌ Model not found! Please train first.")
    print("Run: python main.py")
    exit()

# Load model
print("📁 Loading model...")
model = YOLO(model_path)

# Open laptop camera (ID 0 is always the built-in camera)
print("\n🎥 Opening laptop camera...")
cap = cv2.VideoCapture(0)  # 0 = built-in laptop camera

if not cap.isOpened():
    print("❌ Could not open laptop camera!")
    print("Make sure no other app is using the camera")
    exit()

print("✅ Camera ready!")
print("="*50)
print("🎯 LAPTOP CAMERA CHEATING DETECTION")
print("="*50)
print("Controls:")
print("  • 'q' - Quit")
print("  • 's' - Save screenshot")
print("="*50)

while True:
    # Read frame from laptop camera
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to get frame")
        break
    
    # Flip horizontally (so it acts like a mirror)
    frame = cv2.flip(frame, 1)
    
    # Run cheating detection
    results = model(frame, conf=0.5)[0]
    
    # Draw detections on frame
    annotated_frame = results.plot()
    
    # Add status text
    cv2.putText(annotated_frame, "CHEATING DETECTION SYSTEM", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Show the camera feed with detections
    cv2.imshow("Laptop Camera - Cheating Detection", annotated_frame)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        print("\n👋 Quitting...")
        break
    elif key == ord('s'):
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f"cheating_capture_{timestamp}.jpg", annotated_frame)
        print(f"📸 Screenshot saved!")

# Clean up
cap.release()
cv2.destroyAllWindows()
print("✅ Laptop camera closed!")