import cv2
import numpy as np
import random


# =============================================================================
# BASE CLASS — ImageAlteration
# =============================================================================

class ImageAlteration:
    """
    Base class for all alteration types.
    Each alteration affects a circular region defined by centre (x, y) and radius r.
    Child classes must implement the apply() method.
    """

    def __init__(self, x: int, y: int, r: int):
        """
        Initialise the alteration region.

        Args:
            x: x coordinate of the circle centre
            y: y coordinate of the circle centre
            r: radius of the circle
        """
        self.x = x
        self.y = y
        self.r = r

    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Apply this alteration to the image.
        Every child class MUST implement this method.
        """
        raise NotImplementedError("Subclass must implement apply()")

    def get_region(self) -> dict:
        """
        Return the circular region this alteration affects,
        in the standard format used across the application.

        Returns:
            dict: {'x': int, 'y': int, 'r': int, 'found': False}
        """
        pass

    def overlaps(self, other: 'ImageAlteration') -> bool:
        """
        Check if this alteration's circle overlaps with another.

        Args:
            other: another ImageAlteration instance to check against

        Returns:
            True if the circles overlap, False otherwise
        """
        pass

    def _get_circular_mask(self, image: np.ndarray) -> np.ndarray:
        """
        Create a mask the same size as the image.
        Pixels inside the circle are 255, outside are 0.
        Use this in child classes to apply effects only within the circle.

        Args:
            image: the image to base the mask size on

        Returns:
            mask as a numpy array
        """
        pass


# =============================================================================
# CHILD CLASS 1 — ColourShift
# =============================================================================

class ColourShift(ImageAlteration):
    """
    Shifts the hue of a circular region.
    The change should be noticeable on close inspection but not glaringly obvious.
    """

    def __init__(self, x: int, y: int, r: int, shift: int = 40):
        """
        Args:
            shift: how many degrees to rotate the hue (0-179 in OpenCV HSV)
        """
        super().__init__(x, y, r)
        self.shift = shift

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Rotate the hue channel within the circular region."""
        pass


# =============================================================================
# CHILD CLASS 2 — BlurAlteration
# =============================================================================

class BlurAlteration(ImageAlteration):
    """
    Applies a gaussian blur to a circular region.
    """

    def __init__(self, x: int, y: int, r: int, strength: int = 15):
        """
        Args:
            strength: blur kernel size — must be a positive odd number
        """
        super().__init__(x, y, r)
        self.strength = strength

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply gaussian blur within the circular region."""
        pass


# =============================================================================
# CHILD CLASS 3 — BrightnessAlteration
# =============================================================================

class BrightnessAlteration(ImageAlteration):
    """
    Increases or decreases the brightness of a circular region.
    """

    def __init__(self, x: int, y: int, r: int, amount: int = 60):
        """
        Args:
            amount: brightness adjustment. Positive = brighter, negative = darker.
        """
        super().__init__(x, y, r)
        self.amount = amount

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Adjust brightness within the circular region."""
        pass


# =============================================================================
# MAIN CLASS — ImageProcessor
# =============================================================================

class ImageProcessor:
    """
    Loads an image, creates a modified copy with exactly 5 non-overlapping
    circular differences, and exposes both images and region data to the app.
    """

    # Available alteration types — add new child classes here to extend
    ALTERATION_TYPES = [ColourShift, BlurAlteration, BrightnessAlteration]

    # Radius range for each difference circle (pixels)
    MIN_RADIUS = 20
    MAX_RADIUS = 50

    # Number of differences to generate
    NUM_DIFFERENCES = 5

    def __init__(self):
        self.original = None       # unmodified image (numpy array)
        self.modified = None       # image with differences applied (numpy array)
        self.alterations = []      # list of ImageAlteration instances
        self.image_path = None

    def load_image(self, path: str) -> bool:
        """
        Load an image from disk and generate 5 differences on a copy.

        Args:
            path: absolute or relative path to the image file (JPG, PNG, BMP)

        Returns:
            True if the image loaded successfully, False otherwise.
        """
        pass

    def generate_differences(self, image: np.ndarray) -> tuple:
        """
        Introduce exactly 5 non-overlapping circular differences into a copy
        of the image. Alteration type and position are chosen randomly each time.

        Args:
            image: the image to modify (numpy array)

        Returns:
            Tuple of (modified image, list of ImageAlteration instances)
        """
        pass

    def get_original(self) -> np.ndarray:
        """Return the original unmodified image."""
        pass

    def get_modified(self) -> np.ndarray:
        """Return the modified image with differences applied."""
        pass

    def get_regions(self) -> list:
        """
        Return the list of difference regions in standard format.

        Returns:
            List of dicts: [{'x': int, 'y': int, 'r': int, 'found': False}, ...]
        """
        pass

    def is_loaded(self) -> bool:
        """Returns True if an image has been successfully loaded."""
        pass