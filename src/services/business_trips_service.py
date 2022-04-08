from src.models.business_trip import BusinessTrip, PenguinTripsCount, DestinationsCount


class BusinessTripService:
    def get_data(self):

        average_destinations_count = DestinationsCount.objects().average("count")
        destininations_with_most_count_qs = DestinationsCount.objects(
            count__gte=average_destinations_count
        )
        most_visited_places = [item.name for item in destininations_with_most_count_qs]

        average_pengiuns_trips_count = PenguinTripsCount.objects().average("count")
        penguins_with_most_trips_qs = PenguinTripsCount.objects(
            count__gte=average_pengiuns_trips_count
        )
        penguins_with_most_trips = [item.name for item in penguins_with_most_trips_qs]

        data = {
            "penguins_with_most_trips": penguins_with_most_trips,
            "most_visited_places": most_visited_places,
            "total_business_trips": len(BusinessTrip.objects(business=True)),
        }
        return data
