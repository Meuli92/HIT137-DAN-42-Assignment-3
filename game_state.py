class GameState:

    def __init__(self):
        self.regions = []
        self.mistakes = 0
        self.max_mistakes = 3
        self.found_count = 0
        self.total_differences = 5

    def new_round(self, regions:list):
        self.regions = regions
        self.mistakes = 0
        self.max_mistakes = 3
        self.found_count = 0
        self.total_differences = 5

    def check_click(self, x: int, y: int) -> str:
        if self.mistakes >= self.max_mistakes:
            return 'locked'

        for region in self.regions:
            if (region['x'] <= x <= region['x'] + region['w']
            and region['y'] <= y <= region['y'] + region['h']):
                if region['found']:
                    return 'already_found'
                
                region['found'] = True
                self.found_count += 1
                return 'hit'
        
        self.mistakes += 1
        return 'miss'
    
    def get_found_regions(self) -> list:
        return [r for r in self.regions if r['found']]

    def get_unfound_regions(self) -> list:
        return [r for r in self.regions if not r['found']]

    def is_game_over(self) -> bool:
        return (self.mistakes >= self.max_mistakes
                or
                self.found_count == self.total_differences)
    
    def get_remaining(self) -> int:
        return self.total_differences - self.found_count

    def get_mistakes(self) -> int:
        return self.mistakes

    def is_complete(self) -> bool:
        return self.found_count == self.total_differences

    def is_locked(self) -> bool:
        return self.mistakes >= self.max_mistakes
