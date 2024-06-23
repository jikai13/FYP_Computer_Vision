import cv2
import os


def extract_and_crop_frames(video_path, output_folder, num_frames, exact_frame, crop_coords):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    frames_per_minute = int(fps * 60)

    x, y, width, height = crop_coords  # Unpack cropping coordinates

    for minute in range(num_frames):  # From 0 to 39 minutes

        if exact_frame == True:
            frame_number = minute
        else:
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

def crop_frames(frames_path, output_folder, crop_coords):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    x, y, width, height = crop_coords  # Unpack cropping coordinates

    for filename in os.listdir(frames_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            input_path = os.path.join(frames_path, filename)
            output_path = os.path.join(output_folder, filename)

            # Read the image
            image = cv2.imread(input_path)

            if image is None:
                print(f"Failed to load image: {input_path}")
                continue

            # Crop the image
            cropped_image = image[y:y + height, x:x + width]

            # Save the cropped image
            cv2.imwrite(output_path, cropped_image)

            print(f"Cropped and saved: {output_path}")














if __name__ == '__main__':
    # Proof of Concept
    # video_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7).mp4"
    # output_folder = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7) Frames Precise"
    # num_frames = 40
    # exact_frame = False
    # crop_coords = (345, 210, 55, 190)  # Example coordinates (x, y, width, height)
    # extract_and_crop_frames(video_path, output_folder, num_frames, crop_coords)
    # Use Case 1
    # video_path1 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29.mp4"
    # output_folder1 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Frames Barrel"
    # num_frames1 = 15
    # exact_frame1 = True
    # crop_coords1 = (550, 630, 70, 115)  # Example coordinates (x, y, width, height)
    # extract_and_crop_frames(video_path1, output_folder1, num_frames1, exact_frame1, crop_coords1)
    # Use Case 2: Barrel Correction
    # frames_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Barrel Correct"
    # output_folder2 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Barrel Correct Frames"
    # crop_coords2 = (650, 600, 40 ,100)
    # crop_frames(frames_path, output_folder2, crop_coords2)
    frames_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\cam0_photos\2024-05-30_19-33-13.jpg"
    output_folder2 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Barrel Correct Frames"
    crop_coords2 = (200, 400, 40 ,100)
    crop_frames(frames_path, output_folder2, crop_coords2)

