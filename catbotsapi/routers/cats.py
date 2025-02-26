from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError
from catbotsapi.models.models import Cat
from catbotsapi.repository.database import add_info_db, get_parsed_data
from catbotsapi.extensions import limiter

cats_bp = Blueprint("cats", __name__)

@cats_bp.route("/cats", methods=["GET"])
@limiter.limit("600 per minute")
def data_parser() -> tuple[Response, int]:
    attribute = request.args.get("attribute", default="name")
    order = request.args.get("order", default="asc")
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=10, type=int)

    result = get_parsed_data(attribute, order, offset, limit)
    return jsonify(result[0]), result[1]

@cats_bp.route("/cat", methods=["POST"])
def add_info() -> tuple[dict[str, str], int] | tuple[Response, int]:
    try:
        data_cats = Cat(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    result = add_info_db(data_cats.dict())
    return jsonify(result[0]), result[1]