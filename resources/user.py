from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from common.db import db
from models import UserModel
from common.schemas import UserSchema

blp = Blueprint("users", __name__, description="Operation on users")


@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(username=user_data["username"], password=pbkdf2_sha256.hash(
            user_data["password"]))

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="A user with that username already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred when creating user")

        return user


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred when deleting user")

        return {"message": "User deleted"}
