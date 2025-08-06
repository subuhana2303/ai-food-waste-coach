from flask import render_template, request, jsonify, session
from app import app
from agent import FoodWasteAgent
import logging

# Initialize the AI agent
agent = FoodWasteAgent()

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Please enter some ingredients or ask a question!'
            }), 400
        
        # Get or initialize conversation history
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        # Add user message to history
        session['conversation_history'].append({
            'type': 'user',
            'message': user_message
        })
        
        # Process message with agent
        agent_response = agent.process_message(user_message, session['conversation_history'])
        
        # Add agent response to history
        session['conversation_history'].append({
            'type': 'agent',
            'message': agent_response
        })
        
        # Save session
        session.permanent = True
        
        return jsonify({
            'success': True,
            'response': agent_response
        })
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error. Please try again!'
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    try:
        session['conversation_history'] = []
        return jsonify({
            'success': True,
            'message': 'Chat history cleared successfully!'
        })
    except Exception as e:
        logging.error(f"Error clearing chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear chat history'
        }), 500

@app.route('/api/status')
def status():
    """Check API status"""
    return jsonify({
        'success': True,
        'status': 'AI Food Waste and Nutrition Coach is running!',
        'version': '2.0.0',
        'features': [
            'AI Agent with Multi-step Reasoning',
            'Environmental Impact Calculator',
            'Weekly Meal Planning',
            'Smart Recipe Discovery',
            'Nutrition Analysis',
            'Storage Optimization',
            'Sustainability Tracking'
        ]
    })

@app.route('/api/meal-plan', methods=['POST'])
def generate_meal_plan():
    """Generate weekly meal plan endpoint"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'Please provide a list of ingredients'
            }), 400
        
        # Use agent to generate meal plan
        meal_plan_response = agent.process_message(f"meal plan for {', '.join(ingredients)}", [])
        
        return jsonify({
            'success': True,
            'meal_plan': meal_plan_response
        })
        
    except Exception as e:
        logging.error(f"Error in meal plan endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate meal plan'
        }), 500

@app.route('/api/impact', methods=['POST'])
def calculate_impact():
    """Calculate environmental impact endpoint"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'Please provide a list of ingredients'
            }), 400
        
        from impact_calculator import FoodWasteImpactCalculator
        calculator = FoodWasteImpactCalculator()
        
        impact_data = calculator.calculate_total_impact(ingredients)
        achievement = calculator.get_achievement_level(impact_data)
        challenge = calculator.get_weekly_challenge()
        
        return jsonify({
            'success': True,
            'impact': impact_data,
            'achievement': achievement,
            'challenge': challenge
        })
        
    except Exception as e:
        logging.error(f"Error in impact endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to calculate impact'
        }), 500

@app.route('/api/smart-recipes', methods=['POST'])
def get_smart_recipes():
    """Get smart recipe recommendations endpoint"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        cuisine_preference = data.get('cuisine', None)
        dietary_preferences = data.get('dietary_preferences', [])
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'Please provide a list of ingredients'
            }), 400
        
        from recipe_engine import SmartRecipeEngine
        from smart_features import RecipePersonalizer
        
        recipe_engine = SmartRecipeEngine()
        personalizer = RecipePersonalizer()
        
        # Get recipe recommendations
        if cuisine_preference:
            recipes = recipe_engine.get_recipe_suggestions_by_cuisine(ingredients)
            recipe_list = recipes.get(cuisine_preference.lower(), [])
        else:
            recipe_list = recipe_engine.find_best_recipes(ingredients, max_recipes=5)
        
        # Personalize recipes based on dietary preferences
        if dietary_preferences:
            for recipe in recipe_list:
                recipe = personalizer.personalize_recipe(recipe, dietary_preferences)
        
        # Get creative combinations
        creative_recipes = recipe_engine.generate_creative_combinations(ingredients)
        
        return jsonify({
            'success': True,
            'recipes': recipe_list,
            'creative_combinations': creative_recipes,
            'total_recipes': len(recipe_list)
        })
        
    except Exception as e:
        logging.error(f"Error in smart recipes endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get recipe recommendations'
        }), 500

@app.route('/api/expiration-tracker', methods=['POST'])
def track_expiration():
    """Track ingredient expiration dates"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        storage_location = data.get('storage_location', 'fridge')
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'Please provide a list of ingredients'
            }), 400
        
        from smart_features import SmartFoodManager
        food_manager = SmartFoodManager()
        
        expiration_data = []
        for ingredient in ingredients:
            prediction = food_manager.predict_expiration(ingredient, storage_location)
            expiration_data.append(prediction)
        
        # Sort by urgency (days remaining)
        expiration_data.sort(key=lambda x: x['days_remaining'])
        
        return jsonify({
            'success': True,
            'expiration_predictions': expiration_data,
            'urgent_items': [item for item in expiration_data if item['days_remaining'] <= 3]
        })
        
    except Exception as e:
        logging.error(f"Error in expiration tracker endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to track expiration dates'
        }), 500

@app.route('/api/sustainability-tip', methods=['GET'])
def get_sustainability_tip():
    """Get daily sustainability tip"""
    try:
        from smart_features import SustainabilityCoach
        coach = SustainabilityCoach()
        
        tip = coach.get_daily_sustainability_tip()
        
        return jsonify({
            'success': True,
            'tip': tip
        })
        
    except Exception as e:
        logging.error(f"Error getting sustainability tip: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get sustainability tip'
        }), 500
