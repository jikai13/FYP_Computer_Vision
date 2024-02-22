import cv2
import os


def extract_and_crop_frames(video_path, output_folder, num_frames, crop_coords):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    frames_per_minute = int(fps * 60)

    x, y, width, height = crop_coords  # Unpack cropping coordinates

    for minute in range(num_frames):  # From 0 to 39 minutes
        frame_number = minute * frames_per_minute
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:  # If the frame was read successfully
            # Crop the frame
            cropped_frame = frame[y:y + height, x:x + width]

            frame_path = os.path.join(output_folder, f"frame_{minute:02d}.png")
            cv2.imwrite(frame_path, cropped_frame)
        else:
            print(f"Could not read frame for minute {minute}")
            break  # Exit the loop if unable to read frame

    cap.release()
    print("Frame extraction and cropping complete.")








if __name__ == '__main__':
    # Example usage
    video_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7).mp4"
    output_folder = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7) Frames Precise"
    num_frames = 40
    crop_coords = (345, 210, 55, 190)  # Example coordinates (x, y, width, height)
    extract_and_crop_frames(video_path, output_folder, num_frames, crop_coords)
