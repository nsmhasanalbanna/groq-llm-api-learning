from fastapi import APIRouter,Depends
from schemas.ai_schemas import AIResponseModel,AIRequestModel,CreateTripRequest,CreateTripResponse, AllTripsResponse,GenerateItineraryRequest
from services import ai_services,chunking
from clients.groq_client import get_groq_client
from clients.voyage_client import get_voyage_header
from dependencies.authentication_header import get_current_user_id


ai_router = APIRouter(prefix="/ai",)

@ai_router.post("/question/", response_model= AIResponseModel)
def ai_question(data : AIRequestModel, client = Depends(get_groq_client),headers : dict = Depends(get_voyage_header), user_id : int =Depends(get_current_user_id)):
    contexts = chunking.ask_rag(data.question,headers)
    return ai_services.ai_answer(data, contexts, client)

@ai_router.post("/trips/", response_model= CreateTripResponse)
def make_trip(data : CreateTripRequest, user_id : int = Depends(get_current_user_id)):
    return ai_services.create_a_trip(data.destination, data.start_date, data.end_date, user_id)

@ai_router.get("/my_trips/", response_model= AllTripsResponse)
def show_all_trips(user_id : int = Depends(get_current_user_id)):
    return ai_services.get_all_trips(user_id)

@ai_router.post("/trips/{trip_id}/itinerary/")
def generate_itinerary(trip_id : int, data: GenerateItineraryRequest, client = Depends(get_groq_client), user_id : int = Depends(get_current_user_id)):
    return ai_services.ai_itinerary(trip_id, data, client, user_id)
    

