
# import Rpi.GPIO as GPIO
import os
import cv2
import time
import asyncio

def control_loop(duration_sec):

    #folder_generation(2)
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

            take_photo(2)

            time.sleep(10)

    # GPIO.output('gpio_pin', GPIO.LOW)

    # finally:
    #
    #     GPIO.cleanup()

async def async_take_photo(cam_index):

    cap = cv2.VideoCapture(cam_index)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Sets frame width and height of the video capture
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Adjusts Auto exposure

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
        photo_filename = f"D:\FYP\cam{cam_index}_photos/{cam_index}_{timestamp}.tiff"
        cv2.imwrite(photo_filename, frame)
        print("Photo taken!")

    # Release the camera and close the window
    cap.release()

async def async_control_loop(duration, interval, cam_amount):

    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        for i in range(cam_amount):
            await async_take_photo(i)
            await asyncio.sleep(interval) # Delay


def folder_generation(cam_amount):

    for i in range(cam_amount):

        folder_path = f"D:\FYP\cam{i}_photos"
        os.mkdir(folder_path)
def take_photo(cam_index):
    # Open a connection to the webcam (you can specify the camera index, e.g., 0 for the default camera)
    cap = cv2.VideoCapture(cam_index)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Sets frame width and height of the video capture
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) # Adjusts Auto exposure

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
        photo_filename = f"D:\FYP\cam{cam_index}_photos/{cam_index}_{timestamp}.tiff"
        cv2.imwrite(photo_filename, frame)
        print("Photo taken!")

    # Release the camera and close the window
    cap.release()

def cam_index_testing():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera index {i} opened successfully.")
            break
    else:
        print("Error: Couldn't open any camera.")

def cam_index_testing_singular(cam_index):
    cap = cv2.VideoCapture(cam_index)
    if cap.isOpened():
        print(f"Camera index has opened successfully.")


    else:
        print("Error: Couldn't open any camera.")



def vid_testing(cam_index):

    vid = cv2.VideoCapture(cam_index)

    while (True):

        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

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
    #take_photo(1)
    #take_photo(2)
    #testing()
    #testing_specific(1)
    vid_testing(1)


