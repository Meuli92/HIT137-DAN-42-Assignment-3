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