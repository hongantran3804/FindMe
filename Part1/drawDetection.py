import cv2
import math
import random

def draw_detection_boxes(image, boxes, classes, confidence_threshold=0.25):
    """
    Draws bounding boxes and class labels on the input image.

    Args:
        image (numpy.ndarray): The input image where detections will be drawn.
        boxes (numpy.ndarray): Array of detected bounding boxes and associated data.
            Each box is expected to have the format:
            [x_min, y_min, x_max, y_max, confidence_score, class_label].
        classes (list): List of class names corresponding to class labels.
        confidence_threshold (float, optional): Minimum confidence score for a detection
            to be drawn. Default is 0.25.

    Returns:
        None: Modifies the input image in-place by adding bounding boxes and labels.

    Raises:
        ValueError: If input `boxes` has invalid dimensions or if class labels
            cannot be found in the `classes` list.

    Example:
        boxes = np.array([[100, 50, 200, 150, 0.9, 1]])
        classes = ["person", "car"]
        image = cv2.imread("example.jpg")
        draw_detection_boxes(image, boxes, classes)
    """
    for box in boxes:
        ceil_box = [
            math.ceil(val) if i < len(box) - 2 else val for i, val in enumerate(box)
        ]
        x, y, x2, y2, score, label = ceil_box

        if score <= confidence_threshold:
            continue

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        label_text = f"{classes[int(label)]} {str(round(score, 2))}"

        cv2.rectangle(image, (x, y), (x2, y2), color, 2)

        text_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        text_w, text_h = text_size
        cv2.rectangle(image, (x, y), (x + text_w, y + text_h + 5), (0, 0, 0), -1)

        cv2.putText(
            image,
            label_text,
            (x, y + text_h),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
    cv2.imshow("Image with Detections", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
