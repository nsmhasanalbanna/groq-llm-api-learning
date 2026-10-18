from config.settings import settings
from schemas.ai_schemas import AIConfig, FullItineraryResponse
from tools.travel_tools import search_flight_schedule_tool, tool_registry,save_itinerary,get_trip,create_trip,get_user_trips
import json
from evaluations.combined_evaluation import evaluate_all
config = AIConfig(
    model= settings.groq_model
)

def call_llm(client, messages,tools = None, tool_choice = None, response_format = None, max_tokens = 1000, temperature = 0.2):
    parameters = {
        "model" : config.model,
        "messages" : messages,
        "max_tokens" : max_tokens,
        "temperature" : temperature
    }

    if tools is not None :
        parameters["tools"] = tools
    if tool_choice is not None:
        parameters["tool_choice"] = tool_choice
    if response_format is not None:
        parameters["response_format"] = response_format

    return client.chat.completions.create(
        **parameters
    )



def ai_answer(data, contexts, client):
    messages = [
            {
                "role":"system",
                "content" : contexts
            },
            {
                "role":"user",
                "content" : data.question
            }
        ]
    response = call_llm(client,messages,max_tokens=data.max_tokens, temperature=data.temperature)
    answer = response.choices[0].message.content

    return {
        "question" : data.question,
        "answer" : answer
    }

def create_a_trip(destination, start_date, end_date, user_id):
    trip_table = create_trip(destination, start_date, end_date, user_id)
    return {
        "creation_message" : "trip has been created successfully",
        "start_date" : trip_table["start_date"],
        "end_date" : trip_table["end_date"],
        "destination" : trip_table["destination"],
        "trip_id" : trip_table["trip_id"]
    }

def get_all_trips(user_id):
    trips = get_user_trips(user_id)
    return {
        "all_trips" : trips
    }


def ai_itinerary(trip_id, data, client, user_id):
    trip = get_trip(trip_id,user_id)
    system_prompt = """
You are a professional AI travel itinerary planner.

Your task is to plan a realistic travel itinerary based on the
user's selected destination, travel dates, and preferences.

Before generating the itinerary, request flight schedules using
the available search_flight_schedule tool.

Do not invent flight schedules or assume flights are confirmed.
Do not generate the final itinerary until flight information
has been retrieved.

IMPORTANT TIME FORMAT RULE:
Every time_of_day value MUST use HH:MM:SS format.
Examples: 09:00:00, 13:15:00, 18:30:00.
Never use HH:MM or words such as Morning, Afternoon, or Evening.
"""

    user_prompt = f"""
    Trip details:
    {json.dumps(trip, default=str)}

    Travel preferences:
    {data.instructions or "No special preferences. Create a balanced sightseeing itinerary."}
    """

    messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
    ]
    tools = [search_flight_schedule_tool]
    tool_choice={
        "type": "function",
        "function": {
            "name": "search_flight_schedule"
        }
    }
    max_tokens =500
    temperature = 0.2
    response = call_llm(client,messages,tools=tools,tool_choice=tool_choice,max_tokens=max_tokens,temperature=temperature)
    tool_call = response.choices[0].message.tool_calls
    if tool_call:
        tool_id = tool_call[0].id
        tool_name = tool_call[0].function.name
        tool_arguments = json.loads(tool_call[0].function.arguments)
        if tool_name in tool_registry:
            function_name = tool_registry[tool_name]
            tool_result = function_name(trip)
            messages.append(response.choices[0].message)
            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_id,
                "content" : json.dumps(tool_result)
            })
            final_response = call_llm(
                client,
                messages = messages,
                response_format = {
                    "type": "json_schema",
                    "json_schema": {
                    "name": "itinerary",
                    "strict": True,
                    "schema": FullItineraryResponse.model_json_schema()
                    }
                },
                max_tokens=4000,
                temperature=0.2
            )
            content = final_response.choices[0].message.content
            itinerary = FullItineraryResponse.model_validate_json(content)
            run_result = {
                "content" : content,
                "tool_name" : tool_name,
                "tool_arguments" : tool_arguments,
                "flight_results": tool_result,
                "trip" : trip           
            }
            if evaluate_all(run_result)["overall_passed"]:
                save_itinerary(itinerary, trip_id)
                answer = "YOUR ITINERARY HAS GENERATED SUCCESSFULLY"
            else:
                answer = "evaluation failed"
        else:
            answer = "unavailable tool call"

    return {
        "message" : answer
    }