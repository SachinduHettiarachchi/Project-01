# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import DataStore
import os

app = Flask(__name__,static_folder='static', template_folder='templates')
app.secret_key = 'food_recipe_system_secret_key'  

# Initialize data store
data_store = DataStore()

# Routes
@app.route('/')
def index():
    featured_recipes = data_store.get_featured_recipes()
    return render_template('index.html', featured_recipes=featured_recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate user
        user = data_store.get_user_by_email(email)
        if user and user.password == password:  # In real app, check hashed password
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        
        # Validate input
        if not username or not email or not password:
            error = 'Please fill in all fields'
            return render_template('register.html', error=error)
        
        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('register.html', error=error)
        
        # Check if email already exists
        if data_store.get_user_by_email(email):
            error = 'Email already registered'
            return render_template('register.html', error=error)
        
        # Create user
        user = data_store.add_user(username, email, password)
        session['user_id'] = user.id
        session['username'] = user.username
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = data_store.get_recipe_by_id(recipe_id)
    if not recipe:
        return render_template('404.html'), 404
    return render_template('recipe.html', recipe=recipe)

@app.route('/categories')
def categories():
    category = request.args.get('category')
    if category:
        recipes = data_store.get_recipes_by_category(category)
    else:
        recipes = data_store.get_all_recipes()
    
    return render_template('categories.html', recipes=recipes, category=category)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    recipes = data_store.search_recipes(query) if query else []
    return render_template('search.html', recipes=recipes, query=query)

@app.route('/saved-recipes')
def saved_recipes():
    # If user is not logged in, show empty saved recipes page with login prompt
    if 'user_id' not in session:
        return render_template('saved-recipes.html', 
                              recipes=[], 
                              not_logged_in=True)
    
    # For logged in users, show their saved recipes
    user = data_store.get_user_by_id(session['user_id'])
    saved = [data_store.get_recipe_by_id(recipe_id) for recipe_id in user.saved_recipes]
    saved = [recipe for recipe in saved if recipe]  # Filter out None values
    return render_template('saved-recipes.html', recipes=saved)

# API routes for AJAX calls
@app.route('/api/comment/<int:recipe_id>', methods=['POST'])
def add_comment(recipe_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Login required'}), 401
        
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Comment text is required'}), 400
        
    user = data_store.get_user_by_id(session['user_id'])
    comment = data_store.add_comment(text, user.username, recipe_id)
    
    return jsonify({
        'id': comment.id,
        'text': comment.text,
        'author': comment.author,
        'date': comment.date
    })

@app.route('/api/save-recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Login required'}), 401
        
    user = data_store.get_user_by_id(session['user_id'])
    
    if recipe_id in user.saved_recipes:
        user.saved_recipes.remove(recipe_id)
        saved = False
    else:
        user.saved_recipes.append(recipe_id)
        saved = True
    
    return jsonify({'saved': saved})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/test-images')
def test_images():
    return """
    <html>
    <head>
        <title>Image Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .image-test { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }
            img { max-width: 300px; height: auto; }
        </style>
    </head>
    <body>
        <h1>Image Path Testing</h1>
        
        <div class="image-test">
            <h2>Recipe Images</h2>
            <p>carbonara.jpg:</p>
            <img src="/static/img/carbonara.jpg" alt="Carbonara">
            
            <p>tikka-masala.jpg:</p>
            <img src="/static/img/tikka-masala.jpg" alt="Tikka Masala">
        </div>
        
        <div class="image-test">
            <h2>Category Images</h2>
            <p>pasta.jpg:</p>
            <img src="/static/img/pasta.jpg" alt="Pasta">
            
            <p>salad.jpg:</p>
            <img src="/static/img/salad.jpg" alt="Salad">
        </div>
        
        <div class="image-test">
            <h2>Background Image</h2>
            <p>hero-bg.jpg:</p>
            <img src="/static/img/hero-bg.jpg" alt="Hero">
        </div>
    </body>
    </html>
    """


  