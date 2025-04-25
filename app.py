from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Recipe %r>' % self.id

def seed_database():
    if Recipe.query.count() == 0:
        sample_recipes = [
            Recipe(name="Spaghetti Bolognese",
                   ingredients="spaghetti, ground beef, tomato sauce, garlic, onion, olive oil, salt, pepper",
                   instructions="Cook pasta. Brown meat with garlic and onion. Add sauce. Combine."),
            Recipe(name="Greek Salad",
                   ingredients="tomato, cucumber, red onion, feta cheese, olives, olive oil, oregano, salt",
                   instructions="Chop vegetables. Mix with olive oil and seasoning."),
            Recipe(name="Pancakes",
                   ingredients="flour, milk, eggs, sugar, baking powder, salt, butter",
                   instructions="Mix ingredients. Fry in a pan on medium heat.")
        ]
        db.session.bulk_save_objects(sample_recipes)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_database()




# Main page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Page with full information about recipe
@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    return render_template('recipes.html', recipe=recipe)

# API для поиска рецептов по ингредиентам
@app.route('/search_recipes', methods=['POST'])
def search_recipes():
    query = request.form.get('query')  # Получаем данные из формы
    if not query:
        return "No query provided", 400

    # Разделяем строку на список ингредиентов
    ingredients = [x.strip().lower() for x in query.split(',')]
    matching_recipes = find_recipes(ingredients)

    return render_template('search_results.html', recipes=matching_recipes, query=query)

# API для добавления нового рецепта
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        add_new_recipe(name, ingredients, instructions)
        return redirect(url_for('index'))
    
    return render_template('recipes.html')




def get_all_recipes():
    recipes = Recipe.query.all()
    return [
        {
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": [ingredient.strip().lower() for ingredient in recipe.ingredients.split(",")],
            "instructions": recipe.instructions
        }
        for recipe in recipes
    ]

# Функция для получения всех рецептов
def find_recipes(available_ingredients):
    available_ingredients = [ing.strip().lower() for ing in available_ingredients]
    recipes = get_all_recipes()

    matching_recipes = []
    for recipe in recipes:
        match_count = len(set(recipe["ingredients"]).intersection(set(available_ingredients)))
        if match_count > 0:
            matching_recipes.append({
                "id": recipe["id"],
                "name": recipe["name"],
                "match_count": match_count,
                "ingredients": recipe["ingredients"],
                "instructions": recipe["instructions"]
            })

    # сортируем по количеству совпадений
    matching_recipes.sort(key=lambda x: x["match_count"], reverse=True)
    return matching_recipes

def get_recipe_by_id(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    return {"id": recipe.id, "name": recipe.name, "ingredients": recipe.ingredients, "instructions": recipe.instructions} if recipe else None


# Function for adding new recipes
def add_new_recipe(name, ingredients, instructions):
    new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
    db.session.add(new_recipe)
    db.session.commit()

@app.route('/recipes')
def all_recipes():
    recipes = Recipe.query.all()
    return render_template('all_recipes.html', recipes=recipes)



    



if __name__ == '__main__':
    app.run(debug=True)