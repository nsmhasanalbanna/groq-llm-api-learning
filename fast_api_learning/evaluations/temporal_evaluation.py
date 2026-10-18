from evaluations.schema_evaluation import evaluate_schema
from datetime import datetime
from schemas.ai_schemas import FullItineraryResponse

def evaluate_temporal(run_result):
    if evaluate_schema(run_result)["passed"]:
        itinerary = FullItineraryResponse.model_validate_json(run_result["content"])
        arrival = datetime.strptime(run_result["flight_results"][0]["arrival_data"]["time"], "%Y-%m-%d %H:%M")
        departure = datetime.strptime(run_result["flight_results"][1]["departure_data"]["time"], "%Y-%m-%d %H:%M")
        check = False
        for item in itinerary.items:
            activity_date_time = datetime.combine(
                item.date,
                datetime.strptime(item.time_of_day, "%H:%M:%S").time()
            )
            if arrival< activity_date_time < departure:
                continue
                
            else :
                check = True
                break
        if not check:
            return {
                "passed" : True,
                "reason" : "all activities are within scheduled time frame"
            }
        return {
            "passed": False,
            "reason" : "unrealistic date or time"
        }