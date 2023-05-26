# from uuid import uuid4

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from common.schemas import ItemSchema, ItemUpdateSchema
from common.db import db
from models import ItemModel

blp = Blueprint("items", __name__, description="Operation on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found")

        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted"}
        # except KeyError:
        #     abort(404, message="Item not found")

        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilage required")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted."}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        '''
        Using default request object from flask
        '''
        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     abort(
        #         400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")

        # try:
        #     item = items[item_id]
        #     item |= item_data

        #     return item
        # except KeyError:
        #     abort(404, message="Item not found")

        item = ItemModel.query.get_or_404(item_id)
        item.name = item_data["name"]
        item.price = item_data["price"]

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {
        #     "items": list(items.values())
        # }

        # return items.values()

        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        '''
        Using default request object from flask
        '''
        # item_data = request.get_json()

        # if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
        #     abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload")

        '''
        Using marshmallow object
        '''
        # for item in items.values():
        #     if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
        #         abort(400, message="Item already exists")

        # if item_data["store_id"] not in stores:
        #     abort(404, message="Store not found")

        # item_id = uuid4().hex
        # item = {
        #     **item_data,
        #     "id": item_id
        # }
        # items[item_id] = item

        '''
        Using sql alchemy model
        '''
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item, 201
