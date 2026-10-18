from schemas.ai_schemas import FullItineraryResponse
from pydantic import ValidationError
def evaluate_schema(run_result):
    try:
        FullItineraryResponse.model_validate_json(run_result["content"])
        return {
            "passed" : True,
            "reason" : "Pydantic Validation successful" 
        }
    except ValidationError as ve:
        return {
            "passed" : False,
            "reason" : str(ve) 
        }

