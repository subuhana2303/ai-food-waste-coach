import requests
import random
import logging
import time
from data_handler import NutritionDataHandler
from impact_calculator import FoodWasteImpactCalculator
from meal_planner import AIWeeklyMealPlanner
from recipe_engine import SmartRecipeEngine
from smart_features import SmartFoodManager, RecipePersonalizer, FoodWastePrevention, SustainabilityCoach
from fuzzywuzzy import fuzz
import re

class FoodWasteAgent:
    """
    Advanced AI Agent for Food Waste and Nutrition Coaching
    Implements sophisticated multi-step reasoning and context awareness
    """
    
    def __init__(self):
        self.nutrition_handler = NutritionDataHandler()
        self.impact_calculator = FoodWasteImpactCalculator()
        self.meal_planner = AIWeeklyMealPlanner()
        self.recipe_engine = SmartRecipeEngine()
        self.food_manager = SmartFoodManager()
        self.recipe_personalizer = RecipePersonalizer()
        self.waste_prevention = FoodWastePrevention()
        self.sustainability_coach = SustainabilityCoach()
        self.sustainability_tips = [
            "🌍 Food waste accounts for 8-10% of global greenhouse gas emissions!",
            "💧 Throwing away 1kg of beef wastes 15,000 liters of water used in production.",
            "🍞 Reducing bread waste by 10% could save 3 million slices daily worldwide.",
            "🍅 You can save up to 150 liters of water by not wasting 1kg of tomatoes.",
            "🥬 Storing leafy greens properly can extend their life by 5-7 days.",
            "🧄 One rotten onion can spoil an entire bag - always remove damaged ones first.",
            "🥕 Carrot tops are edible and nutritious - perfect for making pesto or salads!",
            "🍌 Overripe bananas are perfect for baking and contain more antioxidants.",
            "🧀 Cheese rinds can be added to soups for extra flavor instead of throwing away.",
            "🥔 Potato skins contain most of the nutrients - clean and cook them instead of peeling."
        ]
    
    def process_message(self, message, conversation_history):
        """
        Main agent processing with multi-step reasoning
        """
        try:
            # Step 1: Analyze user intent and context
            context = self._analyze_context(message, conversation_history)
            
            # Step 2: Extract and parse ingredients
            ingredients = self._parse_ingredients(message, context)
            
            # Check for special requests first
            if context['special_requests']['meal_plan'] and ingredients:
                return self._generate_meal_plan_response(ingredients)
            
            if not ingredients:
                return self._generate_help_response()
            
            # Step 3: Execute multi-step workflow
            response_parts = []
            
            # Step 3a: Search for smart recipe recommendations
            smart_recipes = self.recipe_engine.find_best_recipes(ingredients, max_recipes=3)
            if smart_recipes:
                response_parts.append(self._format_smart_recipes(smart_recipes))
            else:
                # Fallback to original recipe search
                recipes = self._search_recipes(ingredients)
                if recipes:
                    response_parts.append(self._format_recipes(recipes))
            
            # Step 3b: Get nutrition information
            nutrition_info = self._get_nutrition_info(ingredients)
            if nutrition_info:
                response_parts.append(self._format_nutrition(nutrition_info))
            
            # Step 3c: Get storage tips and preservation strategies
            storage_tips = self._get_storage_tips(ingredients)
            if storage_tips:
                response_parts.append(self._format_storage_tips(storage_tips))
            
            # Step 3d: Get preservation strategies
            preservation_strategies = self.waste_prevention.get_preservation_strategies(ingredients)
            if preservation_strategies:
                response_parts.append(self._format_preservation_strategies(preservation_strategies))
            
            # Step 4: Calculate environmental impact
            impact_analysis = self._calculate_environmental_impact(ingredients)
            if impact_analysis:
                response_parts.append(impact_analysis)
            
            # Step 5: Add sustainability insight
            sustainability_tip = random.choice(self.sustainability_tips)
            response_parts.append(f"\n💡 **Did You Know?**\n{sustainability_tip}")
            
            # Step 6: Combine and format final response
            if response_parts:
                final_response = "\n\n".join(response_parts)
                return final_response
            else:
                return self._generate_fallback_response(ingredients)
                
        except Exception as e:
            logging.error(f"Agent processing error: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again with a list of ingredients like 'tomato, bread, cheese'."
    
    def _analyze_context(self, message, history):
        """Analyze conversation context for better understanding"""
        recent_ingredients = []
        
        # Look for ingredients mentioned in recent conversation
        for entry in history[-5:]:  # Check last 5 messages
            if entry['type'] == 'user':
                parsed = self._parse_ingredients(entry['message'], None)
                recent_ingredients.extend(parsed)
        
        # Check for special requests
        message_lower = message.lower()
        special_requests = {
            'meal_plan': any(phrase in message_lower for phrase in ['meal plan', 'weekly plan', 'plan meals', 'week plan']),
            'impact_only': any(phrase in message_lower for phrase in ['impact', 'environmental', 'carbon', 'co2', 'footprint']),
            'quick_recipe': any(phrase in message_lower for phrase in ['quick', 'fast', 'easy', '5 minutes', '10 minutes'])
        }
        
        return {
            'recent_ingredients': list(set(recent_ingredients)),
            'is_follow_up': len(history) > 2,
            'special_requests': special_requests
        }
    
    def _parse_ingredients(self, message, context):
        """
        Advanced ingredient parsing with natural language understanding
        """
        # Clean the message
        message = message.lower().strip()
        
        # Remove common phrases
        cleanup_phrases = [
            "i have", "i've got", "what can i make with", "how to use",
            "recipes for", "cook with", "leftover", "leftovers"
        ]
        
        for phrase in cleanup_phrases:
            message = message.replace(phrase, "")
        
        # Split by common separators
        separators = [',', ';', '&', 'and', '\n', '  ']
        ingredients = [message]
        
        for sep in separators:
            new_ingredients = []
            for ingredient in ingredients:
                new_ingredients.extend([part.strip() for part in ingredient.split(sep)])
            ingredients = new_ingredients
        
        # Filter and clean ingredients
        cleaned_ingredients = []
        for ingredient in ingredients:
            ingredient = ingredient.strip()
            if len(ingredient) > 1 and not any(word in ingredient for word in ['please', 'help', 'can', 'how', 'what', 'make']):
                cleaned_ingredients.append(ingredient)
        
        return cleaned_ingredients[:10]  # Limit to 10 ingredients
    
    def _search_recipes(self, ingredients):
        """Search for recipes using Recipe Puppy API"""
        try:
            # Use first 3 ingredients for better API results
            search_ingredients = ",".join(ingredients[:3])
            
            url = "http://www.recipepuppy.com/api/"
            params = {
                'i': search_ingredients,
                'p': 1  # First page
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                recipes = data.get('results', [])
                
                # Filter and limit to 4 best recipes
                valid_recipes = []
                for recipe in recipes:
                    if recipe.get('title') and recipe.get('href'):
                        valid_recipes.append(recipe)
                        if len(valid_recipes) >= 4:
                            break
                
                return valid_recipes
            
        except Exception as e:
            logging.error(f"Recipe search error: {str(e)}")
        
        return []
    
    def _get_nutrition_info(self, ingredients):
        """Get nutrition information for ingredients"""
        nutrition_data = []
        
        for ingredient in ingredients:
            info = self.nutrition_handler.get_nutrition_info(ingredient)
            if info:
                nutrition_data.append({
                    'ingredient': ingredient.title(),
                    'data': info
                })
        
        return nutrition_data
    
    def _get_storage_tips(self, ingredients):
        """Get storage tips for ingredients"""
        storage_data = []
        
        for ingredient in ingredients:
            tip = self.nutrition_handler.get_storage_tip(ingredient)
            if tip:
                storage_data.append({
                    'ingredient': ingredient.title(),
                    'tip': tip
                })
        
        return storage_data
    
    def _calculate_environmental_impact(self, ingredients):
        """Calculate and format environmental impact"""
        try:
            impact_data = self.impact_calculator.calculate_total_impact(ingredients)
            achievement = self.impact_calculator.get_achievement_level(impact_data)
            
            formatted = f"\n🌍 **Environmental Impact Analysis:**\n\n"
            
            # Total impact
            totals = impact_data['totals']
            formatted += f"**Your Waste Reduction Impact:**\n"
            formatted += f"💧 Water Saved: {totals['water_saved_liters']} liters\n"
            formatted += f"🌱 CO₂ Reduced: {totals['co2_reduced_kg']} kg\n"
            formatted += f"💰 Money Saved: ${totals['money_saved_usd']}\n\n"
            
            # Fun equivalents
            equivalents = impact_data['equivalents']
            formatted += f"**That's equivalent to:**\n"
            formatted += f"🚿 {equivalents['showers_saved']} shower(s) worth of water\n"
            formatted += f"🌳 Planting {equivalents['trees_planted']} tree(s)\n"
            formatted += f"🍽️ Funding {equivalents['meals_funded']} meal(s) for someone in need\n\n"
            
            # Achievement
            formatted += f"**Achievement Unlocked:** {achievement['badge']} {achievement['level']}\n"
            formatted += f"*{achievement['description']}*"
            
            return formatted
            
        except Exception as e:
            logging.error(f"Error calculating environmental impact: {str(e)}")
            return None
    
    def _format_recipes(self, recipes):
        """Format recipe results with professional styling"""
        if not recipes:
            return ""
        
        formatted = "🍳 **Recipes You Can Try:**\n"
        
        for i, recipe in enumerate(recipes, 1):
            title = recipe.get('title', 'Untitled Recipe')
            ingredients_list = recipe.get('ingredients', 'N/A')
            link = recipe.get('href', '#')
            
            # Clean up ingredients list
            if ingredients_list and ingredients_list != 'N/A':
                ingredients_list = ingredients_list.replace(',', ', ')
                if len(ingredients_list) > 80:
                    ingredients_list = ingredients_list[:80] + "..."
            
            formatted += f"{i}. **{title}**\n"
            formatted += f"   *Ingredients: {ingredients_list}*\n"
            formatted += f"   [📖 View Recipe]({link})\n\n"
        
        return formatted.strip()
    
    def _format_nutrition(self, nutrition_data):
        """Format nutrition information in a clean table"""
        if not nutrition_data:
            return ""
        
        formatted = "🥗 **Nutrition Facts (per 100g):**\n\n"
        
        for item in nutrition_data:
            ingredient = item['ingredient']
            data = item['data']
            
            formatted += f"**{ingredient}**: "
            formatted += f"{data['calories']} kcal, "
            formatted += f"{data['protein']}g protein, "
            formatted += f"{data['carbs']}g carbs, "
            formatted += f"{data['fat']}g fat\n"
        
        return formatted.strip()
    
    def _format_storage_tips(self, storage_data):
        """Format storage tips with clear organization"""
        if not storage_data:
            return ""
        
        formatted = "📦 **Storage Tips:**\n\n"
        
        for item in storage_data:
            ingredient = item['ingredient']
            tip = item['tip']
            formatted += f"**{ingredient}**: {tip}\n"
        
        return formatted.strip()
    
    def _generate_help_response(self):
        """Generate helpful response when no ingredients are detected"""
        return """👋 **Hello! I'm your AI Food Waste and Nutrition Coach!**

I help you reduce food waste and improve nutrition by finding recipes for your leftover ingredients.

**How to use me:**
- List your ingredients separated by commas (e.g., "tomato, bread, cheese")
- I'll find recipes, provide nutrition facts, and give storage tips
- Ask follow-up questions about specific ingredients or cooking methods

**Try saying:**
- "tomato, onion, garlic"
- "leftover chicken, rice, vegetables"
- "bread, eggs, milk"

What ingredients do you have available? 🥬🍅🧄"""
    
    def _generate_fallback_response(self, ingredients):
        """Generate fallback response when APIs fail"""
        tip = random.choice(self.sustainability_tips)
        
        return f"""I apologize, but I'm having trouble accessing recipe data right now. However, I can still help you reduce food waste!

**Your ingredients:** {', '.join(ingredients)}

**General cooking tips:**
- These ingredients can likely be used in stir-fries, soups, or salads
- Try combining them with basic pantry staples like rice, pasta, or bread
- Most fresh ingredients can be sautéed together with garlic and olive oil

💡 **Did You Know?**
{tip}

Please try again in a moment, or ask me about specific ingredients for storage tips!"""
    
    def _generate_meal_plan_response(self, ingredients):
        """Generate weekly meal plan response"""
        try:
            meal_plan = self.meal_planner.generate_weekly_plan(ingredients)
            
            formatted = "📅 **Your Personalized Weekly Meal Plan**\n\n"
            
            # Show a few days of the plan
            plan_days = list(meal_plan['weekly_plan'].items())[:3]  # Show first 3 days
            
            for day_name, day_data in plan_days:
                formatted += f"**{day_name}** ({day_data['date']}):\n"
                for meal_type, meal_info in day_data['meals'].items():
                    formatted += f"• {meal_type.title()}: {meal_info['name']} ({meal_info['prep_time']} min)\n"
                formatted += f"💡 *{day_data['daily_tip']}*\n\n"
            
            # Shopping list
            if meal_plan['shopping_list']:
                formatted += "🛒 **Smart Shopping List:**\n"
                for category, items in meal_plan['shopping_list'].items():
                    if items:
                        formatted += f"**{category.title()}:** {', '.join(items)}\n"
                formatted += "\n"
            
            # Waste reduction potential
            waste_reduction = meal_plan['waste_reduction']
            formatted += f"🌱 **Waste Reduction Potential:**\n"
            formatted += f"• Food Saved: {waste_reduction['food_saved_kg']} kg\n"
            formatted += f"• Money Saved: ${waste_reduction['money_saved_usd']}\n"
            formatted += f"• CO₂ Reduced: {waste_reduction['co2_reduced_kg']} kg\n"
            formatted += f"• Waste Reduction: {waste_reduction['waste_reduction_percentage']}%\n\n"
            
            # Planning tips
            formatted += "📋 **Pro Tips:**\n"
            for tip in meal_plan['planning_tips'][:3]:
                formatted += f"• {tip}\n"
            
            # Challenge
            challenge = self.impact_calculator.get_weekly_challenge()
            formatted += f"\n🏆 **This Week's Challenge:** {challenge['title']}\n"
            formatted += f"*{challenge['description']}*\n"
            formatted += f"**Target:** {challenge['target']}"
            
            return formatted
            
        except Exception as e:
            logging.error(f"Error generating meal plan: {str(e)}")
            return "I apologize, but I encountered an error generating your meal plan. Please try again with your available ingredients."
    
    def _format_smart_recipes(self, recipes):
        """Format smart recipe recommendations"""
        if not recipes:
            return None
        
        formatted = "👨‍🍳 **Smart Recipe Recommendations:**\n\n"
        
        for i, recipe in enumerate(recipes, 1):
            formatted += f"**{i}. {recipe['name']}** ⭐ {recipe['match_score']}% Match\n"
            formatted += f"🍽️ *{recipe['cuisine'].title()} Cuisine*\n"
            formatted += f"⏱️ Prep Time: {recipe['prep_time']} minutes | Difficulty: {recipe['difficulty']}\n\n"
            
            # Show ingredients you have
            available_ingredients = [ing for ing in recipe['ingredients'] 
                                   if ing.replace('_', ' ').title() not in recipe.get('missing_ingredients', [])]
            if available_ingredients:
                formatted += f"✅ **You have:** {', '.join([ing.replace('_', ' ').title() for ing in available_ingredients])}\n"
            
            # Show missing ingredients
            if recipe.get('missing_ingredients'):
                formatted += f"🛒 **Need to buy:** {', '.join(recipe['missing_ingredients'])}\n"
            
            formatted += "\n**Instructions:**\n"
            for step_num, instruction in enumerate(recipe['instructions'], 1):
                formatted += f"{step_num}. {instruction}\n"
            
            # Add cooking tips
            tips = self.recipe_engine.get_cooking_tips(recipe)
            if tips:
                formatted += f"\n💡 **Pro Tips:**\n"
                for tip in tips[:2]:  # Show top 2 tips
                    formatted += f"• {tip}\n"
            
            formatted += f"\n🌱 **Waste Reduction Score:** {recipe.get('waste_reduction_score', 0)}%\n"
            formatted += "---\n\n"
        
        return formatted.rstrip("---\n\n")
    
    def _format_preservation_strategies(self, strategies):
        """Format preservation strategies"""
        if not strategies:
            return None
        
        formatted = "🥫 **Food Preservation Strategies:**\n\n"
        
        for ingredient, methods in strategies.items():
            formatted += f"**{ingredient.title()}:**\n"
            for method in methods[:3]:  # Show top 3 methods
                formatted += f"• {method}\n"
            formatted += "\n"
        
        return formatted
