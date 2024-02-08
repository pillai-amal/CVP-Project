import numpy as np
import cv2
import os 

def is_grayscale(crop):
    red_average = np.average(crop[:,:,0])
    green_average = np.average(crop[:,:,1])
    blue_average = np.average(crop[:,:,2])
    highest_distance = max(abs(red_average-green_average), abs(red_average-blue_average), abs(green_average-blue_average))
    return highest_distance <= 15

def process_image(image):
    height, width, _ = image.shape
    result_image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            crop = image[y:y+1, x:x+1]
            if is_grayscale(crop):
                result_image[y, x] = [0, 0, 0]  # Black for grayscale
            else:
                result_image[y, x] = [255, 255, 255]  # White for non-grayscale
    return result_image

# Load the image from "../obj1/1.png"
if __name__ == "__main__":
    for i in [4]:
        image_dir = "../obj{}/".format(i)
        for image in os.listdir(image_dir):
            image_path = os.path.join(image_dir, image)
            rgb_image = cv2.imread(image_path)

            if rgb_image is not None:
                # Process the image
                result_image = process_image(rgb_image)

                # Convert the result to grayscale
                gray_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2GRAY)

                # Save the grayscale image
                cv2.imwrite('./masks/{}/{}'.format(i,image), gray_image)
            else:
                print(f"Failed to load the image from {image_path}. Please check the file path.")
