import os

from flask import request, make_response

from flask_restx import Api, Resource, fields
from src.services.route_service import RouteService
from src.services.business_trips_service import BusinessTripService

from src import app
from src.database import connect_to_database
from src.routes import add_routes


connect_to_database(os.getenv("DB_URI"))
add_routes()


api = Api(app)


model = api.model(
    "CalculatePathPayload",
    {
        "name": fields.String(required=True, description="str. Penguin name."),
        "destinations": fields.List(
            fields.String, required=True, description="List of destinations."
        ),
        "business": fields.Boolean(
            required=True,
            description='Indicates if it is a business trip. `true` for "business" trip, `false` for "casual" trip.',
        ),
        "distances": fields.List(
            fields.String, required=True, description="List with all places to visit."
        ),
    },
)


@api.route("/calculate")
class CalculatePathRouter(Resource):
    @api.expect(model)
    def post(self):
        service = RouteService(**request.json)
        result = service.get_path()
        return make_response(result, 200)


@api.route("/business-trips")
class BusinessTripsRouter(Resource):
    def get(self):
        service = BusinessTripService()
        result = service.get_data()
        return make_response(result)
