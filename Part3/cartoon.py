import cv2

"""
Function: cartoonizeImage

Description:
    This function applies a cartoon effect to an image specified by the given file path. It uses OpenCV to process the image, combining edge detection and smoothing techniques to create a cartoon-like representation.

Parameters:
    image_path (str):
        The file path to the image that will be cartoonized.

Steps:
    Reads the input image using `cv2.imread`.
    Converts the image to grayscale using `cv2.cvtColor`.
    Applies a median blur to the grayscale image to reduce noise.
    Detects edges in the image using adaptive thresholding.
    Applies a bilateral filter to the original image to smooth colors while preserving edges.
    Combines the filtered image and the edge mask using `cv2.bitwise_and` to create the cartoon effect.
    Displays the resulting cartoon image using `cv2.imshow`.
    Waits for a key press and closes the display window using `cv2.waitKey` and `cv2.destroyAllWindows`.
"""
def cartoonizeImage(image_path):
    newImage = cv2.imread(image_path)
    grey = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    grey = cv2.medianBlur(grey, 5)
    edges = cv2.adaptiveThreshold(
        grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )

    color = cv2.bilateralFilter(newImage, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    cv2.imshow("Cartoon", cartoon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
