# models.py

class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password  
        self.saved_recipes = []

class Recipe:
    def __init__(self, id, title, description, image, prep_time, cook_time, 
                 servings, difficulty, ingredients, instructions, 
                 categories, author, date, ratings=None, featured=False):
        self.id = id
        self.title = title
        self.description = description
        self.image = image
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.difficulty = difficulty
        self.ingredients = ingredients
        self.instructions = instructions
        self.categories = categories
        self.author = author
        self.date = date
        self.ratings = ratings or []
        self.featured = featured
        self.comments = []

class Comment:
    def __init__(self, id, text, author, date, recipe_id):
        self.id = id
        self.text = text
        self.author = author
        self.date = date
        self.recipe_id = recipe_id

# Data store to mimic a database
class DataStore:
    def __init__(self):
        self.users = {}
        self.recipes = {}
        self.comments = {}
        self.next_user_id = 1
        self.next_recipe_id = 1
        self.next_comment_id = 1
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        # Add sample recipes
        carbonara = Recipe(
            id=self.next_recipe_id,
            title="Pasta Carbonara",
            description="Classic Italian pasta dish with eggs, cheese, pancetta, and pepper",
            image="img/carbonara.jpg",  
            prep_time=10,
            cook_time=15,
            servings=4,
            difficulty="Medium",
            ingredients=[
                "350g spaghetti",
                "150g pancetta",
                "50g pecorino cheese",
                "50g parmesan",
                "3 large eggs",
                "Black pepper"
            ],
            instructions=[
                "Cook pasta in salted water according to package instructions",
                "Fry pancetta until crispy",
                "Beat eggs with grated cheese and pepper",
                "Drain pasta, mix with pancetta, then quickly stir in egg mixture",
                "Serve immediately with extra cheese and pepper"
            ],
            categories=["Pasta", "Italian", "Quick Meals"],
            author="Chef Mario",
            date="2025-03-01",
            ratings=[4, 5, 5, 4, 5],
            featured=True
        )
        self.recipes[self.next_recipe_id] = carbonara
        self.next_recipe_id += 1
        
        tikka = Recipe(
            id=self.next_recipe_id,
            title="Chicken Tikka Masala",
            description="Creamy and flavorful Indian curry with marinated chicken pieces",
            image="img/tikka-masala.jpg",  
            prep_time=30,
            cook_time=40,
            servings=6,
            difficulty="Medium",
            ingredients=[
                "800g chicken breast",
                "200ml yogurt",
                "2 tbsp garam masala",
                "1 tbsp cumin",
                "1 tbsp turmeric",
                "400ml tomato sauce",
                "200ml heavy cream",
                "2 onions",
                "4 garlic cloves",
                "Fresh coriander"
            ],
            instructions=[
                "Mix yogurt with spices and marinate chicken for at least 1 hour",
                "Grill or bake chicken until cooked through",
                "Sauté onions and garlic until soft",
                "Add tomato sauce and simmer for 10 minutes",
                "Add cream and simmer for another 5 minutes",
                "Cut chicken into pieces and add to the sauce",
                "Garnish with fresh coriander and serve with rice or naan"
            ],
            categories=["Curry", "Indian", "Chicken"],
            author="Chef Raj",
            date="2025-03-15",
            ratings=[5, 4, 5, 5, 4],
            featured=True
        )
        self.recipes[self.next_recipe_id] = tikka
        self.next_recipe_id += 1
        
        # Add a sample user
        admin = User(
            id=self.next_user_id,
            username="admin",
            email="admin@example.com",
            password="password123"
        )
        self.users[self.next_user_id] = admin
        self.next_user_id += 1
    
    # User methods
    def add_user(self, username, email, password):
        user = User(self.next_user_id, username, email, password)
        self.users[self.next_user_id] = user
        self.next_user_id += 1
        return user
    
    def get_user_by_email(self, email):
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        return self.users.get(user_id)
    
    # Recipe methods
    def get_all_recipes(self):
        return list(self.recipes.values())
    
    def get_recipe_by_id(self, recipe_id):
        return self.recipes.get(recipe_id)
    
    def get_recipes_by_category(self, category):
        return [r for r in self.recipes.values() if category in r.categories]
    
    def get_featured_recipes(self):
        return [r for r in self.recipes.values() if r.featured]
    
    def search_recipes(self, query):
        query = query.lower()
        return [r for r in self.recipes.values() 
                if query in r.title.lower() or 
                   query in r.description.lower() or
                   any(query in cat.lower() for cat in r.categories) or
                   any(query in ing.lower() for ing in r.ingredients)]
    
    # Comment methods
    def add_comment(self, text, author, recipe_id):
        from datetime import datetime
        comment = Comment(
            id=self.next_comment_id,
            text=text,
            author=author,
            date=datetime.now().isoformat(),
            recipe_id=recipe_id
        )
        self.comments[self.next_comment_id] = comment
        self.next_comment_id += 1
        
        # Add to recipe's comments
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe:
            recipe.comments.append(comment)
        
        return comment
    
    def get_recipe_comments(self, recipe_id):
        return [c for c in self.comments.values() if c.recipe_id == recipe_id]