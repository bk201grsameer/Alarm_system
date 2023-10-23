import threading
import cv2
import imutils
import winsound

alarm = False
alarm_mode = False
alarm_counter = 0


def beep_alarm():
    # HANDLE ALARM
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("[+] ALARM")
        # winsound.Beep(1000, 1000)
    alarm = False


def main():
    global alarm_counter
    global alarm_mode
    global alarm
    try:
        vid = cv2.VideoCapture(1)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        print("[+] CAMERA CONFIGURED")
        # newfram-prev if diff is high alert alarm system
        ret, start_frame = vid.read()
        start_frame = imutils.resize(start_frame, width=500)
        start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
        # smoothen frame
        start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

        while True:
            _, frame = vid.read()
            frame = imutils.resize(frame, width=500)
            if alarm_mode:
                frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_bw = cv2.GaussianBlur(start_frame, (5, 5), 0)
                difference = cv2.absdiff(frame_bw, start_frame)
                threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
                # update the start_frame
                start_frame = frame_bw
                if threshold.sum() > 300:
                    alarm_counter += 1
                else:
                    if alarm_counter > 0:
                        alarm_counter -= 1
                # black and white image
                cv2.imshow("[+] Cam", threshold)
                if alarm_counter >= 10:
                    if not alarm:
                        alarm = True
                        beep_alarm()

            else:
                cv2.imshow("[+] Cam", frame)
            key = cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == 27:  # Press ESC TO EXIT
                break
            if key == ord("t"):  # t toggle
                alarm_mode = not alarm_mode
                print(f"[+] Alarm mode is : {'on' if alarm_mode else 'off'}")
            elif key == ord("s"):
                alarm = False

    except KeyboardInterrupt:
        print("[+] OPERATION CANCELLED ❌")
    except Exception as ex:
        print("[+] SOMETHING WENT WRONG ❌")
        print(str(ex))


main()
