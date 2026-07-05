from ultralytics import YOLO
import cv2

# Paths (only need to change these 3 lines)
video_path = r"C:\Users\ghane\Desktop\Detection_project\code\videos\3833441791-preview.mp4"
model_path = r"C:\Users\ghane\Desktop\Detection_project\runs\detect\train\weights\best.pt"
output_path = r"C:\Users\ghane\Desktop\Detection_project\code\videos\output_detected.mp4"

# Load model
print("Loading model...")
model = YOLO(model_path)

# Open video
cap = cv2.VideoCapture(video_path)

# Setup output
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

print("Processing... Press 'q' to stop")

frame_count = 0
cheating_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # Detect cheating
    results = model(frame, conf=0.5)[0]
    
    # Draw boxes
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])
        
        if class_id == 0:  # Cheating
            cheating_count += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, "CHEATING", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:  # Normal
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Show status on frame
    if cheating_count > 0:
        cv2.putText(frame, "CHEATING DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Save and show
    out.write(frame)
    cv2.imshow("Detection", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"\nDone! Processed {frame_count} frames")
print(f"Cheating detected in {cheating_count} frames")
print(f"Output saved to: {output_path}")