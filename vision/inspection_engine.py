from pathlib import Path
import math

import cv2
import numpy as np


# ============================================================
# VISIONFORGE - ASSEMBLY INSPECTION ENGINE
# Version 1.3
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
TEST_DIR = BASE_DIR / "test_images"

EXPECTED_POSITIONS = {
    "circle": (200, 250),
    "square": (400, 250),
    "triangle": (600, 250),
}

POSITION_TOLERANCE = 25
MIN_COMPONENT_AREA = 3000


# ============================================================
# 1. LOAD IMAGE
# ============================================================

def load_image(image_path):
    """Load and validate an image."""

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Cannot load image: {image_path}")

    if image.size == 0:
        raise ValueError("Image is empty.")

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected a color image.")

    return image


# ============================================================
# 2. DETECT COLORED COMPONENTS
# ============================================================

def detect_components(image):
    """Detect red circles, green squares and blue triangles."""

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color_ranges = {
        "circle": (
            np.array([0, 80, 50]),
            np.array([10, 255, 255]),
        ),
        "square": (
            np.array([35, 70, 40]),
            np.array([85, 255, 255]),
        ),
        "triangle": (
            np.array([100, 80, 50]),
            np.array([130, 255, 255]),
        ),
    }

    detections = []
    kernel = np.ones((3, 3), dtype=np.uint8)

    for component_name, (lower, upper) in color_ranges.items():

        mask = cv2.inRange(hsv, lower, upper)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel,
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < MIN_COMPONENT_AREA:
                continue

            moments = cv2.moments(contour)

            if moments["m00"] == 0:
                continue

            center = (
                int(moments["m10"] / moments["m00"]),
                int(moments["m01"] / moments["m00"]),
            )

            detections.append({
                "type": component_name,
                "center": center,
                "area": float(area),
                "contour": contour,
            })

    return detections


# ============================================================
# 3. DETERMINE TRIANGLE ORIENTATION
# ============================================================

def calculate_triangle_orientation(contour):
    """
    Determine whether the detected triangle points up or down.

    Returns:
        "up", "down", or None.
    """

    perimeter = cv2.arcLength(contour, True)

    polygon = cv2.approxPolyDP(
        contour,
        0.025 * perimeter,
        True,
    ).reshape(-1, 2)

    if len(polygon) != 3:
        return None

    # Sort vertices from top to bottom in image coordinates.
    vertices = sorted(
        polygon.tolist(),
        key=lambda point: point[1],
    )

    top = vertices[0]
    middle = vertices[1]
    bottom = vertices[2]

    # A triangle pointing UP has its tip at the top:
    #
    #             /\
    #            /  \
    #           /____\
    #
    # A triangle pointing DOWN has its tip at the bottom:
    #
    #           _____
    #            \  /
    #             \/

    top_y = top[1]
    middle_y = middle[1]
    bottom_y = bottom[1]

    # Compare vertical gaps between consecutive vertices.
    upper_gap = middle_y - top_y
    lower_gap = bottom_y - middle_y

    if upper_gap > lower_gap:
        return "up"

    return "down"


# ============================================================
# 4. INSPECT ASSEMBLY
# ============================================================

def inspect_assembly(image_path):

    image = load_image(image_path)
    detections = detect_components(image)

    defects = []

    grouped = {
        name: [
            item for item in detections
            if item["type"] == name
        ]
        for name in EXPECTED_POSITIONS
    }

    # --------------------------------------------------------
    # A. COMPONENT PRESENCE, DUPLICATES AND POSITION
    # --------------------------------------------------------

    for name, expected_position in EXPECTED_POSITIONS.items():

        found = grouped[name]

        if not found:
            defects.append(f"Missing {name} component")
            continue

        # Find the instance nearest to the expected location.
        selected = min(
            found,
            key=lambda item: math.dist(
                item["center"],
                expected_position,
            ),
        )

        distance = math.dist(
            selected["center"],
            expected_position,
        )

        if distance > POSITION_TOLERANCE:
            defects.append(f"{name.capitalize()} is misplaced")

        # Report additional components separately.
        for item in found:
            if item is not selected:
                defects.append(
                    f"Unexpected extra {name} detected "
                    f"at {item['center']}"
                )

    # --------------------------------------------------------
    # B. TRIANGLE ORIENTATION
    # --------------------------------------------------------

    triangles = grouped["triangle"]

    if triangles:

        expected_position = EXPECTED_POSITIONS["triangle"]

        selected_triangle = min(
            triangles,
            key=lambda item: math.dist(
                item["center"],
                expected_position,
            ),
        )

        orientation = calculate_triangle_orientation(
            selected_triangle["contour"]
        )

        if orientation is None:
            defects.append(
                "Unable to determine triangle orientation"
            )

        elif orientation != "up":
            defects.append(
                "Triangle orientation is incorrect"
            )

    # --------------------------------------------------------
    # C. RESULT
    # --------------------------------------------------------

    return {
        "image": str(image_path),
        "status": "PASS" if not defects else "FAIL",
        "detected_components": [
            {
                "type": item["type"],
                "center": item["center"],
                "area": round(item["area"], 2),
            }
            for item in detections
        ],
        "defects": defects,
    }


# ============================================================
# 5. PRINT RESULT
# ============================================================

def print_result(result):

    print("\n" + "=" * 60)
    print("          VISIONFORGE ASSEMBLY INSPECTION")
    print("=" * 60)

    print(f"Image: {Path(result['image']).name}")
    print(f"Result: {result['status']}")

    print("\nDetected components:")

    for item in result["detected_components"]:
        print(
            f"  - {item['type'].capitalize()}: "
            f"center={item['center']}, "
            f"area={item['area']}"
        )

    print("\nDefects:")

    if result["defects"]:
        for defect in result["defects"]:
            print(f"  - {defect}")
    else:
        print("  No defects detected.")

    print("=" * 60)


# ============================================================
# 6. TEST SUITE
# ============================================================

def main():

    test_cases = [
        ("correct.png", "PASS"),
        ("missing_component.png", "FAIL"),
        ("misplaced_component.png", "FAIL"),
        ("wrong_orientation.png", "FAIL"),
        ("extra_component.png", "FAIL"),
    ]

    passed = 0
    failed = 0

    print("\nStarting VISIONFORGE inspection tests...")

    for filename, expected_status in test_cases:

        image_path = TEST_DIR / filename

        try:
            result = inspect_assembly(image_path)
            print_result(result)

            # Check the overall status.
            status_correct = (
                result["status"] == expected_status
            )

            # Also check the expected defect category.
            defect_text = " ".join(result["defects"]).lower()

            if filename == "missing_component.png":
                reason_correct = "missing square" in defect_text

            elif filename == "misplaced_component.png":
                reason_correct = "square is misplaced" in defect_text

            elif filename == "wrong_orientation.png":
                reason_correct = "triangle orientation" in defect_text

            elif filename == "extra_component.png":
                reason_correct = "extra circle" in defect_text

            else:
                reason_correct = not result["defects"]

            if status_correct and reason_correct:
                print("TEST CHECK: PASSED")
                passed += 1
            else:
                print("TEST CHECK: FAILED")
                print(f"Expected status: {expected_status}")
                print(f"Actual status: {result['status']}")
                print(f"Expected reason check: {reason_correct}")
                failed += 1

        except (ValueError, cv2.error) as error:
            print(f"\nError processing {filename}: {error}")
            failed += 1

    print("\n" + "=" * 60)
    print("                  TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {passed + failed}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()