import numpy as np
from tensorflow import keras
import os

class NNEvaluatorV1:
    """Old model: 64-dimensional piece values"""
    def __init__(self, model_path='model_training/chess_eval_model.h5'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        self.model = keras.models.load_model(model_path, compile=False)
        self.eval_cache = {}
        print(f"✓ Loaded NN model V1 (64-dim) from {model_path}")
    
    def fen_to_vector(self, fen):
        """Convert FEN to 64-dimensional piece vector (old method)"""
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
        """Predict evaluation score"""
        if fen in self.eval_cache:
            return self.eval_cache[fen]
        
        vector = self.fen_to_vector(fen).reshape(1, 64)
        prediction = self.model.predict(vector, verbose=0)[0][0]
        score = float(prediction * 5.0)
        
        self.eval_cache[fen] = score
        return score