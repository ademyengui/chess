import numpy as np
from tensorflow import keras
import os

class NNEvaluatorV2:
    def __init__(self, model_path='model_2/chess_eval_model_final.h5'):
        """Load the trained NN model"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        self.model = keras.models.load_model(model_path, compile=False)
        self.eval_cache = {}  # Cache for repeated positions
        print(f"✓ Loaded NN model from {model_path}")
    
    def fen_to_vector(self, fen):
        """Convert FEN to 781-dimensional bitboard vector"""
        try:
            parts = fen.split()
            if len(parts) < 4:
                return None
            
            board_fen = parts[0]
            side_to_move = parts[1]
            castling = parts[2]
            en_passant = parts[3]
            
            piece_types = ['P', 'p', 'N', 'n', 'B', 'b', 'R', 'r', 'Q', 'q', 'K', 'k']
            bitboards = np.zeros(768, dtype=np.float32)
            
            square = 0
            for rank in board_fen.split('/'):
                for char in rank:
                    if char.isdigit():
                        square += int(char)
                    else:
                        if char in piece_types:
                            piece_idx = piece_types.index(char)
                            bitboards[piece_idx * 64 + square] = 1.0
                        square += 1
            
            castling_features = np.zeros(4, dtype=np.float32)
            if 'K' in castling:
                castling_features[0] = 1.0
            if 'Q' in castling:
                castling_features[1] = 1.0
            if 'k' in castling:
                castling_features[2] = 1.0
            if 'q' in castling:
                castling_features[3] = 1.0
            
            en_passant_features = np.zeros(8, dtype=np.float32)
            if en_passant != '-' and len(en_passant) >= 1:
                file = ord(en_passant[0]) - ord('a')
                if 0 <= file < 8:
                    en_passant_features[file] = 1.0
            
            side_feature = np.array([1.0 if side_to_move == 'w' else 0.0], dtype=np.float32)
            
            vector = np.concatenate([bitboards, castling_features, en_passant_features, side_feature])
            return vector
        except:
            return None
    
    def evaluate(self, fen):
        """Predict evaluation score for a position (FEN)"""
        # Check cache first
        if fen in self.eval_cache:
            return self.eval_cache[fen]
        
        vector = self.fen_to_vector(fen)
        if vector is None:
            return 0.0  # Default to 0 if FEN is invalid
        
        vector = vector.reshape(1, 781)
        prediction = self.model.predict(vector, verbose=0)[0][0]
        
        # Scale back from -1 to 1 range to actual evaluation
        score = float(prediction * 5.0)
        
        # Cache the result
        self.eval_cache[fen] = score
        
        return score