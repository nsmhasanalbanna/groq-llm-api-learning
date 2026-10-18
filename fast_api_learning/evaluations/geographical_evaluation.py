from evaluations.schema_evaluation import evaluate_schema
from schemas.ai_schemas import FullItineraryResponse
from clients.geofy_client import get_geofy_client
def evaluate_geographical_location(run_result):
    if evaluate_schema(run_result)["passed"]:
        itinerary = FullItineraryResponse.model_validate_json(run_result["content"])
        destinations = [run_result["trip"]["destination"].lower(),"kamakura","yokohama","nikko","hakone","kawagoe"]
        for place in itinerary.items:
            data = get_geofy_client(place.location).json()
            city = data["features"][0]["properties"]["city"].lower()
            district = data["features"][0]["properties"]["district"].lower()
            if city in destinations or district in destinations:
                continue
            else :
                return {
                    "passed" : False,
                    "reason" : f"{city} is inaccessible place from the destination"
                }

        return {
            "passed" : True,
            "reason" : "places are within range of the destination"
        }
            
        

