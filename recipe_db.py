import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Настроим приложение Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для рецепта
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Recipe {self.name}>'

# Функция для создания базы данных и добавления тестовых данных
def create_and_seed_database():
    with app.app_context():
        db.create_all()  # Создаем таблицы с помощью SQLAlchemy

    print("Database created and seeded successfully!")

# Функция для сбора рецептов с сайта AllRecipes
def get_recipes_from_allrecipes():
    url = "https://www.allrecipes.com/recipes/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Пример парсинга. Это зависит от структуры сайта.
    recipe_cards = soup.find_all('article', class_='fixed-recipe-card')

    recipes = []

    for card in recipe_cards:
        name = card.find('span', class_='fixed-recipe-card__title-link').text.strip()
        ingredients = card.find('div', class_='fixed-recipe-card__ingredients').text.strip()
        instructions = card.find('div', class_='fixed-recipe-card__instructions').text.strip()

        recipe = {
            'name': name,
            'ingredients': ingredients,
            'instructions': instructions
        }

        recipes.append(recipe)

    return recipes

# Функция для добавления собранных рецептов в базу данных
def add_recipes_to_database():
    recipes = get_recipes_from_allrecipes()

    with app.app_context():
        for recipe_data in recipes:
            new_recipe = Recipe(
                name=recipe_data['name'],
                ingredients=recipe_data['ingredients'],
                instructions=recipe_data['instructions']
            )
            db.session.add(new_recipe)

        db.session.commit()

    print("Recipes added to the database!")

# Запуск функции для создания и наполнения базы данных
if __name__ == '__main__':
    create_and_seed_database()  # Создаём базу данных и таблицы
    add_recipes_to_database()  # Собираем данные и добавляем их в базу
