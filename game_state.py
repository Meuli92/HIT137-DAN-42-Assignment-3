import math

class GameState:

    def __init__(self):
        self.regions = []
        self.mistakes = 0
        self.found_count = 0

        """
        regions: A list of dictionaries provided by the OpenCV class.
        Example: {'x': 100, 'y': 150, 'radius': 15, 'found': False}
        """
    def new_round(self, regions:list):
        self.regions = regions
        self.mistakes = 0
        self.max_mistakes = 3
        self.found_count = 0
        self.total_differences = 5

    def _get_distance(self, x1, y1, x2, y2):
        """Proximity Logic: Calculates Euclidean distance."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def check_click(self, x: int, y: int) -> str:
        """
        Validates the click against hidden regions.
        """
        if self.mistakes >= self.max_mistakes:
            return 'locked'

        for region in self.regions:
            # Calculate how close the click was to the center of the difference
            distance = self._get_distance(x, y, region['x'], region['y'])
            
            # Complexity Detection: Smaller radius = harder to hit
            if distance <= region['r']:
                if region['found']:
                    return 'already_found'
                
                region['found'] = True
                self.found_count += 1
                return 'hit'
        
        # No hit found in the loop
        self.mistakes += 1
        return 'miss'
    
    def get_found_regions(self):
        return [r for r in self.regions if r['found']]

    def get_unfound_regions(self) -> list:
        """Provides data for the 'Reveal' button."""
        return [r for r in self.regions if not r['found']]

    def is_game_over(self) -> bool:
        """Checks if the user has failed (3 mistakes) or won (5 found)."""
        return self.mistakes >= self.max_mistakes or self.found_count == self.total_differences
    
    def get_remaining(self):
        return self.total_differences - self.found_count

    def get_mistakes(self):
        return self.mistakes

    def is_complete(self):
        return self.found_count >= self.total_differences
