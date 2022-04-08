from src.services.route_calculator import RouteCalculator

distances = [
    "Munich - Munich: 0",
    "Munich - Kinganru: 3",
    "Munich - Facenianorth: 7",
    "Munich - SantaTiesrie: 4",
    "Munich - Mitling: 1",
    "Kinganru - Facenianorth: 2",
    "Kinganru - SantaTiesrie: 1",
    "Kinganru - Mitling: 1",
    "Facenianorth - SantaTiesrie: 5",
    "Facenianorth - Mitling:  3",
    "SantaTiesrie - Mitling: 2",
]

destinations =  ["Kinganru", "Facenianorth", "SantaTiesrie"]

def test_algo():
    calculator = RouteCalculator(destinations=destinations, distances=distances, start_node="Munich")
    result = calculator.run()
    assert result == ["Munich", "Mitling", "Kinganru", "Facenianorth", "Kinganru", "SantaTiesrie"]

