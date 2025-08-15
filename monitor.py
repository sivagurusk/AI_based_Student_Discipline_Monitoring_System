import cv2
import mediapipe as mp
import mysql.connector
from datetime import datetime

# --- MySQL Config ---
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Sivask@21sk",
    "database": "student_monitoring"
}

def log_to_mysql(shirt_status, shoe_status, hair_status):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO dress_code_logs (shirt_status, shoe_status, hair_status)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (shirt_status, shoe_status, hair_status))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ MySQL Error:", e)

# --- MediaPipe Setup ---
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# --- Monitoring Logic ---
def evaluate_appearance(results):
    shirt_status = "Unknown"
    shoe_status = "Unknown"
    hair_status = "Unknown"

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark

        # Simulated logic
        shoulder = lm[mp_holistic.PoseLandmark.LEFT_SHOULDER.value]
        hip = lm[mp_holistic.PoseLandmark.LEFT_HIP.value]
        if hip.y - shoulder.y > 0.3:
            shirt_status = "Untucked"
        else:
            shirt_status = "Tucked-in"

        left_foot = lm[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_foot = lm[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX.value]
        shoe_status = "Wearing Shoes" if left_foot.visibility > 0.5 and right_foot.visibility > 0.5 else "No Shoes"

        head = lm[mp_holistic.PoseLandmark.NOSE.value]
        hair_status = "Proper" if head.visibility > 0.5 else "Improper"

    return shirt_status, shoe_status, hair_status

# --- Main App ---
def main():
    cap = cv2.VideoCapture(0)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(rgb)

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

            shirt_status, shoe_status, hair_status = evaluate_appearance(results)

            # Display on screen
            cv2.putText(frame, f"Shirt: {shirt_status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, f"Shoes: {shoe_status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, f"Hair: {hair_status}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            # Save to database (once every few seconds to avoid spam)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                log_to_mysql(shirt_status, shoe_status, hair_status)
                print("✅ Data logged to MySQL")

            cv2.imshow("Student Monitoring System", frame)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
