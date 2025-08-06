"""
Smart Features for AI Food Waste Coach
Advanced features to make the application hackathon-winning
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SmartFoodManager:
    """
    Advanced food management with predictive expiration tracking
    """
    
    def __init__(self):
        self.expiration_database = {
            # Fresh Produce (days)
            'tomato': {'fridge': 7, 'counter': 3, 'signs': ['soft spots', 'wrinkled skin', 'mold']},
            'banana': {'fridge': 10, 'counter': 4, 'signs': ['brown spots', 'mushy texture', 'strong odor']},
            'apple': {'fridge': 30, 'counter': 7, 'signs': ['brown spots', 'soft texture', 'wrinkled skin']},
            'lettuce': {'fridge': 10, 'counter': 2, 'signs': ['wilted leaves', 'brown edges', 'slimy texture']},
            'carrot': {'fridge': 21, 'counter': 7, 'signs': ['white spots', 'rubbery texture', 'black spots']},
            'onion': {'fridge': 30, 'counter': 14, 'signs': ['soft spots', 'sprouting', 'mold']},
            'potato': {'fridge': 14, 'counter': 21, 'signs': ['green spots', 'sprouting', 'soft spots']},
            
            # Dairy Products
            'milk': {'fridge': 7, 'counter': 0.5, 'signs': ['sour smell', 'chunky texture', 'separation']},
            'cheese': {'fridge': 14, 'counter': 2, 'signs': ['mold growth', 'strong odor', 'hard texture']},
            'yogurt': {'fridge': 14, 'counter': 1, 'signs': ['separation', 'mold', 'off smell']},
            
            # Proteins
            'chicken': {'fridge': 2, 'freezer': 180, 'signs': ['gray color', 'slimy texture', 'off odor']},
            'beef': {'fridge': 3, 'freezer': 240, 'signs': ['brown color', 'sticky texture', 'sour smell']},
            'fish': {'fridge': 2, 'freezer': 90, 'signs': ['fishy odor', 'slimy texture', 'cloudy eyes']},
            'eggs': {'fridge': 28, 'counter': 7, 'signs': ['cracked shell', 'floating in water', 'sulfur smell']},
            
            # Grains and Pantry
            'rice': {'pantry': 365, 'cooked_fridge': 3, 'signs': ['insects', 'musty smell', 'hard texture']},
            'pasta': {'pantry': 730, 'cooked_fridge': 5, 'signs': ['insects', 'stale smell', 'brittle texture']},
            'bread': {'counter': 5, 'fridge': 10, 'freezer': 90, 'signs': ['mold spots', 'hard texture', 'stale smell']}
        }
    
    def predict_expiration(self, ingredient: str, storage_location: str = 'fridge') -> Dict[str, Any]:
        """Predict when an ingredient will expire"""
        ingredient_lower = ingredient.lower().strip()
        
        # Find matching ingredient
        expiration_info = None
        for key, info in self.expiration_database.items():
            if key in ingredient_lower or ingredient_lower in key:
                expiration_info = info
                break
        
        if not expiration_info:
            # Default estimation
            expiration_info = {'fridge': 7, 'counter': 3, 'signs': ['changes in texture', 'off odor', 'discoloration']}
        
        # Calculate expiration date
        days_until_expiration = expiration_info.get(storage_location, expiration_info.get('fridge', 7))
        expiration_date = datetime.now() + timedelta(days=days_until_expiration)
        
        # Determine urgency level
        if days_until_expiration <= 1:
            urgency = 'Critical - Use Today!'
            urgency_color = '#dc3545'  # Red
        elif days_until_expiration <= 3:
            urgency = 'High - Use Soon'
            urgency_color = '#fd7e14'  # Orange
        elif days_until_expiration <= 7:
            urgency = 'Medium - Plan Usage'
            urgency_color = '#ffc107'  # Yellow
        else:
            urgency = 'Low - Fresh'
            urgency_color = '#28a745'  # Green
        
        return {
            'ingredient': ingredient.title(),
            'days_remaining': days_until_expiration,
            'expiration_date': expiration_date.strftime('%Y-%m-%d'),
            'urgency_level': urgency,
            'urgency_color': urgency_color,
            'spoilage_signs': expiration_info.get('signs', []),
            'storage_tips': self._get_optimal_storage_tips(ingredient, storage_location)
        }
    
    def _get_optimal_storage_tips(self, ingredient: str, current_location: str) -> List[str]:
        """Get optimal storage tips for an ingredient"""
        ingredient_lower = ingredient.lower().strip()
        
        general_tips = {
            'fridge': [
                'Store in airtight container to prevent moisture loss',
                'Keep away from strong-smelling foods',
                'Check regularly for signs of spoilage'
            ],
            'counter': [
                'Keep in cool, dry place away from direct sunlight',
                'Ensure good air circulation',
                'Store away from heat sources'
            ],
            'freezer': [
                'Wrap tightly to prevent freezer burn',
                'Label with date for easy tracking',
                'Use freezer-safe containers'
            ]
        }
        
        # Ingredient-specific tips
        specific_tips = {
            'banana': ['Store separately as they release ethylene gas'],
            'tomato': ['Store stem-side down to prevent moisture loss'],
            'potato': ['Store in dark place to prevent greening'],
            'onion': ['Store in well-ventilated area'],
            'bread': ['Store in breadbox or sealed container']
        }
        
        tips = general_tips.get(current_location, [])
        
        for key, ingredient_tips in specific_tips.items():
            if key in ingredient_lower:
                tips.extend(ingredient_tips)
                break
        
        return tips[:3]  # Return top 3 tips

class RecipePersonalizer:
    """
    Personalize recipes based on dietary preferences and restrictions
    """
    
    def __init__(self):
        self.dietary_substitutions = {
            'vegan': {
                'milk': 'almond milk',
                'butter': 'coconut oil',
                'cheese': 'nutritional yeast',
                'eggs': 'flax eggs',
                'chicken': 'tofu',
                'beef': 'mushrooms'
            },
            'gluten_free': {
                'bread': 'gluten-free bread',
                'pasta': 'rice noodles',
                'flour': 'almond flour',
                'soy_sauce': 'tamari'
            },
            'dairy_free': {
                'milk': 'oat milk',
                'cheese': 'dairy-free cheese',
                'butter': 'vegan butter',
                'yogurt': 'coconut yogurt'
            },
            'keto': {
                'rice': 'cauliflower rice',
                'pasta': 'zucchini noodles',
                'potato': 'turnip',
                'bread': 'cloud bread'
            }
        }
    
    def personalize_recipe(self, recipe: Dict[str, Any], dietary_preferences: List[str]) -> Dict[str, Any]:
        """Personalize recipe based on dietary preferences"""
        personalized_recipe = recipe.copy()
        original_ingredients = recipe['ingredients'].copy()
        substitutions_made = []
        
        for preference in dietary_preferences:
            if preference.lower() in self.dietary_substitutions:
                substitutions = self.dietary_substitutions[preference.lower()]
                
                for i, ingredient in enumerate(personalized_recipe['ingredients']):
                    ingredient_lower = ingredient.lower().replace('_', ' ')
                    
                    for original, substitute in substitutions.items():
                        if original in ingredient_lower:
                            personalized_recipe['ingredients'][i] = substitute
                            substitutions_made.append(f"{original.title()} → {substitute.title()}")
                            break
        
        if substitutions_made:
            personalized_recipe['substitutions'] = substitutions_made
            personalized_recipe['dietary_adapted'] = dietary_preferences
        
        return personalized_recipe

class FoodWastePrevention:
    """
    Advanced food waste prevention strategies
    """
    
    def __init__(self):
        self.preservation_methods = {
            'fruits': [
                'Freeze overripe fruits for smoothies',
                'Make fruit leather or dried fruit',
                'Create fruit compotes or jams',
                'Blend into ice cream or sorbet'
            ],
            'vegetables': [
                'Blanch and freeze for later use',
                'Make vegetable stock from scraps',
                'Pickle vegetables for preservation',
                'Dehydrate for veggie chips'
            ],
            'herbs': [
                'Freeze in ice cubes with oil',
                'Dry herbs for seasoning blends',
                'Make herb-infused oils',
                'Create pesto or herb butter'
            ],
            'bread': [
                'Make breadcrumbs for coating',
                'Create croutons for salads',
                'Transform into bread pudding',
                'Use for stuffing or dressing'
            ]
        }
    
    def get_preservation_strategies(self, ingredients: List[str]) -> Dict[str, List[str]]:
        """Get preservation strategies for specific ingredients"""
        strategies = {}
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower().strip()
            
            # Categorize ingredient and get strategies
            if any(fruit in ingredient_lower for fruit in ['apple', 'banana', 'berry', 'orange', 'grape']):
                strategies[ingredient] = self.preservation_methods['fruits']
            elif any(veg in ingredient_lower for veg in ['carrot', 'celery', 'onion', 'potato', 'tomato']):
                strategies[ingredient] = self.preservation_methods['vegetables']
            elif any(herb in ingredient_lower for herb in ['basil', 'parsley', 'cilantro', 'mint']):
                strategies[ingredient] = self.preservation_methods['herbs']
            elif 'bread' in ingredient_lower:
                strategies[ingredient] = self.preservation_methods['bread']
            else:
                # General preservation strategies
                strategies[ingredient] = [
                    'Store properly to extend freshness',
                    'Use in multiple recipes to avoid waste',
                    'Share with neighbors or friends',
                    'Compost if no longer edible'
                ]
        
        return strategies

class InventoryTracker:
    """
    Smart inventory tracking with purchase date prediction
    """
    
    def __init__(self):
        self.consumption_patterns = {
            'daily': ['milk', 'bread', 'eggs', 'coffee'],
            'weekly': ['chicken', 'rice', 'pasta', 'vegetables'],
            'bi_weekly': ['flour', 'sugar', 'spices', 'canned_goods'],
            'monthly': ['oils', 'vinegars', 'specialty_items']
        }
    
    def predict_next_purchase(self, ingredient: str, last_purchase_date: str = None) -> Dict[str, Any]:
        """Predict when to next purchase an ingredient"""
        if not last_purchase_date:
            last_purchase_date = datetime.now().strftime('%Y-%m-%d')
        
        last_purchase = datetime.strptime(last_purchase_date, '%Y-%m-%d')
        ingredient_lower = ingredient.lower().strip()
        
        # Determine consumption pattern
        pattern = 'weekly'  # default
        for freq, ingredients in self.consumption_patterns.items():
            if any(item in ingredient_lower for item in ingredients):
                pattern = freq
                break
        
        # Calculate next purchase date
        days_mapping = {
            'daily': 3,
            'weekly': 7,
            'bi_weekly': 14,
            'monthly': 30
        }
        
        days_until_next = days_mapping[pattern]
        next_purchase_date = last_purchase + timedelta(days=days_until_next)
        days_remaining = (next_purchase_date - datetime.now()).days
        
        return {
            'ingredient': ingredient.title(),
            'consumption_pattern': pattern,
            'next_purchase_date': next_purchase_date.strftime('%Y-%m-%d'),
            'days_until_purchase': max(0, days_remaining),
            'recommendation': self._get_purchase_recommendation(days_remaining, pattern)
        }
    
    def _get_purchase_recommendation(self, days_remaining: int, pattern: str) -> str:
        """Get purchase recommendation based on timing"""
        if days_remaining <= 0:
            return "🛒 Time to restock!"
        elif days_remaining <= 2:
            return "⚠️ Running low - add to shopping list"
        elif days_remaining <= 5:
            return "📝 Plan to purchase soon"
        else:
            return "✅ Well stocked"

class SustainabilityCoach:
    """
    Provide sustainability coaching and tips
    """
    
    def __init__(self):
        self.sustainability_facts = [
            {
                'fact': 'Food waste accounts for 8-10% of global greenhouse gas emissions',
                'action': 'Plan your meals to reduce waste',
                'impact': 'High'
            },
            {
                'fact': 'Composting food scraps can reduce methane emissions by 50%',
                'action': 'Start a compost bin for vegetable scraps',
                'impact': 'Medium'
            },
            {
                'fact': 'Buying seasonal produce reduces carbon footprint by 30%',
                'action': 'Choose seasonal ingredients when shopping',
                'impact': 'Medium'
            },
            {
                'fact': 'Proper food storage can extend freshness by 50%',
                'action': 'Learn optimal storage methods for each ingredient',
                'impact': 'High'
            }
        ]
    
    def get_daily_sustainability_tip(self) -> Dict[str, str]:
        """Get a daily sustainability tip"""
        tip = random.choice(self.sustainability_facts)
        return {
            'fact': tip['fact'],
            'action': tip['action'],
            'impact_level': tip['impact'],
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def calculate_weekly_impact_summary(self, user_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate weekly sustainability impact summary"""
        total_recipes = len(user_actions)
        total_ingredients_saved = sum(action.get('ingredients_used', 0) for action in user_actions)
        
        # Estimate impact
        estimated_waste_reduced = total_ingredients_saved * 0.3  # kg
        estimated_water_saved = estimated_waste_reduced * 500  # liters
        estimated_co2_reduced = estimated_waste_reduced * 2.5  # kg
        
        return {
            'week_ending': datetime.now().strftime('%Y-%m-%d'),
            'recipes_created': total_recipes,
            'ingredients_rescued': total_ingredients_saved,
            'waste_reduced_kg': round(estimated_waste_reduced, 1),
            'water_saved_liters': round(estimated_water_saved, 1),
            'co2_reduced_kg': round(estimated_co2_reduced, 2),
            'sustainability_score': min(100, total_recipes * 10 + total_ingredients_saved * 5)
        }