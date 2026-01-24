import numpy as np
from tensorflow import keras
import re

class NNEvaluator:
    def __init__(self, model_path='/home/adem/Desktop/projects/chess/model_training/chess_eval_model.h5'):
        self.model = keras.models.load_model(model_path, compile=False) # compile=false was added bu copilot
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        print(f"Loaded NN model from {model_path}")
    
    def fen_to_vector(self, fen):
        """Convert FEN to 64-dimensional vector"""
        piece_map = {
            'P': 1, 'p': 2,
            'N': 3, 'n': 4,
            'B': 5, 'b': 6,
            'R': 7, 'r': 8,
            'Q': 9, 'q': 10,
            'K': 11, 'k': 12
        }
        
        board_fen = fen.split()[0]
        vector = []
        
        for rank in board_fen.split('/'):
            for char in rank:
                if char.isdigit():
                    for _ in range(int(char)):
                        vector.append(0)
                else:
                    vector.append(piece_map.get(char, 0))
        
        return np.array(vector) / 12.0
    
    def evaluate(self, fen):
        """Predict evaluation score for a position (FEN)"""
        vector = self.fen_to_vector(fen).reshape(1, 64)
        prediction = self.model.predict(vector, verbose=0)[0][0]
        # Scale back from -1 to 1 range to actual evaluation
        return float(prediction * 5.0)