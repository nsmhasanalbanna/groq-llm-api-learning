from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
class AIResponseModel(BaseModel):
    question : str
    answer : str

class AIRequestModel(BaseModel):
    question : str = Field(min_length=2,max_length=3000)
    max_tokens : int = Field(ge=1,le=1000)
    temperature : float = Field(ge=0.0,le=1.0)

class AIConfig(BaseModel):
    model : str

class ItineraryResponseItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day : int
    date : date
    time_of_day : str = Field(pattern=r"^\d{2}:\d{2}:\d{2}$")
    activity : str
    location : str

class FullItineraryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items : list[ItineraryResponseItem]

class CreateTripRequest(BaseModel):
    start_date : date 
    end_date : date
    destination : str = Field(min_length=2,max_length=15)

class CreateTripResponse(BaseModel):
    creation_message : str
    start_date : date
    end_date : date
    destination : str
    trip_id : int 

class EachTrip(BaseModel):
    trip_id : int
    start_date : date
    end_date : date
    destination : str

class AllTripsResponse(BaseModel):
    all_trips : list[EachTrip]

class GenerateItineraryRequest(BaseModel):
    instructions : str | None = Field(min_length=10, max_length=100) 