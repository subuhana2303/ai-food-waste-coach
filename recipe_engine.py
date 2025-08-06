"""
Advanced Recipe Engine with Smart Recommendations
"""

import random
import logging
from typing import List, Dict, Any
from fuzzywuzzy import fuzz, process

class SmartRecipeEngine:
    """
    Intelligent recipe recommendation engine with cuisine-based suggestions
    """
    
    def __init__(self):
        self.recipe_database = {
            # Italian Cuisine
            'italian': [
                {
                    'name': 'Classic Margherita Pizza',
                    'ingredients': ['bread', 'tomato', 'cheese', 'basil'],
                    'instructions': [
                        'Use bread as pizza base or make dough',
                        'Spread tomato sauce evenly',
                        'Add mozzarella cheese generously',
                        'Top with fresh basil leaves',
                        'Bake at 450°F for 12-15 minutes'
                    ],
                    'prep_time': 25,
                    'difficulty': 'Easy',
                    'cuisine': 'Italian',
                    'waste_reduction_score': 95
                },
                {
                    'name': 'Pasta Primavera',
                    'ingredients': ['pasta', 'vegetables', 'garlic', 'olive_oil', 'cheese'],
                    'instructions': [
                        'Cook pasta according to package directions',
                        'Sauté mixed vegetables with garlic in olive oil',
                        'Toss pasta with vegetables',
                        'Finish with grated cheese and herbs',
                        'Serve immediately while hot'
                    ],
                    'prep_time': 20,
                    'difficulty': 'Easy',
                    'cuisine': 'Italian',
                    'waste_reduction_score': 90
                }
            ],
            
            # Asian Cuisine
            'asian': [
                {
                    'name': 'Vegetable Fried Rice',
                    'ingredients': ['rice', 'vegetables', 'eggs', 'soy_sauce', 'garlic'],
                    'instructions': [
                        'Use day-old rice for best texture',
                        'Scramble eggs and set aside',
                        'Stir-fry vegetables with garlic',
                        'Add rice and break up clumps',
                        'Mix in eggs and soy sauce, serve hot'
                    ],
                    'prep_time': 15,
                    'difficulty': 'Easy',
                    'cuisine': 'Asian',
                    'waste_reduction_score': 100
                },
                {
                    'name': 'Quick Vegetable Stir Fry',
                    'ingredients': ['vegetables', 'garlic', 'ginger', 'soy_sauce', 'oil'],
                    'instructions': [
                        'Heat oil in wok or large pan',
                        'Add garlic and ginger, stir for 30 seconds',
                        'Add harder vegetables first, then softer ones',
                        'Stir-fry for 3-5 minutes until crisp-tender',
                        'Season with soy sauce and serve over rice'
                    ],
                    'prep_time': 10,
                    'difficulty': 'Easy',
                    'cuisine': 'Asian',
                    'waste_reduction_score': 95
                }
            ],
            
            # American/Comfort Food
            'american': [
                {
                    'name': 'Loaded Grilled Cheese',
                    'ingredients': ['bread', 'cheese', 'tomato', 'onion', 'butter'],
                    'instructions': [
                        'Butter bread slices on outside',
                        'Layer cheese, tomato slices, and onion inside',
                        'Cook in pan over medium heat',
                        'Flip when golden brown on bottom',
                        'Cook until second side is golden and cheese melts'
                    ],
                    'prep_time': 8,
                    'difficulty': 'Easy',
                    'cuisine': 'American',
                    'waste_reduction_score': 85
                },
                {
                    'name': 'Hearty Vegetable Soup',
                    'ingredients': ['vegetables', 'broth', 'onion', 'garlic', 'herbs'],
                    'instructions': [
                        'Sauté onion and garlic until fragrant',
                        'Add chopped vegetables and cook 5 minutes',
                        'Pour in broth and bring to boil',
                        'Simmer 20-25 minutes until vegetables are tender',
                        'Season with herbs and serve hot'
                    ],
                    'prep_time': 35,
                    'difficulty': 'Easy',
                    'cuisine': 'American',
                    'waste_reduction_score': 98
                }
            ],
            
            # Mexican Cuisine
            'mexican': [
                {
                    'name': 'Quick Black Bean Quesadillas',
                    'ingredients': ['tortilla', 'beans', 'cheese', 'onion', 'peppers'],
                    'instructions': [
                        'Mash beans slightly with fork',
                        'Spread beans on half of tortilla',
                        'Add cheese, diced onion, and peppers',
                        'Fold tortilla and cook in dry pan',
                        'Flip once and cook until crispy and cheese melts'
                    ],
                    'prep_time': 12,
                    'difficulty': 'Easy',
                    'cuisine': 'Mexican',
                    'waste_reduction_score': 92
                }
            ],
            
            # Mediterranean
            'mediterranean': [
                {
                    'name': 'Greek-Style Vegetable Medley',
                    'ingredients': ['vegetables', 'olive_oil', 'lemon', 'herbs', 'cheese'],
                    'instructions': [
                        'Chop vegetables into uniform pieces',
                        'Toss with olive oil, lemon juice, and herbs',
                        'Roast at 400°F for 25-30 minutes',
                        'Sprinkle with crumbled cheese before serving',
                        'Serve warm or at room temperature'
                    ],
                    'prep_time': 40,
                    'difficulty': 'Easy',
                    'cuisine': 'Mediterranean',
                    'waste_reduction_score': 90
                }
            ]
        }
        
        # Ingredient categories for smart matching
        self.ingredient_categories = {
            'proteins': ['chicken', 'beef', 'pork', 'fish', 'eggs', 'beans', 'tofu', 'cheese'],
            'grains': ['rice', 'pasta', 'bread', 'quinoa', 'oats', 'noodles'],
            'vegetables': ['tomato', 'onion', 'garlic', 'carrot', 'potato', 'pepper', 'broccoli', 'spinach'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
            'pantry': ['oil', 'vinegar', 'soy_sauce', 'herbs', 'spices', 'salt', 'pepper']
        }
    
    def find_best_recipes(self, available_ingredients: List[str], max_recipes: int = 3) -> List[Dict[str, Any]]:
        """Find the best recipe matches for available ingredients"""
        all_recipes = []
        
        # Collect all recipes from all cuisines
        for cuisine_recipes in self.recipe_database.values():
            all_recipes.extend(cuisine_recipes)
        
        # Score each recipe based on ingredient availability
        scored_recipes = []
        
        for recipe in all_recipes:
            score = self._calculate_recipe_score(recipe, available_ingredients)
            if score > 0:  # Only include recipes with at least one matching ingredient
                recipe_with_score = recipe.copy()
                recipe_with_score['match_score'] = score
                recipe_with_score['missing_ingredients'] = self._find_missing_ingredients(recipe, available_ingredients)
                scored_recipes.append(recipe_with_score)
        
        # Sort by score and return top matches
        scored_recipes.sort(key=lambda x: x['match_score'], reverse=True)
        return scored_recipes[:max_recipes]
    
    def _calculate_recipe_score(self, recipe: Dict[str, Any], available_ingredients: List[str]) -> int:
        """Calculate how well a recipe matches available ingredients"""
        recipe_ingredients = recipe['ingredients']
        available_lower = [ing.lower().strip() for ing in available_ingredients]
        
        matches = 0
        total_recipe_ingredients = len(recipe_ingredients)
        
        for recipe_ing in recipe_ingredients:
            recipe_ing_lower = recipe_ing.lower().replace('_', ' ')
            
            # Check for exact matches first
            for avail_ing in available_lower:
                if recipe_ing_lower == avail_ing or recipe_ing_lower in avail_ing or avail_ing in recipe_ing_lower:
                    matches += 1
                    break
            else:
                # Use fuzzy matching for partial matches
                best_match = process.extractOne(recipe_ing_lower, available_lower, scorer=fuzz.ratio)
                if best_match and best_match[1] >= 70:  # 70% similarity threshold
                    matches += 0.7  # Partial credit for fuzzy matches
        
        # Calculate percentage match and boost for high waste reduction
        base_score = (matches / total_recipe_ingredients) * 100
        waste_bonus = recipe.get('waste_reduction_score', 0) * 0.1
        
        return int(base_score + waste_bonus)
    
    def _find_missing_ingredients(self, recipe: Dict[str, Any], available_ingredients: List[str]) -> List[str]:
        """Find ingredients needed to complete the recipe"""
        recipe_ingredients = recipe['ingredients']
        available_lower = [ing.lower().strip() for ing in available_ingredients]
        missing = []
        
        for recipe_ing in recipe_ingredients:
            recipe_ing_lower = recipe_ing.lower().replace('_', ' ')
            
            # Check if ingredient is available
            found = False
            for avail_ing in available_lower:
                if (recipe_ing_lower == avail_ing or 
                    recipe_ing_lower in avail_ing or 
                    avail_ing in recipe_ing_lower):
                    found = True
                    break
            
            if not found:
                # Check fuzzy match
                best_match = process.extractOne(recipe_ing_lower, available_lower, scorer=fuzz.ratio)
                if not best_match or best_match[1] < 70:
                    missing.append(recipe_ing.replace('_', ' ').title())
        
        return missing
    
    def get_recipe_suggestions_by_cuisine(self, available_ingredients: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Get recipe suggestions organized by cuisine type"""
        cuisine_suggestions = {}
        
        for cuisine, recipes in self.recipe_database.items():
            cuisine_matches = []
            for recipe in recipes:
                score = self._calculate_recipe_score(recipe, available_ingredients)
                if score > 30:  # At least 30% match
                    recipe_with_score = recipe.copy()
                    recipe_with_score['match_score'] = score
                    recipe_with_score['missing_ingredients'] = self._find_missing_ingredients(recipe, available_ingredients)
                    cuisine_matches.append(recipe_with_score)
            
            if cuisine_matches:
                cuisine_matches.sort(key=lambda x: x['match_score'], reverse=True)
                cuisine_suggestions[cuisine] = cuisine_matches[:2]  # Top 2 per cuisine
        
        return cuisine_suggestions
    
    def generate_creative_combinations(self, available_ingredients: List[str]) -> List[Dict[str, Any]]:
        """Generate creative recipe combinations based on available ingredients"""
        creative_recipes = []
        
        # Categorize available ingredients
        categorized = self._categorize_ingredients(available_ingredients)
        
        # Generate fusion recipes based on available categories
        if categorized['proteins'] and categorized['grains']:
            creative_recipes.append({
                'name': f"Fusion {categorized['proteins'][0].title()} Bowl",
                'description': f"Creative bowl combining {', '.join(categorized['proteins'])} with {', '.join(categorized['grains'])}",
                'estimated_prep_time': 20,
                'creativity_score': 85,
                'ingredients_used': categorized['proteins'] + categorized['grains'] + categorized['vegetables'][:2]
            })
        
        if len(categorized['vegetables']) >= 3:
            creative_recipes.append({
                'name': "Rainbow Veggie Medley",
                'description': f"Colorful combination of {', '.join(categorized['vegetables'][:4])}",
                'estimated_prep_time': 15,
                'creativity_score': 75,
                'ingredients_used': categorized['vegetables'][:4]
            })
        
        return creative_recipes
    
    def _categorize_ingredients(self, ingredients: List[str]) -> Dict[str, List[str]]:
        """Categorize ingredients by type"""
        categorized = {category: [] for category in self.ingredient_categories.keys()}
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower().strip()
            categorized_flag = False
            
            for category, category_ingredients in self.ingredient_categories.items():
                for cat_ing in category_ingredients:
                    if cat_ing in ingredient_lower or ingredient_lower in cat_ing:
                        categorized[category].append(ingredient)
                        categorized_flag = True
                        break
                if categorized_flag:
                    break
        
        return categorized
    
    def get_cooking_tips(self, recipe: Dict[str, Any]) -> List[str]:
        """Get cooking tips for a specific recipe"""
        tips = [
            "Prep all ingredients before starting to cook",
            "Taste and adjust seasoning as you go",
            "Use fresh herbs when possible for better flavor"
        ]
        
        # Add recipe-specific tips
        if recipe.get('cuisine') == 'asian':
            tips.extend([
                "Heat your pan properly before adding oil",
                "Cut vegetables uniformly for even cooking",
                "Don't overcrowd the pan when stir-frying"
            ])
        elif recipe.get('cuisine') == 'italian':
            tips.extend([
                "Use good quality olive oil for best flavor",
                "Don't rinse pasta after cooking",
                "Save some pasta water for adjusting sauce consistency"
            ])
        
        return tips[:4]  # Return top 4 tips