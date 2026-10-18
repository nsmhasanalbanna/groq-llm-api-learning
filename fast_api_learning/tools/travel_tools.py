from clients.post_gres_client import get_post_gres_connection
from clients.flight_client import get_flight_response
from schemas.ai_schemas import FullItineraryResponse


search_flight_schedule_tool = {
    "type": "function",
    "function": {
        "name": "search_flight_schedule",
        "description": "Retrieve the actual flight schedule for a trip using the trip details stored in the database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


def search_flight_schedule(trip):
    airports = {
        "germany": "FRA",
        "usa": "JFK",
        "uk": "LHR",
        "france": "CDG",
        "uae": "DXB",
        "singapore": "SIN",
        "brazil": "GRU",
        "argentina": "EZE",
        "australia": "SYD",
        "new zealand": "AKL",
        "japan" : "NRT",
        "hongkong" : "HKG"
    }
    destination = airports[trip["destination"].lower()]
    departure_date = trip["departure_date"]
    return_date = trip["return_date"]
    results = get_flight_response("DAC",destination,departure_date,return_date)
    return results

tool_registry = {
    "search_flight_schedule" : search_flight_schedule
}

def create_trip(destination : str, start_date : str, end_date : str, user_id : int):
    connection = get_post_gres_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO trips (destination, start_date, end_date, user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (destination, start_date, end_date, user_id)
            )
            trip_id = cursor.fetchone()[0]
            connection.commit()

            return {
                "trip_id" : trip_id,
                "destination" : destination,
                "start_date" : start_date,
                "end_date" : end_date
            }

    finally:
        connection.close()

def get_trip(trip_id:int, user_id:int):
    connection = get_post_gres_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT destination, start_date, end_date 
                FROM trips
                WHERE id = %s and user_id = %s;
                """,
                (trip_id,user_id)
            )
            row = cursor.fetchone()
            return {
                "destination" : row[0],
                "departure_date" : row[1],
                "return_date" : row[2]
            }
    finally:
        connection.close()

def save_itinerary(itinerary : FullItineraryResponse, trip_id : int):
    connection = get_post_gres_connection()

    try:
        with connection.cursor() as cursor:
            for day in itinerary.items:
                cursor.execute(
                """
                INSERT INTO itinerary_items(trip_id, day, date, time_of_day, activity,location)
                VALUES(%s,%s,%s,%s,%s,%s);
                """,
                (
                    trip_id,
                    day.day,
                    day.date,
                    day.time_of_day,
                    day.activity,
                    day.location
                )
                )
        connection.commit()
        return {
            "trip_id" : trip_id,
            "status" : "saved successfully"
        }
    finally:
        connection.close()

def get_user_trips(user_id):
    connection = get_post_gres_connection()
    all_trips = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id,destination, start_date, end_date
                FROM TRIPS
                WHERE user_id = %s
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

            for row in rows:
                all_trip = {
                    "trip_id" : row[0],
                    "destination" : row[1],
                    "start_date" : row[2],
                    "end_date" : row[3]
                }
                all_trips.append(all_trip)
            return all_trips

    finally:
        connection.close()



    