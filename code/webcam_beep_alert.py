from ultralytics import YOLO
import cv2
from datetime import datetime

# Load model
model = YOLO(r"C:\Users\ghane\Desktop\Detection_project\runs\detect\train\weights\best.pt")

# Open camera
cap = cv2.VideoCapture(0)

print("="*40)
print("🎥 Cheating Detection")
print("Press 'q' to quit")
print("Press 's' to save screenshot")
print("="*40)

while True:
    # Read frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    # Detect
    results = model(frame)[0]
    
    # Check for cheating
    cheating = False
    for box in results.boxes:
        if int(box.cls[0]) == 0:  # Cheating detected
            cheating = True
            # Draw red box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, "CHEATING!", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Show BIG visual alert if cheating detected
    if cheating:
        # Red background at top
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 255), -1)
        cv2.putText(frame, "⚠️ ALERT: CHEATING DETECTED! ⚠️", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        # Also print in terminal
        print("⚠️ CHEATING DETECTED! ⚠️")
    else:
        # Green background at top
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 255, 0), -1)
        cv2.putText(frame, "STATUS: NORMAL", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Show instructions
    cv2.putText(frame, "Press 'q'=Quit  |  Press 's'=Save Screenshot", (10, frame.shape[0]-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Show frame
    cv2.imshow("Cheating Detection", frame)
    
    # Handle keys
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
    elif key == ord('s'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Screenshot saved: {filename}")

# Clean up
cap.release()
cv2.destroyAllWindows()
print("✅ Program closed")