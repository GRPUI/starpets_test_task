# Импортируем библиотеки
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from random import randint, choice
import string

from weather import fetch_weather

# Создаем приложение
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# Создаем модель для пользователей
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    # Методы для работы с пользователями
    @classmethod
    def get_user(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def add_user(cls, username, balance):
        new_user = cls(username=username, balance=balance)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def delete_user(cls, user_id):
        user = cls.get_user(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def update_user(cls, user_id, username, balance):
        user = cls.get_user(user_id)
        if user:
            if username:
                user.username = username
            if balance:
                user.balance = balance
            db.session.commit()
            return user
        return None

    @classmethod
    def update_user_balance(cls, user_id, change_amount):
        user = cls.get_user(user_id)
        if user:
            if change_amount and user.balance + change_amount >= 0:
                user.balance += change_amount
            db.session.commit()
            return user
        return None


# Создаем таблицу в базе данных, которая соответствует модели и создаётся при запуске приложения
with app.app_context():
    db.drop_all()
    db.create_all()
    for count in range(5):
        Users.add_user(
            username=''.join(choice(string.ascii_letters + string.digits) for i in range(10)),
            balance=randint(500, 1500)
        )


# Создаем маршрут для приветствия
@app.route('/')
def hello_world():
    return 'Привет, STARPETS! Думаю, что напишу то же на FastAPI, но намного лучше :)'


# маршрут для обновления баланса пользователя
# Пример запроса: http://127.0.0.1:5000/update/?userId=1&city=moscow
@app.route("/update/")
def update():
    try:
        user_id = int(request.args.get('userId'))
    except ValueError:
        return {'error': 'Invalid user id'}
    city = request.args.get('city')
    weather = fetch_weather(city)
    if weather is None:
        return {'error': 'City not found'}
    user = Users.update_user_balance(user_id, weather)
    if not user:
        return {'error': 'User not found'}
    return {'id': user.id, 'username': user.username, 'balance': user.balance}


# точка входа в приложение
if __name__ == '__main__':
    app.run()
