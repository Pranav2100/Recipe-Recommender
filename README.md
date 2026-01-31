# Recipe Recommender System

## Overview
The Recipe Recommender System is a full-stack web application built with Python and Flask that suggests recipes based on user input.  
It integrates with the Spoonacular API to fetch real-time recipe data and supports full CRUD (Create, Read, Update, Delete) functionality for managing saved recipes.

This project demonstrates backend development, API integration, database management, and clean RESTful application structure.

<br>
<p align="center">
<img width="946" height="563" alt="Recipe Recommender" src="https://github.com/user-attachments/assets/51afa4c0-3590-402c-991f-d7c4d6463c80" />
</p>

Live Demo: https://recipe-recommender-po57.onrender.com

---

## 🔍 Features
- Search for recipes using keyword inputs
- Fetch recipe data using the Spoonacular API
- Full CRUD operations for saved recipes
- RESTful routes using Flask
- Persistent storage using MongoDB (PyMongo)
- Clear separation of frontend and backend logic

---

## 🧰 Tech Stack
- **Backend:** Python, Flask  
- **API Integration:** Spoonacular API  
- **Database:** MongoDB (using PyMongo)  
- **Frontend:** HTML, CSS, Jinja2 templates  
- **Version Control:** Git & GitHub

---

## 🏗 Architecture & Workflow
1. User enters a search term (e.g., “pasta”)  
2. Flask backend requests matching recipes from Spoonacular API  
3. Recipes are displayed on frontend  
4. User favorites a recipe → Saves to MongoDB  
5. User can view, update, or delete saved recipes

---

## 🚀 Installation & Setup
Follow these steps to run the application locally:

git clone https://github.com/Pranav2100/Recipe-Recommender.git
cd Recipe-Recommender

python -m venv venv
 
venv\Scripts\activate

pip install -r requirements.txt

Set up environment variables

Create a .env file with:

SPOONACULAR_API_KEY=your_spoonacular_api_key

MONGO_URI=your_mongodb_connection_string

DATABASE_NAME=recipe_app_db

Running the App

python app.py

---

👤 Author

Pranav Jagtap

GitHub: https://github.com/Pranav2100

LinkedIn: https://www.linkedin.com/in/pranav--jagtap

Email: pranavjagtap2151@gmail.com
