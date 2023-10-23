import cv2
import imutils
import winsound

# Initialize global variables
alarm = False
alarm_mode = False
alarm_counter = 0


def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("[+] ALARM")
        winsound.Beep(1000, 1000)
    alarm = False


def main():
    try:
        vid = cv2.VideoCapture(0)  # Use camera index 0 for the default camera
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        print("[+] CAMERA CONFIGURED")

        ret, start_frame = vid.read()
        start_frame = imutils.resize(start_frame, width=500)
        start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
        start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

        global alarm_counter  # Declare alarm_counter as global

        while True:
            _, frame = vid.read()
            frame = imutils.resize(frame, width=500)

            if alarm_mode:
                frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
                difference = cv2.absdiff(frame_bw, start_frame)
                threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
                start_frame = frame_bw

                if threshold.sum() > 300:
                    alarm_counter += 1
                else:
                    # if means there was motion but now stopped 
                    if alarm_counter > 0:
                        alarm_counter -= 1

                cv2.imshow("[+] Cam", threshold)

                if alarm_counter >= 10:  # Set a threshold for the alarm to go off
                    if not alarm:
                        alarm = True
                        beep_alarm()
            else:
                cv2.imshow("[+] Cam", frame)

            key = cv2.waitKey(1)
            if key == 27:  # Press 'Esc' key to exit the program
                break
            elif key == ord("a"):  # Press 'A' key to toggle alarm mode
                alarm_mode = not alarm_mode
                print(f"Alarm mode is {'on' if alarm_mode else 'off'}")
            elif key == ord("s"):  # Press 'S' key to stop the alarm
                alarm = False

    except KeyboardInterrupt:
        print("[+] OPERATION CANCELLED ❌")
    except Exception as ex:
        print("[+] SOMETHING WENT WRONG ❌")
        print(str(ex))

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
