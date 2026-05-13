import cv2
import numpy as np
import random 

class ImageAlteration:
  def __init__(self, x, y, w, h):
      self.x = x
      self.y = y
      self.w = w
      self.h = h

  def apply(self, image):
      raise NotImplementedError

class ColourShift(ImageAlteration):
    def apply(self, image):
        region = image[self.y:self.y
        + self.h, self.x: self.x
        + self.w].astype(np.int16)

        shift = np.random.randint(-25, 25, region.shape)
        region = np.clip(region + shift, 0, 255).astype(np.uint8)

        image[self.y:self.y
        + self.h, self.x:self.x
        + self.w]
        = region
        return image

class BrightnessChange (ImageAlteration):
    def apply(self, image):
        region = image[self.y:self.y
        + self.h, self.x: self.x
        + self.w].astype(np.int16)

        value = random.randint(-40, 40)
        region = np.clip(region + value, 0, 255).astype(np.uint8)

        image[self.y:self.y
        + self.h, self.x:self.x
        + self.w]
        = region
        return image

class AddShape(ImageAlteration):
    def apply(self, image):
        overlay = image.copy()

        center = (self.x + self.w // 2, self.y + self.h // 2)
        radius = min(self.w, self.h) // 3

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        cv2.circle(overlay, center, radius, color, -1)

        roi = image[self.y: self.y + self.h, self.x: self.x + self.w]
        overlay_roi = overlay[self.y: self.y + self.h, self.x: self.x + self.w]

        alpha = 0.45
        blended = cv2.addWeighted(overlay_roi, alpha, roi, 1 - alpha, 0)

        image[self.y: self.y + self.h, self.x: self.x + self.w] = blended

        return image

class ImageProcessor:  
    def __init__ (self):
        self.num_differences = 5
        self.original = None
        self.modified = None
        self.differences = []

    def load_image(self, image_path):
        self.original = cv2.imread(image_path)
        if self.original is None:
            return False
        self.modified = self.original.copy()
        self.differences = []
        self.generate_differences()
        return True
 
    def is_loaded(self):
        return self.original is not None
 
    def get_original(self):
        return self.original.copy()
 
    def get_modified(self):
        return self.modified.copy()
 
    def get_regions(self):
        regions = []
        for (x, y, w, h, _) in self.differences:
            regions.append({"x": x, "y": y, "w": w, "h": h,
            "center_x": x + w // 2,
            "center_y": y + h // 2,
            "r": max(min(w, h) // 2, 20),
            "found": False})
        return regions
 
    def generate_differences(self):
        height, width, _ = self.original.shape

        attempts = 0
        max_attempts = 500

        while len(self.differences) < self.num_differences and attempts < max_attempts:
            attempts += 1

            w = random.randint(width // 12, width // 6)
            h = random.randint(height // 12, height // 6)

            x = random.randint(0, width - w)
            y = random.randint(0, height - h)

            new_rect = (x, y, w, h)

            if not self._is_overlapping(new_rect):

                alteration_class = random.choice([ColourShift, BrightnessChange, AddShape])

                alteration = alteration_class(x, y, w, h)
                self.modified = alteration.apply(self.modified)

                self.differences.append((x, y, w, h, alteration_class.__name__))

        if len(self.differences) < self.num_differences:
            raise RuntimeError("Failed to generate differences") 
    
    def get_images(self):
        return self.original, self.modified

    def get_differences(self):
        return self.differences

    def is_click_inside(self, click_x, click_y, tolerance = 10):
        for (x, y, w, h, _) in self.differences:
            if (x - tolerance <= click_x <= x + w + tolerance
            and y - tolerance <= click_y <= y + h + tolerance):
                return True
        return False

    def draw_debug(self):
        debug = self.modified.copy()

        for (x, y, w, h, _) in self.differences:
            cv2.rectangle(debug, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return debug 

    def _is_overlapping(self, new_rect):
        nx, ny, nw, nh = new_rect

        for (x, y, w, h, _) in self.differences:
            if (nx < x + w and nx + nw > x and ny < y + h and ny + nh > y):
                return True
        return False
