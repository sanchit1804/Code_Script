import cv2 as cv
import sys

def get_camera(camera_source_idx : int) -> cv.VideoCapture:
    cap = cv.VideoCapture(camera_source_idx)

    if not cap.isOpened():
        print("Cannot open camera")
        sys.exit()

    return cap

def process_frame(frame):
    detect_faces(frame)
    return frame

TEXT_MARGIN = 5
last_face = (0, 0)
last_face_w, last_face_h = (100, 100)

def smooth(last_pos, cur_pos, alpha=0.2, threshold=2):
    dx = cur_pos[0] - last_pos[0]
    dy = cur_pos[1] - last_pos[1]

    if abs(dx) < threshold:
        cur_pos = (last_pos[0], cur_pos[1])
    if abs(dy) < threshold:
        cur_pos = (cur_pos[0], last_pos[1])

    x = int(alpha * cur_pos[0] + (1 - alpha) * last_pos[0])
    y = int(alpha * cur_pos[1] + (1 - alpha) * last_pos[1])
    return x, y


def detect_faces(frame):
    global last_face
    global last_face_w, last_face_h
    frame_gray = cv.cvtColor(src=frame, code=cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image=frame_gray, scaleFactor=1.2, minNeighbors=7)

    for (x, y, w, h) in faces:
        x, y = smooth(last_face, (x,y))
        w, h = smooth((last_face_w, last_face_h), (w, h))
        frame = cv.rectangle(
            img=frame,
            pt1=(x, y), pt2=(x + w, y + h),
            color=(255, 0, 0), thickness=2)
        add_text(frame, "Face", (x + w + TEXT_MARGIN, y - TEXT_MARGIN), h / 200)
        last_face = (x, y)
        last_face_w, last_face_h = w, h

def add_text(frame, text, point, font_scale = 1, font_face = cv.FONT_HERSHEY_DUPLEX, color = (255, 0, 0), thickness = 1):
    cv.putText(frame, text, point, font_face, font_scale, color, thickness)
    return frame

# TODO: List all cameras let him choose
def main():
    global face_cascade

    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = get_camera(0)

    # Main loop
    while True:
        res, frame = cap.read()
        frame = process_frame(frame)

        if not res:
            print("Cannot read frame")
            break

        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()