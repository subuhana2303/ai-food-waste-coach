import pandas as pd
import logging
from fuzzywuzzy import fuzz, process
import os

class NutritionDataHandler:
    """
    Handles nutrition and storage data with intelligent fuzzy matching
    """
    
    def __init__(self):
        self.data = None
        self.ingredient_names = []
        self._load_data()
    
    def _load_data(self):
        """Load nutrition data from CSV with error handling"""
        try:
            csv_path = 'nutrition_storage_dataset.csv'
            if os.path.exists(csv_path):
                self.data = pd.read_csv(csv_path)
                # Convert ingredient names to lowercase for matching
                self.data['ingredient_lower'] = self.data['Ingredient'].str.lower()
                self.ingredient_names = self.data['ingredient_lower'].tolist()
                logging.info(f"Loaded {len(self.data)} nutrition records")
            else:
                logging.warning(f"Nutrition data file not found: {csv_path}")
                self.data = pd.DataFrame()
        except Exception as e:
            logging.error(f"Error loading nutrition data: {str(e)}")
            self.data = pd.DataFrame()
    
    def _find_best_match(self, ingredient):
        """Find best matching ingredient using fuzzy matching"""
        if self.data is None or self.data.empty:
            return None
        
        ingredient_lower = ingredient.lower().strip()
        
        # First try exact match
        if self.data is not None:
            exact_match = self.data[self.data['ingredient_lower'] == ingredient_lower]
            if not exact_match.empty:
                return exact_match.iloc[0]
        
        # Try fuzzy matching
        best_match = process.extractOne(
            ingredient_lower, 
            self.ingredient_names,
            scorer=fuzz.ratio,
            score_cutoff=70  # Minimum 70% similarity
        )
        
        if best_match and self.data is not None:
            matched_ingredient = best_match[0]
            match_row = self.data[self.data['ingredient_lower'] == matched_ingredient]
            if not match_row.empty:
                return match_row.iloc[0]
        
        return None
    
    def get_nutrition_info(self, ingredient):
        """Get nutrition information for an ingredient"""
        try:
            match = self._find_best_match(ingredient)
            if match is not None:
                return {
                    'calories': self._safe_get(match, 'Calories_per_100g', 'N/A'),
                    'protein': self._safe_get(match, 'Protein_g', 'N/A'),
                    'carbs': self._safe_get(match, 'Carbs_g', 'N/A'),
                    'fat': self._safe_get(match, 'Fat_g', 'N/A')
                }
            return None
        except Exception as e:
            logging.error(f"Error getting nutrition info for {ingredient}: {str(e)}")
            return None
    
    def get_storage_tip(self, ingredient):
        """Get storage tip for an ingredient"""
        try:
            match = self._find_best_match(ingredient)
            if match is not None:
                tip = self._safe_get(match, 'Storage_Tip', '')
                return tip if tip and tip != 'N/A' and tip != '' else None
            return None
        except Exception as e:
            logging.error(f"Error getting storage tip for {ingredient}: {str(e)}")
            return None
    
    def _safe_get(self, row, column, default='N/A'):
        """Safely get value from pandas row"""
        try:
            value = row[column]
            if pd.isna(value) or value == '' or str(value).strip() == '':
                return default
            return str(value).strip()
        except (KeyError, AttributeError):
            return default
