/**
 * Premium AI Food Waste Coach - Frontend Application
 * Enterprise-grade JavaScript with sophisticated interactions
 */

class FoodWasteCoach {
    constructor() {
        this.isLoading = false;
        this.messageCount = 0;
        this.initializeApp();
    }

    /**
     * Initialize the application with event listeners and setup
     */
    initializeApp() {
        // Initialize AOS (Animate On Scroll)
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });

        // Set up event listeners
        this.setupEventListeners();
        
        // Focus on input field
        this.focusInput();
        
        // Add welcome animation
        this.animateWelcome();
        
        console.log('🚀 AI Food Waste Coach initialized successfully');
        
        // Add dynamic effects
        addDynamicEffects();
    }

    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        // Form submission
        document.querySelector('.input-form').addEventListener('submit', (e) => {
            this.sendMessage(e);
        });
        
        // Enter key support
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage(e);
            }
        });
        
        // Input field enhancements
        messageInput.addEventListener('focus', () => {
            this.onInputFocus();
        });
        
        messageInput.addEventListener('blur', () => {
            this.onInputBlur();
        });
        
        // Auto-resize chat on window resize
        window.addEventListener('resize', () => {
            this.adjustChatHeight();
        });
    }

    /**
     * Handle message sending with validation and API communication
     */
    async sendMessage(event) {
        event.preventDefault();
        
        if (this.isLoading) return;
        
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) {
            this.showInputError('Please enter some ingredients!');
            return;
        }
        
        // Add user message to chat
        this.addUserMessage(message);
        
        // Clear input and show loading state
        messageInput.value = '';
        this.setLoadingState(true);
        
        try {
            // Show agent status
            this.showAgentStatus('Analyzing your ingredients...');
            
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Simulate processing steps for better UX
                await this.simulateProcessingSteps();
                
                // Add agent response
                this.addAgentMessage(data.response);
            } else {
                this.addAgentMessage(
                    `❌ **Sorry, I encountered an error:**\n\n${data.error}\n\nPlease try again with a list of ingredients like "tomato, bread, cheese".`
                );
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addAgentMessage(
                '❌ **Connection Error**\n\nI\'m having trouble connecting to my services. Please check your internet connection and try again.'
            );
        } finally {
            this.setLoadingState(false);
            this.hideAgentStatus();
            this.focusInput();
        }
    }

    /**
     * Simulate processing steps for enhanced user experience
     */
    async simulateProcessingSteps() {
        const steps = [
            'Parsing ingredients...',
            'Searching for recipes...',
            'Loading nutrition data...',
            'Preparing recommendations...'
        ];
        
        for (let i = 0; i < steps.length; i++) {
            this.showAgentStatus(steps[i]);
            await this.sleep(800);
        }
    }

    /**
     * Add user message to chat
     */
    addUserMessage(message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageTime = this.getCurrentTime();
        
        const messageHTML = `
            <div class="message-container user-message" data-aos="fade-left">
                <div class="message-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="message-bubble user-bubble">
                    <div class="message-content">
                        ${this.escapeHtml(message)}
                    </div>
                    <div class="message-time">${messageTime}</div>
                </div>
            </div>
        `;
        
        chatMessages.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
        this.messageCount++;
        
        // Refresh AOS for new elements
        AOS.refresh();
    }

    /**
     * Add agent message to chat with markdown parsing
     */
    addAgentMessage(message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageTime = this.getCurrentTime();
        
        // Parse markdown-style formatting
        const formattedMessage = this.parseMarkdown(message);
        
        const messageHTML = `
            <div class="message-container agent-message" data-aos="fade-right">
                <div class="message-avatar">
                    <i class="fas fa-seedling"></i>
                </div>
                <div class="message-bubble agent-bubble">
                    <div class="message-content">
                        ${formattedMessage}
                    </div>
                    <div class="message-time">${messageTime}</div>
                </div>
            </div>
        `;
        
        chatMessages.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
        this.messageCount++;
        
        // Refresh AOS for new elements
        AOS.refresh();
        
        // Add typing animation effect
        this.animateTyping(chatMessages.lastElementChild);
    }

    /**
     * Parse markdown-style formatting for agent messages
     */
    parseMarkdown(text) {
        // Escape HTML first
        text = this.escapeHtml(text);
        
        // Bold text **text**
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Links [text](url)
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Line breaks
        text = text.replace(/\n/g, '<br>');
        
        // List items starting with - or numbers
        text = text.replace(/^[\-\*]\s+(.+)$/gm, '<li>$1</li>');
        text = text.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
        
        // Wrap consecutive list items in ul tags
        text = text.replace(/(<li>.*<\/li>)/gs, (match) => {
            if (!match.includes('<ul>')) {
                return '<ul>' + match + '</ul>';
            }
            return match;
        });
        
        return text;
    }

    /**
     * Show agent status with typing indicator
     */
    showAgentStatus(statusText) {
        const agentStatus = document.getElementById('agentStatus');
        const statusTextElement = agentStatus.querySelector('.status-text');
        
        statusTextElement.textContent = statusText;
        agentStatus.style.display = 'block';
        
        // Animate in
        setTimeout(() => {
            agentStatus.style.opacity = '1';
            agentStatus.style.transform = 'translateY(0)';
        }, 100);
    }

    /**
     * Hide agent status
     */
    hideAgentStatus() {
        const agentStatus = document.getElementById('agentStatus');
        agentStatus.style.opacity = '0';
        agentStatus.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            agentStatus.style.display = 'none';
        }, 300);
    }

    /**
     * Set loading state for UI elements
     */
    setLoadingState(loading) {
        this.isLoading = loading;
        const sendButton = document.getElementById('sendButton');
        const messageInput = document.getElementById('messageInput');
        const chatContainer = document.querySelector('.chat-container');
        
        if (loading) {
            sendButton.disabled = true;
            sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            messageInput.disabled = true;
            chatContainer.classList.add('loading');
        } else {
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
            messageInput.disabled = false;
            chatContainer.classList.remove('loading');
        }
    }

    /**
     * Scroll chat to bottom with smooth animation
     */
    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        const scrollOptions = {
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        };
        
        chatMessages.scrollTo(scrollOptions);
    }

    /**
     * Focus on input field
     */
    focusInput() {
        setTimeout(() => {
            const messageInput = document.getElementById('messageInput');
            messageInput.focus();
        }, 100);
    }

    /**
     * Handle input focus
     */
    onInputFocus() {
        const inputGroup = document.querySelector('.input-group');
        inputGroup.style.transform = 'scale(1.02)';
        inputGroup.style.boxShadow = '0 5px 15px rgba(102, 126, 234, 0.3)';
    }

    /**
     * Handle input blur
     */
    onInputBlur() {
        const inputGroup = document.querySelector('.input-group');
        inputGroup.style.transform = 'scale(1)';
        inputGroup.style.boxShadow = 'none';
    }

    /**
     * Show input error with animation
     */
    showInputError(message) {
        const messageInput = document.getElementById('messageInput');
        const originalPlaceholder = messageInput.placeholder;
        
        messageInput.style.borderColor = '#ef4444';
        messageInput.placeholder = message;
        messageInput.classList.add('shake');
        
        setTimeout(() => {
            messageInput.style.borderColor = '';
            messageInput.placeholder = originalPlaceholder;
            messageInput.classList.remove('shake');
        }, 3000);
    }

    /**
     * Animate welcome message
     */
    animateWelcome() {
        const welcomeMessage = document.querySelector('.agent-message');
        if (welcomeMessage) {
            welcomeMessage.style.opacity = '0';
            welcomeMessage.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                welcomeMessage.style.transition = 'all 0.8s ease';
                welcomeMessage.style.opacity = '1';
                welcomeMessage.style.transform = 'translateY(0)';
            }, 500);
        }
    }

    /**
     * Animate typing effect for new messages
     */
    animateTyping(messageElement) {
        const content = messageElement.querySelector('.message-content');
        const originalHTML = content.innerHTML;
        
        content.innerHTML = '';
        content.style.opacity = '1';
        
        // Simulate typing
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < originalHTML.length) {
                content.innerHTML = originalHTML.substring(0, i + 1);
                i++;
            } else {
                clearInterval(typeInterval);
            }
        }, 10);
    }

    /**
     * Adjust chat height for responsive design
     */
    adjustChatHeight() {
        const chatMessages = document.getElementById('chatMessages');
        const windowHeight = window.innerHeight;
        const headerHeight = document.querySelector('.header-premium').offsetHeight;
        const inputHeight = document.querySelector('.chat-input').offsetHeight;
        const maxChatHeight = windowHeight - headerHeight - inputHeight - 200;
        
        if (maxChatHeight > 300) {
            chatMessages.style.maxHeight = maxChatHeight + 'px';
        }
    }

    /**
     * Utility function for sleep/delay
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Get current time formatted
     */
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    /**
     * Escape HTML characters
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for HTML event handlers
let app;

/**
 * Send message (called from HTML)
 */
function sendMessage(event) {
    if (app) {
        app.sendMessage(event);
    }
}

/**
 * Quick input function
 */
function quickInput(text) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = text;
    messageInput.focus();
    
    // Add highlight effect
    messageInput.style.background = 'linear-gradient(45deg, #667eea, #764ba2)';
    messageInput.style.color = 'white';
    
    setTimeout(() => {
        messageInput.style.background = '';
        messageInput.style.color = '';
    }, 1000);
}

/**
 * Show impact dashboard
 */
async function showImpactDashboard() {
    const modal = new bootstrap.Modal(document.getElementById('impactModal'));
    modal.show();
    
    // Load sample impact data
    const sampleIngredients = ['tomato', 'bread', 'chicken', 'rice', 'cheese'];
    
    try {
        const response = await fetch('/api/impact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ingredients: sampleIngredients })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderImpactDashboard(data);
        } else {
            document.getElementById('impactDashboardContent').innerHTML = 
                '<div class="alert alert-danger">Failed to load impact data</div>';
        }
    } catch (error) {
        console.error('Error loading impact dashboard:', error);
        document.getElementById('impactDashboardContent').innerHTML = 
            '<div class="alert alert-danger">Error loading impact data</div>';
    }
}

/**
 * Render impact dashboard
 */
function renderImpactDashboard(data) {
    const { impact, achievement, challenge } = data;
    
    const content = `
        <div class="impact-dashboard">
            <div class="achievement-badge">
                <i class="fas fa-trophy"></i>
                ${achievement.level} - ${achievement.description}
            </div>
            
            <div class="row sustainability-stats">
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-icon" style="color: #3b82f6;">💧</div>
                        <div class="stat-value" style="color: #3b82f6;">${impact.totals.water_saved_liters}L</div>
                        <div class="stat-label">Water Saved</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-icon" style="color: #10b981;">🌱</div>
                        <div class="stat-value" style="color: #10b981;">${impact.totals.co2_reduced_kg}kg</div>
                        <div class="stat-label">CO₂ Reduced</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-icon" style="color: #f59e0b;">💰</div>
                        <div class="stat-value" style="color: #f59e0b;">$${impact.totals.money_saved_usd}</div>
                        <div class="stat-label">Money Saved</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-icon" style="color: #8b5cf6;">🌍</div>
                        <div class="stat-value" style="color: #8b5cf6;">${impact.equivalents.trees_planted}</div>
                        <div class="stat-label">Trees Planted Equivalent</div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="fas fa-chart-bar"></i> Progress Towards Goals</h6>
                    <div class="progress-container">
                        <div class="progress-label">
                            <span>Water Conservation</span>
                            <span>${impact.percentage_of_goal.water}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" style="width: ${impact.percentage_of_goal.water}%"></div>
                        </div>
                    </div>
                    <div class="progress-container">
                        <div class="progress-label">
                            <span>Carbon Reduction</span>
                            <span>${impact.percentage_of_goal.co2}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" style="width: ${impact.percentage_of_goal.co2}%"></div>
                        </div>
                    </div>
                    <div class="progress-container">
                        <div class="progress-label">
                            <span>Cost Savings</span>
                            <span>${impact.percentage_of_goal.money}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" style="width: ${impact.percentage_of_goal.money}%"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <h6><i class="fas fa-trophy"></i> This Week's Challenge</h6>
                    <div class="challenge-card">
                        <h5>${challenge.title}</h5>
                        <p>${challenge.description}</p>
                        <strong>Target: ${challenge.target}</strong>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('impactDashboardContent').innerHTML = content;
}

/**
 * Show meal planner
 */
function showMealPlanner() {
    const modal = new bootstrap.Modal(document.getElementById('mealPlanModal'));
    modal.show();
}

/**
 * Generate meal plan
 */
async function generateMealPlan() {
    const ingredients = document.getElementById('ingredientsInput').value.trim();
    
    if (!ingredients) {
        alert('Please enter some ingredients first!');
        return;
    }
    
    const contentDiv = document.getElementById('mealPlanContent');
    contentDiv.innerHTML = '<div class="loading-spinner"><div class="spinner-border text-primary"></div></div>';
    
    try {
        const ingredientList = ingredients.split(',').map(ing => ing.trim());
        
        const response = await fetch('/api/meal-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ingredients: ingredientList })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderMealPlan(data.meal_plan);
        } else {
            contentDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error generating meal plan:', error);
        contentDiv.innerHTML = '<div class="alert alert-danger">Error generating meal plan</div>';
    }
}

/**
 * Render meal plan
 */
function renderMealPlan(mealPlanText) {
    // Convert the text response to HTML format
    const formattedPlan = mealPlanText
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/•/g, '<li style="list-style: none;">•')
        .replace(/📅|🛒|🌱|📋|🏆/g, '<i class="fas fa-star text-warning"></i>');
    
    document.getElementById('mealPlanContent').innerHTML = `
        <div class="meal-plan-result">
            ${formattedPlan}
        </div>
    `;
}

/**
 * Show sustainability stats
 */
function showSustainabilityStats() {
    const statsModal = `
        <div class="sustainability-overview">
            <h4><i class="fas fa-globe-americas"></i> Global Food Waste Impact</h4>
            <div class="row">
                <div class="col-md-4">
                    <div class="impact-metric">
                        <div class="metric-icon">🌍</div>
                        <div class="metric-value">1.3B</div>
                        <div class="metric-label">Tonnes wasted annually</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="impact-metric">
                        <div class="metric-icon">👥</div>
                        <div class="metric-value">3B</div>
                        <div class="metric-label">People could be fed</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="impact-metric">
                        <div class="metric-icon">💰</div>
                        <div class="metric-value">$940B</div>
                        <div class="metric-label">Economic loss (USD)</div>
                    </div>
                </div>
            </div>
            <p class="text-center mt-3"><strong>You're making a difference!</strong> Every ingredient saved contributes to solving this global challenge.</p>
        </div>
    `;
    
    // Add to a message bubble
    if (app) {
        app.addAgentMessage(statsModal);
    }
}

/**
 * Show smart recipes modal
 */
function showSmartRecipes() {
    const modal = new bootstrap.Modal(document.getElementById('smartRecipesModal'));
    modal.show();
}

/**
 * Get smart recipe recommendations
 */
async function getSmartRecipes() {
    const ingredients = document.getElementById('smartRecipesInput').value.trim();
    const cuisine = document.getElementById('cuisineSelect').value;
    
    // Get dietary preferences
    const dietaryPreferences = [];
    if (document.getElementById('veganCheck').checked) dietaryPreferences.push('vegan');
    if (document.getElementById('glutenCheck').checked) dietaryPreferences.push('gluten_free');
    if (document.getElementById('dairyCheck').checked) dietaryPreferences.push('dairy_free');
    if (document.getElementById('ketoCheck').checked) dietaryPreferences.push('keto');
    
    if (!ingredients) {
        alert('Please enter some ingredients first!');
        return;
    }
    
    const contentDiv = document.getElementById('smartRecipesContent');
    contentDiv.innerHTML = '<div class="loading-spinner"><div class="spinner-border text-primary"></div></div>';
    
    try {
        const ingredientList = ingredients.split(',').map(ing => ing.trim());
        
        const response = await fetch('/api/smart-recipes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                ingredients: ingredientList,
                cuisine: cuisine,
                dietary_preferences: dietaryPreferences
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderSmartRecipes(data);
        } else {
            contentDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error getting smart recipes:', error);
        contentDiv.innerHTML = '<div class="alert alert-danger">Error getting recipe recommendations</div>';
    }
}

/**
 * Render smart recipes
 */
function renderSmartRecipes(data) {
    const { recipes, creative_combinations } = data;
    
    let content = '<div class="smart-recipes-results">';
    
    if (recipes && recipes.length > 0) {
        content += '<h6><i class="fas fa-star"></i> Perfect Matches</h6>';
        
        recipes.forEach((recipe, index) => {
            content += `
                <div class="recipe-card mb-3">
                    <div class="recipe-header">
                        <h6>${recipe.name} <span class="badge bg-success">${recipe.match_score}% match</span></h6>
                        <small class="text-muted">${recipe.cuisine} • ${recipe.prep_time} min • ${recipe.difficulty}</small>
                    </div>
                    <div class="recipe-body">
                        <strong>Instructions:</strong>
                        <ol class="small">
                            ${recipe.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                        </ol>
                        ${recipe.missing_ingredients && recipe.missing_ingredients.length > 0 ? 
                            `<div class="mt-2"><strong>Need to buy:</strong> <span class="text-warning">${recipe.missing_ingredients.join(', ')}</span></div>` : 
                            '<div class="mt-2"><span class="text-success">✅ You have all ingredients!</span></div>'
                        }
                    </div>
                </div>
            `;
        });
    }
    
    if (creative_combinations && creative_combinations.length > 0) {
        content += '<h6 class="mt-4"><i class="fas fa-lightbulb"></i> Creative Ideas</h6>';
        
        creative_combinations.forEach(combo => {
            content += `
                <div class="creative-combo-card mb-2">
                    <h6>${combo.name}</h6>
                    <p class="small">${combo.description}</p>
                    <small class="text-muted">Est. prep time: ${combo.estimated_prep_time} min • Creativity: ${combo.creativity_score}%</small>
                </div>
            `;
        });
    }
    
    content += '</div>';
    
    document.getElementById('smartRecipesContent').innerHTML = content;
}

/**
 * Show expiration tracker modal
 */
function showExpirationTracker() {
    const modal = new bootstrap.Modal(document.getElementById('expirationModal'));
    modal.show();
}

/**
 * Track ingredient expiration
 */
async function trackExpiration() {
    const ingredients = document.getElementById('expirationInput').value.trim();
    const storageLocation = document.getElementById('storageSelect').value;
    
    if (!ingredients) {
        alert('Please enter some ingredients to track!');
        return;
    }
    
    const contentDiv = document.getElementById('expirationContent');
    contentDiv.innerHTML = '<div class="loading-spinner"><div class="spinner-border text-warning"></div></div>';
    
    try {
        const ingredientList = ingredients.split(',').map(ing => ing.trim());
        
        const response = await fetch('/api/expiration-tracker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                ingredients: ingredientList,
                storage_location: storageLocation
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderExpirationData(data);
        } else {
            contentDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error tracking expiration:', error);
        contentDiv.innerHTML = '<div class="alert alert-danger">Error tracking expiration dates</div>';
    }
}

/**
 * Render expiration tracking data
 */
function renderExpirationData(data) {
    const { expiration_predictions, urgent_items } = data;
    
    let content = '<div class="expiration-results">';
    
    if (urgent_items && urgent_items.length > 0) {
        content += '<div class="alert alert-warning"><strong>⚠️ Use Soon:</strong> ';
        content += urgent_items.map(item => item.ingredient).join(', ');
        content += '</div>';
    }
    
    content += '<h6><i class="fas fa-list"></i> Expiration Timeline</h6>';
    
    expiration_predictions.forEach(prediction => {
        const urgencyClass = prediction.days_remaining <= 1 ? 'danger' : 
                           prediction.days_remaining <= 3 ? 'warning' : 'success';
        
        content += `
            <div class="expiration-item mb-3 border-start border-${urgencyClass} border-3 ps-3">
                <div class="d-flex justify-content-between align-items-center">
                    <strong>${prediction.ingredient}</strong>
                    <span class="badge bg-${urgencyClass}">${prediction.days_remaining} days</span>
                </div>
                <small class="text-muted">Expires: ${prediction.expiration_date}</small>
                <div class="mt-1">
                    <small><strong>Storage tips:</strong></small>
                    <ul class="small mb-0">
                        ${prediction.storage_tips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
                <div class="mt-1">
                    <small><strong>Watch for:</strong> ${prediction.spoilage_signs.join(', ')}</small>
                </div>
            </div>
        `;
    });
    
    content += '</div>';
    
    document.getElementById('expirationContent').innerHTML = content;
}

/**
 * Add dynamic effects to make the site more interactive
 */
function addDynamicEffects() {
    // Add floating animation to quick cards with dynamic offset tracking
    const quickCards = document.querySelectorAll('.quick-card');
    quickCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('floating');
        
        // Track floating offset for mouse parallax
        let floatOffset = 0;
        const updateFloatOffset = () => {
            const rect = card.getBoundingClientRect();
            const computedStyle = window.getComputedStyle(card);
            const transform = computedStyle.transform;
            
            if (transform && transform !== 'none') {
                const matrix = new DOMMatrix(transform);
                floatOffset = matrix.m42; // translateY value
            }
            
            card.dataset.floatOffset = floatOffset;
            requestAnimationFrame(updateFloatOffset);
        };
        
        updateFloatOffset();
    });
    
    // Add pulse effect to status indicator
    const statusIndicator = document.querySelector('.status-indicator');
    if (statusIndicator) {
        statusIndicator.classList.add('pulse-effect');
    }
    
    // Add parallax effect to header and dynamic scrolling
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const header = document.querySelector('.header-premium');
        const chatContainer = document.querySelector('.chat-container');
        
        if (header) {
            header.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
        
        // Add dynamic transform to chat container based on scroll
        if (chatContainer) {
            const rect = chatContainer.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                const progress = Math.max(0, Math.min(1, (window.innerHeight - rect.top) / window.innerHeight));
                chatContainer.style.transform = `scale(${0.95 + progress * 0.05}) translateY(${(1 - progress) * 20}px)`;
            }
        }
    });
    
    // Add mouse movement parallax
    document.addEventListener('mousemove', (e) => {
        const cards = document.querySelectorAll('.quick-card');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        cards.forEach((card, index) => {
            const intensity = (index + 1) * 2;
            const xOffset = (mouseX - 0.5) * intensity;
            const yOffset = (mouseY - 0.5) * intensity;
            
            card.style.transform = `translate(${xOffset}px, ${yOffset}px) translateY(${card.dataset.floatOffset || 0}px)`;
        });
    });
    
    // Add typing indicator to chat
    addTypingIndicator();
    
    // Create floating particles
    createFloatingParticles();
    
    // Add interactive click animations
    addClickAnimations();
    
    // Add dynamic loading states
    addDynamicLoadingStates();
}

/**
 * Add click animations to interactive elements
 */
function addClickAnimations() {
    document.addEventListener('click', (e) => {
        const target = e.target.closest('.quick-card, .btn, .message-bubble');
        if (target) {
            // Create ripple effect
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.pointerEvents = 'none';
            
            const rect = target.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            target.style.position = 'relative';
            target.style.overflow = 'hidden';
            target.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        }
    });
}

/**
 * Add dynamic loading states and visual feedback
 */
function addDynamicLoadingStates() {
    // Enhanced form submission feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"], .send-btn');
            if (submitBtn) {
                submitBtn.classList.add('loading-pulse');
                setTimeout(() => {
                    submitBtn.classList.remove('loading-pulse');
                }, 3000);
            }
        });
    });
    
    // Dynamic focus indicators
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.transform = 'scale(1.02)';
            input.style.transition = 'all 0.3s ease';
        });
        
        input.addEventListener('blur', () => {
            input.style.transform = 'scale(1)';
        });
    });
}

/**
 * Create floating particles for background effect
 */
function createFloatingParticles() {
    const container = document.getElementById('particles-container');
    if (!container) return;
    
    const particleCount = 15;
    
    for (let i = 0; i < particleCount; i++) {
        setTimeout(() => {
            createParticle(container);
        }, i * 500);
    }
    
    // Continue creating particles
    setInterval(() => {
        createParticle(container);
    }, 3000);
}

/**
 * Create a single floating particle
 */
function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Random size and position
    const size = Math.random() * 4 + 2; // 2-6px
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    particle.style.left = Math.random() * 100 + '%';
    
    // Random animation duration
    particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 6000);
}

/**
 * Add typing indicator for better chat experience
 */
function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;
    
    // Create typing indicator element
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typingIndicator';
    typingIndicator.className = 'message-container agent-message typing-indicator';
    typingIndicator.style.display = 'none';
    typingIndicator.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-bubble agent-bubble">
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingIndicator);
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'flex';
        indicator.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

/**
 * Clear chat history
 */
async function clearChat() {
    try {
        const response = await fetch('/api/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear chat messages
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="message-container agent-message" data-aos="fade-right">
                    <div class="message-avatar">
                        <i class="fas fa-seedling"></i>
                    </div>
                    <div class="message-bubble agent-bubble">
                        <div class="message-content">
                            <h6>✨ Chat cleared successfully!</h6>
                            <p>I'm ready to help you with your leftover ingredients. What do you have available today?</p>
                        </div>
                        <div class="message-time">${app ? app.getCurrentTime() : 'now'}</div>
                    </div>
                </div>
            `;
            
            // Reset message count
            if (app) {
                app.messageCount = 0;
                app.focusInput();
            }
            
            // Refresh AOS
            AOS.refresh();
            
            // Show success toast
            showToast('Chat history cleared!', 'success');
        } else {
            showToast('Failed to clear chat', 'error');
        }
    } catch (error) {
        console.error('Error clearing chat:', error);
        showToast('Error clearing chat', 'error');
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add toast styles
    Object.assign(toast.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6',
        color: 'white',
        padding: '12px 20px',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        zIndex: '9999',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '14px',
        fontWeight: '500',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Add shake animation CSS
const shakeCSS = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    .shake {
        animation: shake 0.6s ease-in-out;
    }
`;

// Inject shake CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = shakeCSS;
document.head.appendChild(styleSheet);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app = new FoodWasteCoach();
});

// Handle page visibility for better performance
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && app) {
        app.focusInput();
    }
});

// Progressive Web App features
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FoodWasteCoach;
}
