import cv2

# ==========================================
# VISIONFORGE - Image Preprocessing Test
# ==========================================

# 1. Load image
image = cv2.imread("vision/test_image.jpg")

# 2. Check whether image was loaded
if image is None:
    print("ERROR: Image could not be loaded.")

else:
    print("Image loaded successfully!")

    # --------------------------------------
    # 3. Original image information
    # --------------------------------------

    print("Original image shape:", image.shape)
    print("Original image height:", image.shape[0])
    print("Original image width:", image.shape[1])

    # --------------------------------------
    # 4. Resize image
    # --------------------------------------

    image_small = cv2.resize(
        image,
        (1200, 1000)
    )

    print("Resized image shape:", image_small.shape)

    # --------------------------------------
    # 5. Convert BGR to grayscale
    # --------------------------------------

    gray = cv2.cvtColor(
        image_small,
        cv2.COLOR_BGR2GRAY
    )

    print("Grayscale shape:", gray.shape)

    # --------------------------------------
    # 6. Check individual pixels
    # --------------------------------------

    print(
        "Top-left grayscale pixel:",
        gray[0, 0]
    )

    center_y = gray.shape[0] // 2
    center_x = gray.shape[1] // 2

    print(
        "Center grayscale pixel:",
        gray[center_y, center_x]
    )

    # --------------------------------------
    # 7. Gaussian Blur
    # --------------------------------------

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # --------------------------------------
    # 8. Thresholding
    # --------------------------------------

    _, binary = cv2.threshold(
        blurred,
        127,
        255,
        cv2.THRESH_BINARY
    )

    # --------------------------------------
    # 9. Find contours
    # --------------------------------------

    contours, hierarchy = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print("Original contours:", len(contours))

    # --------------------------------------
    # 10. Filter contours by area
    # --------------------------------------

    MIN_AREA = 1000

    contour_image = image_small.copy()

    object_count = 0

    for contour in contours:

        area = cv2.contourArea(contour)

        if area > MIN_AREA:

            object_count += 1

            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)

            print(
                f"Object {object_count}: "
                f"Area={area:.0f}, "
                f"Position=({x},{y}), "
                f"Size=({w}x{h})"
            )

            # Draw bounding box
            cv2.rectangle(
                contour_image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Label object
            cv2.putText(
                contour_image,
                f"Object {object_count}",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # --------------------------------------
    # 11. Print object count
    # --------------------------------------

    print("------------------------------")
    print("Filtered objects:", object_count)
    print("------------------------------")

    # --------------------------------------
    # 12. Display original image
    # --------------------------------------

    cv2.imshow(
        "VISIONFORGE - Original",
        image
    )

    # --------------------------------------
    # 13. Display resized image
    # --------------------------------------

    cv2.imshow(
        "VISIONFORGE - Resized",
        image_small
    )

    # --------------------------------------
    # 14. Display grayscale image
    # --------------------------------------

    cv2.imshow(
        "VISIONFORGE - Grayscale",
        gray
    )

    # --------------------------------------
    # 15. Display blurred image
    # --------------------------------------

    cv2.imshow(
        "VISIONFORGE - Blurred",
        blurred
    )

    # --------------------------------------
    # 16. Display binary image
    # --------------------------------------

    cv2.imshow(
        "VISIONFORGE - Binary",
        binary
    )

    # --------------------------------------
    # 17. Display detected objects
    # --------------------------------------

    cv2.imshow(
        "VISIONFORGE - Detected Objects",
        contour_image
    )

    # --------------------------------------
    # 18. Wait for key
    # --------------------------------------

    cv2.waitKey(0)

    # --------------------------------------
    # 19. Close all windows
    # --------------------------------------

    cv2.destroyAllWindows()