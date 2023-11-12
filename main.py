
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
    #
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
        photo_filename = f"D:\FYP\cam{cam_index}_photos/{timestamp}.jpg"
        cv2.imwrite(photo_filename, frame)
        print("Photo taken!")

    # Release the camera and close the window
    cap.release()

if __name__ == '__main__':
    control_loop(30)
    #take_photo(0)


