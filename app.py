import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import User, UserRegister, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') # 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disabling flask tracking as SQLAlchemy already does it
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'json' # app.config['JWT_SECRET_KEY'] can be used
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(UserLogin, '/auth') # 'auth' can be renamed to /login
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':

    from db import db
    db.init_app(app)

    app.run(port=5000)
