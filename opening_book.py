import json

class OpeningBook:
    def __init__(self, json_file='custom_openings.json'):
        self.openings = []  # List of UCI move sequences as strings
        self.load_from_json(json_file)
    
    def load_from_json(self, json_file):
        """Load opening book from JSON file"""
        try:
            with open(json_file, 'r') as f:
                self.openings = json.load(f)
            print(f"Loaded opening book: {len(self.openings)} opening lines")
        except FileNotFoundError:
            print(f"File {json_file} not found. Generating...")
            try:
                from generate_openings import generate_opening_book
                self.openings = generate_opening_book()
            except Exception as e:
                print(f"Error: {e}")
                self.openings = []
        except Exception as e:
            print(f"Error loading: {e}")
            self.openings = []
    
    def get_next_move(self, current_moves_uci):
        """
        Find next move in the opening book.
        
        current_moves_uci: string like "e2e4 e7e5 g1f3"
        returns: next move as UCI string like "b8c6", or None
        """
        if not current_moves_uci:
            return None
        
        for opening_line in self.openings:
            # Check if current moves match the start of this opening
            if opening_line.startswith(current_moves_uci):
                # Get the part after current moves
                remaining = opening_line[len(current_moves_uci):].strip()
                if remaining:
                    # Extract the next move (first 4 characters of remaining)
                    next_move = remaining.split()[0]  # Get first move in remaining
                    return next_move
        
        return None