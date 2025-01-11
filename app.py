from flask import Flask, render_template, Response, jsonify
import cv2
from exercise_analyzer import ExerciseAnalyzer

app = Flask(__name__)

# Initialize video capture and exercise analyzer
video_capture = cv2.VideoCapture(0)  # Open default camera
analyzer = ExerciseAnalyzer()

@app.route("/")
def index():
    return render_template("index.html")

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Analyze frame for exercise
        frame, exercise_data = analyzer.process_frame(frame)

        # Encode frame for live streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame in byte format for video streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/data")
def get_data():
    return jsonify(analyzer.get_exercise_data())

if __name__ == "__main__":
    app.run(debug=True)
