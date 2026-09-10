import cv2
import pytesseract

from app.config import TESSERACT_PATH


pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


IMAGE_PATH = r"test_editor_regions\app_1902.77_editor.jpg"

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise ValueError(
        f"Could not read image: {IMAGE_PATH}"
    )


print("=" * 80)
print("CODE OCR EXPERIMENT")
print("=" * 80)

print(
    f"ORIGINAL SIZE: "
    f"{image.shape[1]}x{image.shape[0]}"
)


# Convert to grayscale.
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY,
)


scales = [4, 6, 8]

psm_modes = [6, 11]


for scale in scales:

    resized = cv2.resize(
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC,
    )

    print()
    print("-" * 80)
    print(f"SCALE: {scale}x")
    print(
        f"SIZE: "
        f"{resized.shape[1]}x{resized.shape[0]}"
    )

    # --------------------------------------------------
    # RAW GRAYSCALE
    # --------------------------------------------------

    for psm in psm_modes:

        text = pytesseract.image_to_string(
            resized,
            lang="eng",
            config=f"--psm {psm}",
        )

        print()
        print(
            f"GRAYSCALE | PSM {psm}"
        )
        print(
            text.strip()
        )


    # --------------------------------------------------
    # OTSU THRESHOLD
    # --------------------------------------------------

    _, threshold = cv2.threshold(
        resized,
        0,
        255,
        cv2.THRESH_BINARY
        + cv2.THRESH_OTSU,
    )

    for psm in psm_modes:

        text = pytesseract.image_to_string(
            threshold,
            lang="eng",
            config=f"--psm {psm}",
        )

        print()
        print(
            f"OTSU | PSM {psm}"
        )
        print(
            text.strip()
        )


    # --------------------------------------------------
    # ADAPTIVE THRESHOLD
    # --------------------------------------------------

    adaptive = cv2.adaptiveThreshold(
        resized,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    for psm in psm_modes:

        text = pytesseract.image_to_string(
            adaptive,
            lang="eng",
            config=f"--psm {psm}",
        )

        print()
        print(
            f"ADAPTIVE | PSM {psm}"
        )
        print(
            text.strip()
        )