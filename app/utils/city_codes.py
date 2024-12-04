city_codes = {
    "New York": "NYC",
    "London": "LON",
    "Moscow": "MOV",
    "Paris": "CDG",
    "Saint Petersburg": "LED"

}


def get_city_code(city: str) -> str:
    return city_codes.get(city)
