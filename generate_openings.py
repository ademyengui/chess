import json

def generate_opening_book():
    """Generate opening book as a simple list of UCI move sequences"""
    
    openings = [
    # Ruy Lopez
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6 c2c3 e8g8 h2h3 c6a5 b3c2 c7c5 d2d4 d8c7",
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6 c2c3 e8g8 h2h3 c6b8 d2d4 b8d7",
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 e8g8 c2c3 d7d6 h2h3 c6b8 d2d4 b8d7",
    
    # Sicilian Defense - Najdorf
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 c1g5 e7e6 f2f4 b8d7 d1f3 d8c7 e1c1",
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 f2f4 e7e5 d4b3 c8e6 f1c4 b8c6",
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 a2a4 b8c6 c1g5 e7e6 f2f4 f8e7",
    
    # Sicilian Defense - Dragon
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6 c1e3 f8g7 f2f3 e8g8 d1d2 b8c6",
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6 c1e3 f8g7 f2f3 b8c6 d1d2 e8g8 f1c4",
    
    # Sicilian Defense - Classical
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4 f3d4 g8f6 b1c3 d7d6 f1e2 e7e5 d4b3 f8e7 e1g1 e8g8",
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4 f3d4 g8f6 b1c3 d7d6 f1b5 c8d7 b5c6 b7c6",
    
    # French Defense
    "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5 f8e7 e4e5 f6d7 g5e7 d8e7 f2f4 e8g8 g1f3 c7c5 d4c5 b8c6",
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5 a2a3 b4c3 b2c3 g8e7 a3a4 b8c6 g1f3 d8a5",
    "e2e4 e7e6 d2d4 d7d5 b1d2 g8f6 e4e5 f6d7 f2f4 c7c5 g1f3 b8c6 c2c3",
    
    # Caro-Kann
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 c8f5 e4g3 f5g6 h2h4 h7h6 g1f3 b8d7 h4h5 g6h7 f1d3 h7d3 d1d3",
    "e2e4 c7c6 d2d4 d7d5 e4e5 c8f5 f1e2 e7e6 g1f3 f8e7 e1g1 d8d7",
    "e2e4 c7c6 g1f3 d7d5 e4e5 c8f5 d2d4 e7e6 f1e2 c6c5 e1g1 b8c6",
    
    # Pirc Defense
    "e2e4 d7d6 d2d4 g8f6 b1c3 g7g6 f2f4 f8g7 g1f3 e8g8 f1e2 b8c6 e1g1 e7e5",
    "e2e4 d7d6 d2d4 g8f6 b1c3 g7g6 g1f3 f8g7 f1e2 e8g8 e1g1 b8c6 d4d5 c6b8",
    
    # Queen's Gambit Declined
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3 e8g8 g1f3 b8d7 a1c1 c7c6",
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3 e8g8 g1f3 b8d7 a1c1 c7c6 c4d5",
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 g1f3 f8e7 c1f4 e8g8 e2e3 c7c5 c4d5 f6d5",
    
    # Slav Defense
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 a2a4 c8f4 e2e3 b7b5 a4b5 c6b5 f3e5",
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 e7e6 e2e3 b8d7 f1d3 f8d6 e1g1 e8g8",
    
    # King's Indian Defense
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3 e8g8 f1e2 e7e5 e1g1 b8c6 d4d5 c6e7",
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3 e8g8 f1e2 e7e5 e1g1 b8c6 d4d5 c6e7 f3e1 f6e8",
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 f2f3 e8g8 c1e3 e7e5 d4d5 c7c6",
    
    # Grünfeld Defense
    "d2d4 g8f6 c2c4 g7g6 b1c3 d7d5 c4d5 f6d5 e2e4 d5c3 b2c3 c7c5 f1b5 c8d7",
    "d2d4 g8f6 c2c4 g7g6 b1c3 d7d5 c4d5 f6d5 e2e4 d5c3 b2c3 c7c5 g1f3 f8g7 f1e4 e8g8",
    
    # Nimzo-Indian Defense
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 d1c2 d7d5 c4d5 e6d5 c1g5 h7h6 g5h4 c7c5 d4c5 b4c3",
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 d1c2 c7c5 d4c5 e8g8 a2a3 b4c5 g1f3 b7b6",
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 e2e3 c7c5 f1d3 b8c6 g1e2 d7d5 e1g1 e8g8",
    
    # Queen's Indian Defense
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6 e2e3 c8b7 f1d3 d7d5 e1g1 f8e7 b1c3 e8g8",
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6 a2a3 c8b7 b1c3 d7d5 c4d5 f6d5",
    
    # English Opening
    "c2c4 e7e5 b1c3 g8f6 g1f3 b8c6 e2e4 f8b4 f3e5 c6e5 d2d4 b4e7 d4e5 f6e4",
    "c2c4 e7e5 b1c3 g8f6 g1f3 b8c6 g2g3 d7d5 c4d5 f6d5 f1g2 d5b6",
    "c2c4 c7c5 b1c3 b8c6 g1f3 g8f6 d2d4 c5d4 f3d4 e7e6 g2g3 d8b6",
    
    # Reti Opening
    "g1f3 d7d5 c2c4 d5c4 e2e3 g8f6 f1c4 e7e6 e1g1 c7c5 b2b3 b8c6 c1b2 f8e7",
    "g1f3 d7d5 g2g3 g8f6 f1g2 c7c5 e1g1 b8c6 d2d4 e7e6",
    
    # Dutch Defense
    "d2d4 f7f5 c2c4 g8f6 b1c3 e7e6 g1f3 f8e7 e2e3 e8g8 f1d3 d7d5 e1g1 c7c6",
    "d2d4 f7f5 g2g3 g8f6 f1g2 e7e6 g1f3 f8e7 e1g1 e8g8 c2c4 d7d6",
    
    # Benoni Defense
    "d2d4 g8f6 c2c4 c7c5 d4d5 e7e6 b1c3 e6d5 c4d5 d7d6 e2e4 g7g6 g1f3 f8g7",
    "d2d4 g8f6 c2c4 c7c5 d4d5 e7e6 b1c3 e6d5 c4d5 d7d6 e2e4 g7g6 f2f4 f8g7 g1f3 e8g8",
    
    # Benko Gambit
    "d2d4 g8f6 c2c4 c5c5 d4d5 b7b5 c4b5 a7a6 b5a6 c8a6 b1c3 d7d6 e2e4 a6f1 e1f1 g7g6",
    
    # Scandinavian Defense
    "e2e4 d7d5 e4d5 d8d5 b1c3 d8a5 d2d4 g8f6 g1f3 c8g4 f1e2 b8c6",
    "e2e4 d7d5 e4d5 g8f6 d2d4 f6d5 c2c4 d5b6 g1f3 c8g4",
    
    # Alekhine's Defense
    "e2e4 g8f6 e4e5 f6d5 d2d4 d7d6 g1f3 c8g4 f1e2 e7e6 e1g1 b8c6",
    "e2e4 g8f6 e4e5 f6d5 d2d4 d7d6 g1f3 g7g6 c2c4 d5b6 h2h3 f8g7",
    
    # Modern Defense
    "e2e4 g7g6 d2d4 f8g7 b1c3 d7d6 f1e3 c7c6 d1d2 b8d7",
    "e2e4 g7g6 d2d4 f8g7 g1f3 d7d6 f1c4 g8f6 d1e2 e8g8 e1g1 c7c5",
    
    # Budapest Gambit
    "d2d4 g8f6 c2c4 e7e5 d4e5 f6g4 b2b3 g4e5 c1b2 d7d6 g1f3 e5c6",
    
    # Albin Countergambit
    "d2d4 d7d5 c2c4 e7e5 d4e5 d5d4 b1c3 g8f6 g1f3 b8c6 a2a3 c8g4",
    
    # Catalan Opening
    "d2d4 g8f6 c2c4 e7e6 g2g3 d7d5 f1g2 f8e7 g1f3 e8g8 e1g1 b7b6",
    "d2d4 g8f6 c2c4 e7e6 g2g3 d7d5 f1g2 f8e7 g1f3 e8g8 e1g1 d5c4 d1c2 a7a6",
    
    # Italian Game
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d3 d7d6 b2b4 c5b6 a2a4 a7a5",
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4 c5b4 c1d2 b4d2 b1d2 d7d5",
    
    # Scotch Game
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 f8c5 c1e3 d8f6 c2c3 g8e7",
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 g8f6 d4c6 b7c6 e4e5 f6e4 d1e4 d7d5",
    
    # Vienna Game
    "e2e4 e7e5 b1c3 g8f6 f2f4 d7d5 e4d5 f6d5 f4e5 c8f5 g1f3 b8c6",
    "e2e4 e7e5 b1c3 g8f6 g1f3 b8c6 f1b5 f8b4 e1g1 e8g8 d2d3 d7d6 c1g5",
    
    # King's Gambit
    "e2e4 e7e5 f2f4 e5f4 g1f3 g7g5 f1c4 g5g4 e1g1 g4f3 d1f3 d8f6",
    "e2e4 e7e5 f2f4 e5f4 g1f3 d7d5 e4d5 g8f6 f1c4 f6d5 e1g1 f8e7",
    
    # Evans Gambit
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 b2b4 c5b4 c2c3 b4a5 d2d4 e5d4 e1g1 d4c3",
    
    # Four Knights Game
    "e2e4 e7e5 g1f3 b8c6 b1c3 g8f6 f1b5 f8b4 e1g1 e8g8 d2d3 d7d6 c1g5 b4c3",
    
    # Philidor Defense
    "e2e4 e7e5 g1f3 d7d6 d2d4 g8f6 b1c3 b8d7 f1c4 f8e7 e1g1 e8g8",
    
    # Portuguese Opening
    "e2e4 e7e5 g1f3 b8c6 f1b5 c6b4 c2c3 b4a6 b2b4 a6b4 c3b4 f8b4 d2d4",
    
    # Icelandic Gambit
    "e2e4 d7d5 e4d5 g8f6 c2c4 c7c6 d5c6 b8c6 d2d4 c8g4",
    
    # Polish Opening
    "b2b4 e7e5 c1b2 f8b4 e2e3 b7b6 g1f3 c8b7 f1e2 g8f6",
    
    # Bird's Opening
    "f2f4 d7d5 g1f3 g8f6 e2e3 g7g6 f1e2 f8g7 e1g1 e8g8",
    
    # Nimzowitsch-Larsen Attack
    "b2b3 e7e5 c1b2 b8c6 e2e3 d7d5 g1f3 g8f6 f1b5 f8d6",
    
    # Grob's Attack
    "g2g4 d7d5 f1g2 c7c6 g1f3 c8g4 h2h3 g4f3 d1f3 e7e5",
    
    # Dunst Opening
    "b1c3 d7d5 e2e4 d5e4 c3e4 g8f6 e4f6 d8f6 d2d4 c7c6",
    
    # Veresov Attack
    "d2d4 d7d5 b1c3 g8f6 c1g5 b8d7 f2f3 c7c6 e2e4 d5e4 d1d2"
]
    
    print(f"Generated {len(openings)} opening lines")
    save_opening_book(openings)
    return openings

def save_opening_book(openings):
    """Save opening book to JSON file"""
    try:
        with open('custom_openings.json', 'w') as f:
            json.dump(openings, f, indent=2)
        print(f"Opening book saved with {len(openings)} lines")
    except Exception as e:
        print(f"Error saving: {e}")

if __name__ == "__main__":
    generate_opening_book()