import cv2
import numpy as np
import random


class ImageAlteration:
    """Base class for image alterations applied to a rectangular region."""

    def __init__(self, x, y, w, h):
        """Initialise the alteration with the region coordinates.

        Args:
            x: Left edge of the region in pixels.
            y: Top edge of the region in pixels.
            w: Width of the region in pixels.
            h: Height of the region in pixels.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def apply(self, image):
        """Apply the alteration to the given image.

        Args:
            image: A numpy array (BGR) to modify in place.

        Returns:
            The modified image array.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError


class ColourShift(ImageAlteration):
    """Applies a random per-pixel colour noise shift to a region."""

    def apply(self, image):
        """Apply random per-pixel colour noise to the region.

        Args:
            image: A numpy array (BGR) to modify in place.

        Returns:
            The modified image array.
        """
        region = image[self.y:self.y + self.h, self.x:self.x + self.w].astype(np.int16)

        shift = np.random.randint(-45, 45, region.shape)
        region = np.clip(region + shift, 0, 255).astype(np.uint8)

        image[self.y:self.y + self.h, self.x:self.x + self.w] = region
        return image


class BrightnessChange(ImageAlteration):
    """Applies a uniform brightness increase or decrease to a region."""

    def apply(self, image):
        """Apply a uniform brightness shift to the region.

        Args:
            image: A numpy array (BGR) to modify in place.

        Returns:
            The modified image array.
        """
        region = image[self.y:self.y + self.h, self.x:self.x + self.w].astype(np.int16)

        value = random.randint(-70, 70)
        region = np.clip(region + value, 0, 255).astype(np.uint8)

        image[self.y:self.y + self.h, self.x:self.x + self.w] = region
        return image


class AddShape(ImageAlteration):
    """Blends a randomly coloured circle into a region."""

    def apply(self, image):
        """Blend a randomly coloured circle into the region.

        Args:
            image: A numpy array (BGR) to modify in place.

        Returns:
            The modified image array.
        """
        overlay = image.copy()

        center = (self.x + self.w // 2, self.y + self.h // 2)
        radius = min(self.w, self.h) // 3

        color = (random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255))

        cv2.circle(overlay, center, radius, color, -1)

        roi = image[self.y:self.y + self.h,
                    self.x:self.x + self.w]
        overlay_roi = overlay[self.y:self.y + self.h,
                              self.x:self.x + self.w]

        alpha = 0.60
        blended = cv2.addWeighted(overlay_roi, alpha, roi, 1 - alpha, 0)

        image[self.y:self.y + self.h,
              self.x:self.x + self.w] = blended

        return image

class EdgeWarp(ImageAlteration):
    def apply(self, image):
        region = image[self.y: self.y + self.h, self.x: self.x + self.w].copy()

        shift = 5

        M = np.float32([
            [1, 0, random.randint(-shift, shift)],
            [0, 1, random.randint(-shift, shift)]
        ])

        warped = cv2.warpAffine(region, M, (region.shape[1], region.shape[0]))

        image[self.y: self.y + self.h, self.x: self.x + self.w] = warped
        return image
        
class ImageProcessor:
    """Loads an image and generates a modified version with random differences."""

    def __init__(self):
        """Initialise the processor with no image loaded."""
        self.num_differences = 5
        self.original = None
        self.modified = None
        self.differences = []

    def load_image(self, image_path: str) -> bool:
        """Load an image from disk and generate differences on the modified copy.

        Args:
            image_path: File path to the image to load.

        Returns:
            True if the image loaded successfully, False otherwise.

        Raises:
            RuntimeError: If differences could not be placed after max attempts.
        """
        self.original = cv2.imread(image_path)
        if self.original is None:
            return False
        self.modified = self.original.copy()
        self.differences = []
        self.generate_differences()
        return True

    def is_loaded(self) -> bool:
        """Return True if an image has been successfully loaded."""
        return self.original is not None

    def get_original(self) -> np.ndarray:
        """Return a copy of the original unmodified image."""
        return self.original.copy()

    def get_modified(self) -> np.ndarray:
        """Return a copy of the modified image with differences applied."""
        return self.modified.copy()

    def get_regions(self) -> list:
        """Return a list of region dicts describing each difference location.

        Each dict contains keys: x, y, w, h, center_x, center_y, r, found.
        """
        regions = []
        for (x, y, w, h, _) in self.differences:
            regions.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "center_x": x + w // 2,
                "center_y": y + h // 2,
                "r": max(min(w, h) // 2, 20),
                "found": False
            })
        return regions

    def generate_differences(self):
        """Place random non-overlapping alterations on the modified image.

        Raises:
            RuntimeError: If the required number of differences cannot be
                placed within the maximum number of attempts.
        """
        height, width, _ = self.original.shape

        attempts = 0
        max_attempts = 500

        while (len(self.differences) < self.num_differences
               and attempts < max_attempts):
            attempts += 1

            w = random.randint(width // 12, width // 6)
            h = random.randint(height // 12, height // 6)

            x = random.randint(0, width - w)
            y = random.randint(0, height - h)

            new_rect = (x, y, w, h)

            if not self._is_overlapping(new_rect):
                alteration_class = random.choice([ColourShift,
                                                  BrightnessChange,
                                                  AddShape,
                                                  EdgeWarp])
                alteration = alteration_class(x, y, w, h)
                self.modified = alteration.apply(self.modified)
                self.differences.append((x, y, w, h, alteration_class.__name__))

        if len(self.differences) < self.num_differences:
            raise RuntimeError("Failed to generate differences")

    def _is_overlapping(self, new_rect: tuple) -> bool:
        """Check whether a candidate rectangle overlaps any existing difference.

        Args:
            new_rect: A tuple of (x, y, w, h) for the candidate region.

        Returns:
            True if the candidate overlaps an existing region, False otherwise.
        """
        nx, ny, nw, nh = new_rect

        for (x, y, w, h, _) in self.differences:
            if (nx < x + w and nx + nw > x and ny < y + h and ny + nh > y):
                return True
        return False
