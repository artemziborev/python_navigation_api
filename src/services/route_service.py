from typing import List
from .route_calculator import RouteCalculator
from src.models.business_trip import BusinessTrip, PenguinTripsCount, DestinationsCount


class RouteService:
    def __init__(
        self, distances: List[str], destinations: List[str], name: str, business: bool
    ):
        self.distances = distances
        self.destinations = destinations
        self.start_point = "Munich"
        self.name = name
        self.business = business
        self.path_calculator = RouteCalculator(
            start_node=self.start_point,
            destinations=self.destinations,
            distances=self.distances,
        )

    def get_path(self):
        places_to_travel = self.path_calculator.run()
        trip_data = {
            "name": self.name,
            "destinations": places_to_travel,
            "business": self.business,
        }
        business_trip_item = BusinessTrip(**trip_data)
        business_trip_item.save()
        if self.business:
            try:
                penguins_trip = PenguinTripsCount.objects(name=self.name).get()
                PenguinTripsCount.objects(name=self.name).update_one(
                    upsert=True, inc__count=1
                )
            except PenguinTripsCount.DoesNotExist:
                penguin_trip_data = {"name": self.name, "count": 1}
                db_item = PenguinTripsCount(**penguin_trip_data)
                db_item.save()
            for item in self.destinations:
                try:
                    destination_item = DestinationsCount.objects(name=item).get
                    DestinationsCount.objects(name=item).update_one(
                        upsert=True, inc__count=1
                    )
                except DestinationsCount.DoesNotExist:
                    destination_count_data = {"name": item, "count": 1}
                    destination_db_item = DestinationsCount(**destination_count_data)
                    destination_db_item.save()

        return {"places_to_travel": places_to_travel}
