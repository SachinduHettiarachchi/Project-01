*Food Recipe System*

The Food Recipe System is a web application that allows users, especially migrant students, to discover, save, and share food recipes. This project aims to solve the challenge many students face with meal preparation due to a lack of knowledge. The system provides a supportive platform where users can find step-by-step instructions for preparing various dishes.

*Features*

--User Authentication--

-Register new account
-Login to existing account
-Secure session management


--Recipe Management--

-Browse recipes by categories
-Search for specific recipes
-View detailed recipe information
-Rate and comment on recipes
-Save favorite recipes to personal collection


--User Interface--

Responsive design for mobile, tablet, and desktop
Intuitive navigation
Recipe cards with images and essential information
Category-based filtering
User-friendly forms



*Project Structure*


food-recipe-system/
├── css/
│   ├── styles.css          # Main stylesheet
│   └── responsive.css      # Responsive design styles
├── js/
│   ├── app.js              # Main application logic
│   ├── auth.js             # Authentication functionality
│   └── recipe.js           # Recipe management
├── img/
│   ├── hero-bg.jpg         # Hero section background
│   ├── recipe-placeholder.jpg  # Default recipe image
│   ├── categories/         # Category images
│   └── recipes/            # Recipe images
├── pages/
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── recipe.html         # Recipe details page
│   ├── categories.html     # Categories browsing page
│   ├── saved-recipies.html # Saved recipes page
│   └── search.html         # Search results page
└── index.html              # Home page


*MVC Implementation*

This project follows the Model-View-Controller (MVC) architecture:

- Model (M): The `models.py` file defines the data structures and business logic.
  - `User` class: Represents a user with authentication details and saved recipes
  - `Recipe` class: Contains recipe details, ingredients, and instructions
  - `Comment` class: Stores user comments on recipes
  - `DataStore` class: Handles data persistence and retrieval operations


- View (V): The templates in the `templates` folder provide the user interface.
  - Uses Flask's Jinja2 templating engine
  - Responsive design with CSS


- Controller (C): The `app.py` file handles HTTP requests and responds accordingly.
  - Routes user requests to the appropriate functions
  - Processes form submissions
  - Manages sessions for authentication


*Setup Instructions*

1. Install Python 3.8 or higher
2. Install dependencies: