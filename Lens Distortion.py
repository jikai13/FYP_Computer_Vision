import cv2
import numpy as np

# Load the image
image_path = r"C:\Users\wujik\OneDrive - Imperial College London\FYP\TimeLapse 03_25_2024_10_18_29 Barrel\frame_00.png"
image = cv2.imread(image_path)

# Determine the screen size (you may need to adjust these values)
screen_width = 1920
screen_height = 800

# Calculate the scaling factor to fit the image within the screen dimensions
scaling_factor = min(screen_width / image.shape[1], screen_height / image.shape[0])

# Resize the original image to fit within the screen
image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

# Camera matrix (intrinsic parameters), you may need to adjust these for your specific camera
camera_matrix = np.array([[800, 0, image.shape[1]/2],
                          [0, 800, image.shape[0]/2],
                          [0, 0, 1]], dtype=np.float32)

# Initial distortion coefficients
dist_coeffs = np.zeros(5, dtype=np.float32)

# Create a window
cv2.namedWindow('Undistorted Image')

# Define callback function for the trackbars
def update(val):
    # Get the current positions of the trackbars and map them to a range between -1 and 1
    k1 = (cv2.getTrackbarPos('k1', 'Undistorted Image') - 100) / 100.0
    k2 = (cv2.getTrackbarPos('k2', 'Undistorted Image') - 100) / 100.0
    p1 = (cv2.getTrackbarPos('p1', 'Undistorted Image') - 100) / 100.0
    p2 = (cv2.getTrackbarPos('p2', 'Undistorted Image') - 100) / 100.0
    k3 = (cv2.getTrackbarPos('k3', 'Undistorted Image') - 100) / 100.0

    # Update distortion coefficients
    dist_coeffs[:] = [k1, k2, p1, p2, k3]

    # Undistort the image
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)

    # Resize the undistorted image to fit within the screen dimensions
    undistorted_image = cv2.resize(undistorted_image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    # Display the undistorted image
    cv2.imshow('Undistorted Image', undistorted_image)

# Create trackbars for adjusting the distortion coefficients
cv2.createTrackbar('k1', 'Undistorted Image', 100, 200, update)
cv2.createTrackbar('k2', 'Undistorted Image', 100, 200, update)
cv2.createTrackbar('p1', 'Undistorted Image', 100, 200, update)
cv2.createTrackbar('p2', 'Undistorted Image', 100, 200, update)
cv2.createTrackbar('k3', 'Undistorted Image', 100, 200, update)

# Initial call to display the image
cv2.waitKey(500)  # Add a small delay to ensure trackbars are created
update(0)

# Wait until the user presses a key
cv2.waitKey(0)
cv2.destroyAllWindows()
