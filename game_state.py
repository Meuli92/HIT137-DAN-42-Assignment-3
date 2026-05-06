class GameState:
    def __init__(self, regions: list):
        self.regions = regions
        self.mistakes = 0
        self.max_mistakes = 3
        self.found_count = 0
    
    def check_click(self, x: int, y: int) -> str:
        """
        Check if click falls within an unfound difference region.
        Returns 'hit', 'miss', 'already_found', or 'locked' (max mistakes reached).
        """
        pass
    
    def is_complete(self) -> bool:
        """Returns True if all 5 differences have been found."""
        pass
    
    def is_locked(self) -> bool:
        """Returns True if max mistakes reached."""
        pass
    
    def reset(self):
        """Reset state for a new image."""
        pass

####----WORKING ON SKELETON CODE (UNFINISHED)-------####
class GameState:
    def __init__(self, regions: list):
        self.regions = regions  # List of dicts: {'x':, 'y':, 'radius':, 'found': False}
        self.mistakes = 0
        self.max_mistakes = 3
        self.found_count = 0
        self.click_threshold = 20 # Standard proximity buffer

    def check_click(self, x: int, y: int) -> str:
        if self.is_locked():
            return 'locked'

        for region in self.regions:
            distance = self._get_distance(x, y, region['x'], region['y'])
            
            # Check if distance is within the 'proximity' of the region
            if distance <= region.get('radius', self.click_threshold):
                if region['found']:
                    return 'already_found'
                
                region['found'] = True
                self.found_count += 1
                return 'hit'
        
        self.mistakes += 1
        return 'miss'

    def _get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def is_complete(self) -> bool:
        return self.found_count == 5

    def is_locked(self) -> bool:
        return self.mistakes >= self.max_mistakes

    def get_game_summary(self):
        """Useful for complexity detection requirements."""
        # Logic to return how many hard vs easy targets were found
        pass
