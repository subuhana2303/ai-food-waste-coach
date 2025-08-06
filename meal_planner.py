"""
AI-Powered Weekly Meal Planner
"""

import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

class AIWeeklyMealPlanner:
    """
    Generate personalized weekly meal plans to minimize food waste
    """
    
    def __init__(self):
        self.meal_templates = {
            'breakfast': [
                {'name': 'Veggie Omelet', 'ingredients': ['eggs', 'onion', 'bell pepper', 'cheese'], 'prep_time': 10},
                {'name': 'Fruit Smoothie Bowl', 'ingredients': ['banana', 'berries', 'yogurt', 'oats'], 'prep_time': 5},
                {'name': 'Avocado Toast', 'ingredients': ['bread', 'avocado', 'tomato', 'eggs'], 'prep_time': 8},
                {'name': 'Leftover Fried Rice', 'ingredients': ['rice', 'eggs', 'vegetables', 'soy_sauce'], 'prep_time': 12}
            ],
            'lunch': [
                {'name': 'Quick Stir Fry', 'ingredients': ['vegetables', 'protein', 'rice', 'garlic'], 'prep_time': 15},
                {'name': 'Soup & Salad', 'ingredients': ['broth', 'vegetables', 'greens', 'bread'], 'prep_time': 20},
                {'name': 'Grain Bowl', 'ingredients': ['quinoa', 'roasted_vegetables', 'protein', 'dressing'], 'prep_time': 25},
                {'name': 'Leftover Remix', 'ingredients': ['yesterday_dinner', 'fresh_herbs', 'new_sauce'], 'prep_time': 8}
            ],
            'dinner': [
                {'name': 'One-Pan Roasted Meal', 'ingredients': ['protein', 'root_vegetables', 'herbs', 'olive_oil'], 'prep_time': 35},
                {'name': 'Pasta Primavera', 'ingredients': ['pasta', 'seasonal_vegetables', 'garlic', 'cheese'], 'prep_time': 20},
                {'name': 'Sheet Pan Fish', 'ingredients': ['fish', 'vegetables', 'lemon', 'herbs'], 'prep_time': 25},
                {'name': 'Curry Night', 'ingredients': ['protein', 'vegetables', 'coconut_milk', 'spices'], 'prep_time': 30}
            ]
        }
        
        self.waste_reduction_tips = [
            "Buy only what you need for the week",
            "Use older ingredients first (FIFO method)",
            "Transform leftovers into new meals",
            "Prep vegetables when you get home",
            "Freeze items before they spoil",
            "Make soup or smoothies with wilting produce",
            "Use herb stems in stocks and broths",
            "Keep a 'eat first' section in your fridge"
        ]
        
        self.seasonal_ingredients = {
            'spring': ['asparagus', 'peas', 'radishes', 'lettuce', 'strawberries'],
            'summer': ['tomatoes', 'zucchini', 'corn', 'berries', 'stone_fruits'],
            'fall': ['squash', 'apples', 'root_vegetables', 'brussels_sprouts', 'pears'],
            'winter': ['citrus', 'cabbage', 'potatoes', 'onions', 'carrots']
        }
    
    def generate_weekly_plan(self, available_ingredients: List[str], dietary_preferences: List[str] = None) -> Dict[str, Any]:
        """Generate a complete weekly meal plan"""
        if dietary_preferences is None:
            dietary_preferences = []
        
        # Get current season
        current_season = self.get_current_season()
        seasonal_items = self.seasonal_ingredients[current_season]
        
        # Generate 7 days of meals
        weekly_plan = {}
        start_date = datetime.now()
        
        for day in range(7):
            current_date = start_date + timedelta(days=day)
            day_name = current_date.strftime('%A')
            
            daily_meals = {
                'breakfast': self.select_meal('breakfast', available_ingredients, dietary_preferences),
                'lunch': self.select_meal('lunch', available_ingredients, dietary_preferences),
                'dinner': self.select_meal('dinner', available_ingredients, dietary_preferences)
            }
            
            weekly_plan[day_name] = {
                'date': current_date.strftime('%Y-%m-%d'),
                'meals': daily_meals,
                'daily_tip': random.choice(self.waste_reduction_tips)
            }
        
        # Generate shopping list
        shopping_list = self.generate_shopping_list(weekly_plan, available_ingredients)
        
        # Calculate waste reduction potential
        waste_reduction = self.calculate_waste_reduction_potential(weekly_plan)
        
        return {
            'weekly_plan': weekly_plan,
            'shopping_list': shopping_list,
            'waste_reduction': waste_reduction,
            'seasonal_focus': seasonal_items,
            'planning_tips': self.get_planning_tips()
        }
    
    def select_meal(self, meal_type: str, available_ingredients: List[str], dietary_preferences: List[str]) -> Dict[str, Any]:
        """Select appropriate meal based on available ingredients"""
        meal_options = self.meal_templates[meal_type]
        
        # Score meals based on ingredient overlap
        scored_meals = []
        for meal in meal_options:
            score = 0
            available_lower = [ing.lower() for ing in available_ingredients]
            
            for ingredient in meal['ingredients']:
                # Check for partial matches
                for avail_ing in available_lower:
                    if ingredient.lower() in avail_ing or avail_ing in ingredient.lower():
                        score += 1
                        break
            
            scored_meals.append((meal, score))
        
        # Select meal with highest score (or random if tie)
        scored_meals.sort(key=lambda x: x[1], reverse=True)
        best_score = scored_meals[0][1]
        best_meals = [meal for meal, score in scored_meals if score == best_score]
        
        selected_meal = random.choice(best_meals)
        
        return {
            'name': selected_meal['name'],
            'ingredients': selected_meal['ingredients'],
            'prep_time': selected_meal['prep_time'],
            'ingredient_match_score': best_score,
            'waste_reduction_potential': self.calculate_meal_waste_reduction(selected_meal, available_ingredients)
        }
    
    def generate_shopping_list(self, weekly_plan: Dict[str, Any], available_ingredients: List[str]) -> Dict[str, List[str]]:
        """Generate optimized shopping list"""
        needed_ingredients = set()
        available_lower = [ing.lower() for ing in available_ingredients]
        
        # Collect all needed ingredients
        for day_data in weekly_plan.values():
            for meal in day_data['meals'].values():
                for ingredient in meal['ingredients']:
                    # Check if we already have this ingredient
                    if not any(ingredient.lower() in avail.lower() or avail.lower() in ingredient.lower() 
                             for avail in available_lower):
                        needed_ingredients.add(ingredient)
        
        # Categorize shopping list
        categories = {
            'proteins': ['chicken', 'fish', 'beef', 'tofu', 'eggs', 'beans'],
            'vegetables': ['tomato', 'onion', 'garlic', 'bell_pepper', 'carrot', 'broccoli', 'spinach'],
            'grains': ['rice', 'pasta', 'bread', 'quinoa', 'oats'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter'],
            'pantry': ['olive_oil', 'spices', 'herbs', 'soy_sauce', 'vinegar']
        }
        
        categorized_list = {category: [] for category in categories.keys()}
        categorized_list['other'] = []
        
        for ingredient in needed_ingredients:
            categorized = False
            for category, items in categories.items():
                if any(item in ingredient.lower() for item in items):
                    categorized_list[category].append(ingredient.replace('_', ' ').title())
                    categorized = True
                    break
            
            if not categorized:
                categorized_list['other'].append(ingredient.replace('_', ' ').title())
        
        # Remove empty categories
        return {k: v for k, v in categorized_list.items() if v}
    
    def calculate_waste_reduction_potential(self, weekly_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential waste reduction from meal planning"""
        total_meals = len(weekly_plan) * 3  # 7 days * 3 meals
        planned_ingredient_usage = 0
        
        for day_data in weekly_plan.values():
            for meal in day_data['meals'].values():
                planned_ingredient_usage += meal.get('waste_reduction_potential', 0)
        
        # Estimate impact
        estimated_food_saved_kg = planned_ingredient_usage * 0.2  # 200g per matched ingredient
        estimated_money_saved = estimated_food_saved_kg * 5  # $5 per kg
        estimated_co2_reduced = estimated_food_saved_kg * 2.5  # 2.5kg CO2 per kg food
        
        return {
            'food_saved_kg': round(estimated_food_saved_kg, 1),
            'money_saved_usd': round(estimated_money_saved, 2),
            'co2_reduced_kg': round(estimated_co2_reduced, 2),
            'waste_reduction_percentage': min(round((planned_ingredient_usage / total_meals) * 100, 1), 95)
        }
    
    def calculate_meal_waste_reduction(self, meal: Dict[str, Any], available_ingredients: List[str]) -> int:
        """Calculate waste reduction potential for a single meal"""
        matches = 0
        available_lower = [ing.lower() for ing in available_ingredients]
        
        for ingredient in meal['ingredients']:
            if any(ingredient.lower() in avail.lower() or avail.lower() in ingredient.lower() 
                   for avail in available_lower):
                matches += 1
        
        return matches
    
    def get_current_season(self) -> str:
        """Determine current season"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'fall'
        else:
            return 'winter'
    
    def get_planning_tips(self) -> List[str]:
        """Get meal planning tips"""
        return [
            "Plan meals around ingredients you already have",
            "Cook larger portions and use leftovers creatively",
            "Prep ingredients in advance to save time",
            "Keep a flexible attitude - substitute similar ingredients",
            "Use seasonal produce for better flavor and lower cost",
            "Batch cook grains and proteins for the week"
        ]