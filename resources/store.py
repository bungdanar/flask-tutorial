# from uuid import uuid4

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from common.schemas import StoreSchema
from common.db import db
from models import StoreModel

blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found")

        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted"}
        # except KeyError:
        #     abort(404, message="Store not found")

        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted."}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {
        #     "stores": list(stores.values())
        # }

        # return stores.values()

        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        '''
        Using default request object from flask
        '''
        # store_data = request.get_json()

        # if "name" not in store_data:
        #     abort(
        #         400, message="Bad request. Ensure 'name' is included in the JSON payload.")

        '''
        Using marshmallow object
        '''
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message="Store already exists.")

        # store_id = uuid4().hex

        # store = {
        #     **store_data,
        #     "id": store_id
        # }

        # stores[store_id] = store

        '''
        Using sql alchemy model
        '''
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred when creating store.")

        return store, 201
