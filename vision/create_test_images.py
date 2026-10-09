from pathlib import Path

import cv2
import numpy as np


# Directory containing the generated inspection images
OUTPUT_DIR = Path(__file__).resolve().parent / "test_images"

# Image settings
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 500
BACKGROUND = (245, 245, 245)

# Expected component locations: (x, y)
CIRCLE_CENTER = (200, 250)
SQUARE_CENTER = (400, 250)
TRIANGLE_CENTER = (600, 250)

# Component dimensions
CIRCLE_RADIUS = 45
SQUARE_HALF_SIZE = 45
TRIANGLE_SIZE = 55


def create_blank_image():
    """Create a clean background for an assembly image."""
    image = np.full(
        (IMAGE_HEIGHT, IMAGE_WIDTH, 3),
        BACKGROUND,
        dtype=np.uint8,
    )

    # Draw a thin border around the inspection area
    cv2.rectangle(
        image,
        (40, 40),
        (760, 460),
        (180, 180, 180),
        2,
    )

    return image


def draw_circle(image, center=CIRCLE_CENTER):
    """Draw the circular component."""
    cv2.circle(image, center, CIRCLE_RADIUS, (40, 90, 220), -1)
    cv2.circle(image, center, CIRCLE_RADIUS, (20, 20, 20), 3)


def draw_square(image, center=SQUARE_CENTER):
    """Draw the square component."""
    x, y = center

    cv2.rectangle(
        image,
        (x - SQUARE_HALF_SIZE, y - SQUARE_HALF_SIZE),
        (x + SQUARE_HALF_SIZE, y + SQUARE_HALF_SIZE),
        (40, 170, 70),
        -1,
    )

    cv2.rectangle(
        image,
        (x - SQUARE_HALF_SIZE, y - SQUARE_HALF_SIZE),
        (x + SQUARE_HALF_SIZE, y + SQUARE_HALF_SIZE),
        (20, 20, 20),
        3,
    )


def draw_triangle(image, center=TRIANGLE_CENTER, rotation=0):
    """Draw a triangular component with a configurable orientation."""
    cx, cy = center

    angles = np.array([90, 210, 330], dtype=np.float32) + rotation
    radians = np.deg2rad(angles)

    points = np.column_stack(
        (
            cx + TRIANGLE_SIZE * np.cos(radians),
            cy - TRIANGLE_SIZE * np.sin(radians),
        )
    ).astype(np.int32)

    points = points.reshape((-1, 1, 2))

    cv2.fillPoly(image, [points], (220, 100, 40))
    cv2.polylines(
        image,
        [points],
        isClosed=True,
        color=(20, 20, 20),
        thickness=3,
    )


def save_image(image, filename):
    """Save an image and report its location."""
    output_path = OUTPUT_DIR / filename

    if not cv2.imwrite(str(output_path), image):
        raise RuntimeError(f"Could not save image: {output_path}")

    print(f"Created: {output_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Correct assembly
    image = create_blank_image()
    draw_circle(image)
    draw_square(image)
    draw_triangle(image)
    save_image(image, "correct.png")

    # 2. Missing component: no square
    image = create_blank_image()
    draw_circle(image)
    draw_triangle(image)
    save_image(image, "missing_component.png")

    # 3. Misplaced component: square shifted to the right
    image = create_blank_image()
    draw_circle(image)
    draw_square(image, center=(490, 250))
    draw_triangle(image)
    save_image(image, "misplaced_component.png")

    # 4. Wrong orientation: triangle rotated by 180 degrees
    image = create_blank_image()
    draw_circle(image)
    draw_square(image)
    draw_triangle(image, rotation=180)
    save_image(image, "wrong_orientation.png")

    # 5. Extra component: an additional circle
    image = create_blank_image()
    draw_circle(image)
    draw_square(image)
    draw_triangle(image)
    draw_circle(image, center=(700, 370))
    save_image(image, "extra_component.png")

    print("\nAll five test images were generated successfully.")


if __name__ == "__main__":
    main()