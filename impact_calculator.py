"""
Impact Calculator - Calculate environmental and economic impact of food waste reduction
"""

import random
from typing import Dict, Any

class FoodWasteImpactCalculator:
    """
    Calculate real environmental and economic impact of reducing food waste
    """
    
    def __init__(self):
        # Environmental impact data (per kg of food saved)
        self.impact_data = {
            'tomato': {'water': 150, 'co2': 0.7, 'land': 0.02, 'cost': 3.50},
            'bread': {'water': 1100, 'co2': 1.2, 'land': 0.15, 'cost': 2.80},
            'cheese': {'water': 5000, 'co2': 8.9, 'land': 0.25, 'cost': 12.00},
            'chicken': {'water': 4325, 'co2': 6.9, 'land': 0.18, 'cost': 8.50},
            'beef': {'water': 15400, 'co2': 60.0, 'land': 1.25, 'cost': 18.00},
            'milk': {'water': 1000, 'co2': 3.2, 'land': 0.09, 'cost': 4.20},
            'rice': {'water': 2500, 'co2': 2.7, 'land': 0.07, 'cost': 2.10},
            'potato': {'water': 287, 'co2': 0.3, 'land': 0.03, 'cost': 1.80},
            'apple': {'water': 822, 'co2': 0.4, 'land': 0.04, 'cost': 3.20},
            'carrot': {'water': 131, 'co2': 0.2, 'land': 0.02, 'cost': 1.90},
            'onion': {'water': 272, 'co2': 0.3, 'land': 0.02, 'cost': 1.60},
            'pasta': {'water': 1850, 'co2': 1.1, 'land': 0.12, 'cost': 1.50},
            'eggs': {'water': 3300, 'co2': 4.8, 'land': 0.16, 'cost': 4.50},
            'fish': {'water': 2500, 'co2': 3.0, 'land': 0.05, 'cost': 15.00},
            'default': {'water': 1000, 'co2': 2.0, 'land': 0.05, 'cost': 3.00}
        }
        
        # Global stats for context
        self.global_stats = {
            'annual_food_waste': 1300000000,  # tonnes
            'percentage_of_production': 30,
            'people_could_feed': 3000000000,
            'economic_loss': 940000000000  # USD
        }
    
    def calculate_ingredient_impact(self, ingredient: str, weight_kg: float = 0.5) -> Dict[str, Any]:
        """Calculate impact for a single ingredient"""
        ingredient_key = ingredient.lower().strip()
        
        # Find matching impact data
        impact = self.impact_data.get(ingredient_key)
        if not impact:
            # Try partial matching
            for key in self.impact_data.keys():
                if key in ingredient_key or ingredient_key in key:
                    impact = self.impact_data[key]
                    break
            else:
                impact = self.impact_data['default']
        
        return {
            'ingredient': ingredient.title(),
            'weight_kg': weight_kg,
            'water_saved_liters': round(impact['water'] * weight_kg, 1),
            'co2_reduced_kg': round(impact['co2'] * weight_kg, 2),
            'land_saved_m2': round(impact['land'] * weight_kg, 3),
            'money_saved_usd': round(impact['cost'] * weight_kg, 2)
        }
    
    def calculate_total_impact(self, ingredients: list) -> Dict[str, Any]:
        """Calculate total impact for all ingredients"""
        total_water = 0
        total_co2 = 0
        total_land = 0
        total_money = 0
        ingredient_impacts = []
        
        for ingredient in ingredients:
            # Randomize weight slightly for realism (0.3-0.8 kg)
            weight = random.uniform(0.3, 0.8)
            impact = self.calculate_ingredient_impact(ingredient, weight)
            ingredient_impacts.append(impact)
            
            total_water += impact['water_saved_liters']
            total_co2 += impact['co2_reduced_kg']
            total_land += impact['land_saved_m2']
            total_money += impact['money_saved_usd']
        
        # Calculate equivalent impacts
        trees_equivalent = round(total_co2 / 22, 1)  # 1 tree absorbs ~22kg CO2/year
        shower_equivalent = round(total_water / 50, 0)  # 50L per shower
        meals_equivalent = round(total_money / 8, 0)  # $8 per meal
        
        return {
            'ingredients': ingredient_impacts,
            'totals': {
                'water_saved_liters': round(total_water, 1),
                'co2_reduced_kg': round(total_co2, 2),
                'land_saved_m2': round(total_land, 3),
                'money_saved_usd': round(total_money, 2)
            },
            'equivalents': {
                'trees_planted': trees_equivalent,
                'showers_saved': int(shower_equivalent),
                'meals_funded': int(meals_equivalent)
            },
            'percentage_of_goal': {
                'water': min(round((total_water / 10000) * 100, 2), 100),
                'co2': min(round((total_co2 / 100) * 100, 2), 100),
                'money': min(round((total_money / 50) * 100, 2), 100)
            }
        }
    
    def get_achievement_level(self, total_impact: Dict[str, Any]) -> Dict[str, str]:
        """Get achievement level based on impact"""
        co2_saved = total_impact['totals']['co2_reduced_kg']
        
        if co2_saved >= 50:
            return {
                'level': 'Climate Hero',
                'badge': '🌟',
                'description': 'Outstanding environmental impact!'
            }
        elif co2_saved >= 20:
            return {
                'level': 'Eco Warrior',
                'badge': '🌿',
                'description': 'Great contribution to sustainability!'
            }
        elif co2_saved >= 10:
            return {
                'level': 'Green Champion',
                'badge': '🌱',
                'description': 'Making a positive difference!'
            }
        elif co2_saved >= 5:
            return {
                'level': 'Earth Friend',
                'badge': '🌍',
                'description': 'Every action counts!'
            }
        else:
            return {
                'level': 'Getting Started',
                'badge': '🌿',
                'description': 'Keep up the good work!'
            }
    
    def get_weekly_challenge(self) -> Dict[str, str]:
        """Get a weekly sustainability challenge"""
        challenges = [
            {
                'title': 'Zero Vegetable Waste',
                'description': 'Use every part of your vegetables this week',
                'target': 'Save 10kg CO2 with vegetable scraps'
            },
            {
                'title': 'Leftover Master',
                'description': 'Transform all leftovers into new meals',
                'target': 'Create 5 new recipes from leftovers'
            },
            {
                'title': 'Storage Optimizer',
                'description': 'Perfect your food storage techniques',
                'target': 'Extend food life by 3+ days'
            },
            {
                'title': 'Portion Pro',
                'description': 'Cook exact portions to minimize waste',
                'target': 'Zero plate waste for 7 days'
            }
        ]
        
        return random.choice(challenges)