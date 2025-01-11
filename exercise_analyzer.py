import cv2
import mediapipe as mp
import numpy as np
from filterpy.kalman import KalmanFilter

class ExerciseAnalyzer:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.exercise_data = {
            "pushups": 0,
            "leg_raises": 0,
            "pull_ups": 0,
            "pull_downs": 0,
        }
        self.states = {
            "pushup": None,
            "leg_raise": None,
            "pull_up": None,
            "pull_down": None,
        }
        self.kalman_filters = {}

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
            )
            landmarks = results.pose_landmarks.landmark
            self._smooth_landmarks(landmarks)
            self._analyze_pushups(landmarks)
            self._analyze_leg_raises(landmarks)
            self._analyze_pull_ups(landmarks)
            self._analyze_pull_downs(landmarks)

        return frame, self.exercise_data

    def _smooth_landmarks(self, landmarks):
        """ Apply Kalman Filter to smooth landmark positions. """
        for idx, landmark in enumerate(landmarks):
            if idx not in self.kalman_filters:
                self.kalman_filters[idx] = self._create_kalman_filter()
            kf = self.kalman_filters[idx]
            kf.predict()
            kf.update(np.array([landmark.x, landmark.y]))
            landmark.x, landmark.y = kf.x[0], kf.x[1]

    def _create_kalman_filter(self):
        """ Create a Kalman Filter for 2D position tracking. """
        kf = KalmanFilter(dim_x=4, dim_z=2)
        kf.F = np.array([[1, 0, 1, 0],
                         [0, 1, 0, 1],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        kf.H = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0]])
        kf.P *= 1000
        kf.R = np.array([[5, 0],
                         [0, 5]])
        kf.Q = np.eye(4) * 0.1
        return kf

    def _analyze_pushups(self, landmarks):
        """ Analyze elbow and shoulder angle for pushups. """
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]

        angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)

        if angle > 160:  # Arms straight
            if self.states["pushup"] == "down":
                self.exercise_data["pushups"] += 1
            self.states["pushup"] = "up"
        elif angle < 90:  # Arms bent
            self.states["pushup"] = "down"

    def _analyze_leg_raises(self, landmarks):
        """ Analyze hip and knee angle for leg raises. """
        left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
        left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]

        angle = self._calculate_angle(left_hip, left_knee, left_ankle)

        if angle > 150:  # Legs straight
            if self.states["leg_raise"] == "down":
                self.exercise_data["leg_raises"] += 1
            self.states["leg_raise"] = "up"
        elif angle < 90:  # Legs bent
            self.states["leg_raise"] = "down"

    def _analyze_pull_ups(self, landmarks):
        """ Analyze hand position for pull-ups. """
        left_hand = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]

        if left_hand.y < left_shoulder.y - 0.1:  # Hand above shoulder
            if self.states["pull_up"] == "down":
                self.exercise_data["pull_ups"] += 1
            self.states["pull_up"] = "up"
        elif left_hand.y > left_shoulder.y + 0.1:  # Hand below shoulder
            self.states["pull_up"] = "down"

    def _analyze_pull_downs(self, landmarks):
        """ Analyze hand distance from shoulder for pull-downs. """
        left_hand = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]

        distance = np.abs(left_hand.y - left_shoulder.y)

        if distance > 0.2:  # Hands away from shoulders
            if self.states["pull_down"] == "up":
                self.exercise_data["pull_downs"] += 1
            self.states["pull_down"] = "down"
        elif distance < 0.1:  # Hands near shoulders
            self.states["pull_down"] = "up"

    def _calculate_angle(self, point1, point2, point3):
        """ Calculate the angle between three points using vector mathematics. """
        a = np.array([point1.x, point1.y])
        b = np.array([point2.x, point2.y])
        c = np.array([point3.x, point3.y])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle) * 180 / np.pi
        return angle

    def get_exercise_data(self):
        return self.exercise_data