from flask import Flask, Response, render_template, jsonify
import cv2
from ultralytics import YOLO
import time
from datetime import datetime

app = Flask(__name__)

# Load your trained model
model = YOLO(r"C:\Users\ghane\Desktop\Detection_project\runs\detect\train\weights\best.pt")

# Global variables
cheating_status = False
alert_count = 0
alerts = []
last_alert_time = 0

def generate_frames():
    """Generate video frames for streaming"""
    global cheating_status, alert_count, alerts, last_alert_time
    
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Flip frame (mirror effect)
        frame = cv2.flip(frame, 1)
        
        # Run detection
        results = model(frame, conf=0.5)[0]
        
        cheating_detected = False
        
        # Draw bounding boxes
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            
            if class_id == 0:  # Cheating
                cheating_detected = True
                color = (0, 0, 255)  # Red
                label = f"CHEATING! {confidence:.2f}"
            else:  # Normal
                color = (0, 255, 0)  # Green
                label = f"Normal {confidence:.2f}"
            
            # Draw box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Update status and alerts
        if cheating_detected:
            cheating_status = True
            current_time = time.time()
            if current_time - last_alert_time > 2:  # Alert every 2 seconds max
                alert_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                alerts.insert(0, f"⚠️ {timestamp} - CHEATING DETECTED!")
                if len(alerts) > 10:
                    alerts.pop()
                last_alert_time = current_time
        else:
            cheating_status = False
        
        # Add status bar at top
        if cheating_detected:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 60), (0, 0, 255), -1)
            cv2.putText(frame, "⚠️ CHEATING DETECTED!", (50, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 60), (0, 255, 0), -1)
            cv2.putText(frame, "STATUS: NORMAL", (50, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Yield frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream video feed"""
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_status')
def get_status():
    """Return current status as JSON"""
    return jsonify({
        'cheating': cheating_status,
        'alert_count': alert_count,
        'alerts': alerts
    })

if __name__ == '__main__':
    print("="*50)
    print("🚀 Starting Cheating Detection System")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)