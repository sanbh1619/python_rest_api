from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='name of user required for login')
_user_parser.add_argument('password', type=str, required=True, help='password of user required for login')


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "User with name {} already exists".format(data['username'])}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete()
        return {'message': "User deleted"}, 200

class UserLogin(Resource):

    @classmethod
    def post(cls):
        # parse arguments
        data = _user_parser.parse_args()

        # find user
        user = UserModel.find_by_username(data['username'])

        # This is what authenticate does
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200

        return {'message': "Invalid credentials"}, 401