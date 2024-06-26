import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import csv
from itertools import zip_longest


def threshold_full_single(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold
    # Note: Adjust the threshold value (127 in this example) as necessary for your images
    _, thresh = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)

    # Calculate the area of the explant
    area = cv2.countNonZero(thresh)

    # Display the threshold image (for debugging purposes)
    # cv2.imshow('Threshold Image', thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Save the threshold image
    cv2.imwrite(output_path, thresh)

    return area


def frame_analysis_single(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Check if image is loaded properly
    if image is None:
        print("Error: Image not found.")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold
    # _, thresh = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)

    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Rounded: cv2.CHAIN_APPROX_SIMPLE

    if not contours:
        print("No contours found.")
        return None

    # Optionally, draw the contours on the original image for visualization
    # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)

    # Find the largest contour based on area
    largest_contour = max(contours, key=cv2.contourArea)

    # print(f"Contour: {largest_contour}")

    # Calculate the area of the largest contour
    largest_area = cv2.contourArea(largest_contour)

    # Optionally, draw the largest contour on the original image for visualization
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 1)

    # Calculate the centroid of the largest contour
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        # Draw a vertical centerline through the centroid of the largest contour
        height = image.shape[0]
        #cv2.line(image, (cx, 0), (cx, height), (255, 0, 0), 1)  # Drawn in blue with thickness 2

        # Find points on the contour close to the centroid's x-coordinate
        x_tolerance = 2  # Define a tolerance range
        aligned_points = [pt[0] for pt in largest_contour if abs(pt[0][0] - cx) <= x_tolerance]

        highest_point = min(aligned_points, key=lambda pt: pt[1])
        lowest_point = max(aligned_points, key=lambda pt: pt[1])

        #cv2.circle(image, highest_point, radius=2, color=(0, 0, 255), thickness=-1)
        #cv2.circle(image, lowest_point, radius=2, color=(0, 0, 255), thickness=-1)

        contour_height = lowest_point[1] - highest_point[1]


    # Initialize volume
    volume = 0
    pixel_area = 1  # Define the area of a pixel, adjust if you know the scale
    largest_width = 0
    smallest_width = float('inf')

    # Iterate over the height of the image
    for y in range(image.shape[0]):

        # print(f"y:{y}")

        radius = 0
        diameter = 0
        # Find the points on the contour that align with the current y-coordinate
        aligned_points = [pt[0] for pt in largest_contour if pt[0][1] == y]

        # Check if there are at least two points to define a radius
        if len(aligned_points) >= 2:
            # Find the x-coordinates of the points
            x_coords = [pt[0] for pt in aligned_points]

            # Calculate the radius as half the difference between the max and min x-coordinates
            radius = (max(x_coords) - min(x_coords)) / 2.0

            diameter = 2*radius

            if diameter > largest_width:
                largest_width = diameter
            if diameter < smallest_width:
                smallest_width = diameter

            # Draw a line on the original image at this y-coordinate
            # cv2.line(image, (0, y), (image.shape[1], y), (0, 255, 255), 1) # Yellow Line
        elif len(aligned_points) == 1:
            # Fallback to centroid-based radius calculation
            # Calculate distance from each point to the centroid's x-coordinate and use the maximum as the radius
            radius = abs(aligned_points[0][0] - cx)

            # Draw a line on the original image at this y-coordinate to show centroid-based radius calculation
            #cv2.line(image, (0, y), (image.shape[1], y), (255, 0, 0), 1)  # Red line

        volume += np.pi * (radius ** 2) * pixel_area

    # cv2.imshow('All Contours', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Save the contour image
    cv2.imwrite(output_path, image)



    return largest_area, highest_point, volume, contour_height, largest_width, smallest_width

def threshold_full(folder_path, output_folder_path):

    frame_listing = os.listdir(folder_path)

    for frame in frame_listing:

        frame_path = f'{folder_path}/{frame}'

        output_path = f'{output_folder_path}/{frame}'

        threshold_full_single(frame_path, output_path)

def frame_analysis(folder_path, output_folder_path):

    frame_listing = os.listdir(folder_path)

    area_listing = []

    highest_point_listing = []

    volume_listing = []

    height_listing = []

    largest_width_listing = []

    smallest_width_listing = []

    time_listing = list(range(0, len(frame_listing)))

    for frame in frame_listing:

        frame_path = f'{folder_path}/{frame}'

        output_path = f'{output_folder_path}/{frame}'

        area, highest_point, volume, height, largest_width, smallest_width = threshold_largest_single(frame_path, output_path)

        area_listing.append(area)

        highest_point_listing.append(highest_point)

        volume_listing.append(volume)

        height_listing.append(height)

        largest_width_listing.append(largest_width)

        smallest_width_listing.append(smallest_width)

    fig, ax = plt.subplots()

    ax.plot(time_listing, area_listing)

    ax.set(xlabel='Time (Minutes)', ylabel='Area (Pixels Squared)',
           title='Explant Area as a function of Time')

    ax.grid()

    fig.savefig(f'{output_folder_path}/Area Plot')

    highest_point_x, highest_point_y = zip(*highest_point_listing)

    fig1, ax1 = plt.subplots()

    ax1.plot(highest_point_x, highest_point_y)

    ax1.set(xlabel='x-Coordinate (Pixels)', ylabel='y-Coordinate (Pixels)',
           title='Trajectory of the Explant Superior Centroidal Intersection Point')

    ax1.grid()

    fig1.savefig(f'{output_folder_path}/Trajectory Plot')

    magnitudes = [math.sqrt(highest_point_x[i] ** 2 + highest_point_y[i] ** 2) for i in range(len(highest_point_x))]

    fig2, ax2 = plt.subplots()

    ax2.plot(time_listing, magnitudes)

    ax2.set(xlabel='Time (Minutes)', ylabel='Displacement (Pixels)',
            title='Explant Superior Centroidal Displacement as a function of time')

    ax2.grid()

    fig2.savefig(f'{output_folder_path}/Displacement Plot')

    fig3, ax3 = plt.subplots()

    ax3.plot(time_listing, highest_point_y)

    ax3.set(xlabel='Time (Minutes)', ylabel='y-Coordinate (Pixels)',
            title='Vertical Trajectory of the Explant Superior Centroidal Intersection Point')

    ax3.grid()

    fig3.savefig(f'{output_folder_path}/Vertical Trajectory Plot')

    velocities = [(highest_point_y[i] - highest_point_y[i - 1]) / 60 for i in range(1, len(highest_point_y))]

    fig4, ax4 = plt.subplots()

    ax4.plot(time_listing[:-1], velocities)

    ax4.set(xlabel='Time (Minutes)', ylabel='Vertical Velocity (Pixels/s)',
            title='Explant Superior Centroidal Vertical Velocity as a function of time')

    ax4.grid()

    fig4.savefig(f'{output_folder_path}/Vertical Velocity Plot')

    fig5, ax5 = plt.subplots()

    ax5.plot(time_listing, volume_listing)

    ax5.set(xlabel='Time (Minutes)', ylabel='Explant Volume (Pixels Cubed)',
            title='Explant Volume as a function of time')

    ax5.grid()

    fig5.savefig(f'{output_folder_path}/Explant Volume Plot')

    headings = ['Frames', 'Explant Height', 'Largest Width', 'Smallest Width', 'Explant Area', 'Explant Volume', 'Vertical Trajectory', 'Lateral Trajectory', 'Vertical Velocity']

    combined_data = zip_longest(time_listing, height_listing, largest_width_listing, smallest_width_listing, area_listing, volume_listing, highest_point_y, highest_point_x, velocities, fillvalue='')

    with open(f'{output_folder_path}/Explant_Data.csv', 'w', newline='') as file:

        writer = csv.writer(file)

        writer.writerow(headings)

        writer.writerows(combined_data)








def detect_edges(image_path, blur_kernel_size=(5, 5), threshold1=100, threshold2=200):
    """
    Detects edges in an image using the Canny edge detector.

    Parameters:
    - image_path: Path to the input image.
    - blur_kernel_size: Size of the kernel for the Gaussian blur. Default is (5, 5).
    - threshold1: Lower threshold for the hysteresis process. Default is 100.
    - threshold2: Upper threshold for the hysteresis process. Default is 200.
    """
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: Image not found.")
        return

    # Apply Gaussian blur for noise reduction
    blurred_image = cv2.GaussianBlur(image, blur_kernel_size, 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred_image, threshold1, threshold2)

    # Display the results
    cv2.imshow('Original Image', image)
    cv2.imshow('Edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def segment_explant_by_color(image_path, hsv_lower_bound, hsv_upper_bound):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return None

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the HSV range for the explant color
    lower_bound = np.array(hsv_lower_bound)  # e.g., np.array([20, 100, 100])
    upper_bound = np.array(hsv_upper_bound)  # e.g., np.array([30, 255, 255])

    # Create a binary mask where the explant colors are white
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Optional: Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

    # Apply the mask to get the segmented image
    segmented_image = cv2.bitwise_and(image, image, mask=mask_cleaned)

    # Display the original and segmented images
    cv2.imshow('Original Image', image)
    cv2.imshow('Segmented Image', segmented_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # To calculate the area, count the white pixels in the mask
    explant_area = np.sum(mask_cleaned == 255)
    print(f"Explant area: {explant_area} pixels")

    return explant_area


if __name__ == '__main__':
    image_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7) Frames\frame_00.png"
    # area = extract_explant_area_with_threshold(image_path)
    # print(f"Area of the explant: {area} pixels")
    # largest_area = extract_largest_explant_area_with_threshold(image_path)
    # print(f"Area of the largest contour: {largest_area} pixels")
    # detect_edges(image_path)
    # hsv_lower_bound = [0, 35, 105]  # Example lower HSV bound
    # hsv_upper_bound = [180, 85, 200]  # Example upper HSV bound
    # segment_explant_by_color(image_path, hsv_lower_bound, hsv_upper_bound)
    folder_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7) Frames Precise"
    output_folder_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7) Threshold Largest Precise Otsu No Round"
    frame_analysis(folder_path, output_folder_path)
    #threshold_largest_single(image_path, r"C:\Users\wujik\OneDrive - Imperial College London\FYP\17 5cm 50um resistor + explant 3 (1-7) Threshold Largest Precise")
    # Use Case 1
    # folder_path1 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Frames"
    # output_folder_path1 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Threshold"
    # threshold_largest(folder_path1, output_folder_path1)
    # Use Case 2
    # folder_path2 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Barrel Correct Frames"
    # output_folder_path2 = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Threshold Barrel"
    # threshold_largest(folder_path2, output_folder_path2)
    #threshold_largest(r"D:\FYP\test", r"D:\FYP")
