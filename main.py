
# import Rpi.GPIO as GPIO
import os
import cv2
import time

def control_loop(duration_sec):

    folder_generation(2)
    start_time = time.time()
    end_time = start_time + duration_sec

    # try:

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup('gpio_pin', GPIO.OUT)

    while time.time() < end_time:

    # GPIO.output('gpio_pin', GPIO.HIGH)
    
    # time.sleep('setup')

            take_photo(0)

            take_photo(1)

            time.sleep(10)

    # GPIO.output('gpio_pin', GPIO.LOW)

    # finally:
    #
    #     GPIO.cleanup()

def folder_generation(cam_amount):

    for i in range(cam_amount):

        folder_path = f"D:\FYP\cam{i}_photos"
        os.mkdir(folder_path)
def take_photo(cam_index):
    # Open a connection to the webcam (you can specify the camera index, e.g., 0 for the default camera)
    cap = cv2.VideoCapture(cam_index)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't read a frame from the camera.")
        exit()
    else:
        current_time = time.time()
        current_time_struct = time.localtime(current_time)
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", current_time_struct)
        photo_filename = f"D:\FYP\cam{cam_index}_photos/{cam_index}_{timestamp}.jpg"
        cv2.imwrite(photo_filename, frame)
        print("Photo taken!")

    # Release the camera and close the window
    cap.release()

def testing():
    for i in range(10):  # Try indices from 0 to 9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera index {i} opened successfully.")
            break
    else:
        print("Error: Couldn't open any camera.")

def vid_testing(cam_index):
    # define a video capture object
    vid = cv2.VideoCapture(cam_index)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #control_loop(30)
    #folder_generation(3)
    #take_photo(0)
    take_photo(1)
    #take_photo(2)
    #testing()
    #vid_testing(1)


