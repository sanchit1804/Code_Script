import numpy as np
import cv2 as cv


def get_camera(camera_source_idx : int) -> cv.VideoCapture:
    cap = cv.VideoCapture(camera_source_idx)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    return cap



def main():
    #TODO: List all cameras let him choose
    cap = get_camera(0)

    while True:
        res, frame = cap.read()

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