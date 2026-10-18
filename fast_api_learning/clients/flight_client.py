from config.settings import settings
import serpapi

api_key = settings.flight_api_key

def get_flight_response(origin,destination,departure_date,return_date):
    client = serpapi.Client(api_key=api_key)
    results = []

    parameters = {
                "engine": "google_flights",
                "departure_id": origin,
                "arrival_id": destination,
                "outbound_date": departure_date,
                "return_date": return_date,
                "currency": "USD",
                "hl": "en",
    
            }
    outbound_results = client.search(parameters)
    outbound_flight ={
        "departure_data" : outbound_results["best_flights"][0]["flights"][0]["departure_airport"],
        "arrival_data" : outbound_results["best_flights"][0]["flights"][-1]["arrival_airport"],
        "outbound_airline" : [outbound_results["best_flights"][0]["flights"][0]["airline"],outbound_results["best_flights"][0]["flights"][-1]["airline"]],
        "outbound_flight_number" : [outbound_results["best_flights"][0]["flights"][0]["flight_number"],outbound_results["best_flights"][0]["flights"][-1]["flight_number"]]
    }
    results.append(outbound_flight)
    parameters["departure_token"] = outbound_results["best_flights"][0]["departure_token"]
    return_results = client.search(parameters)

    return_flight ={
        "departure_data" : return_results["other_flights"][0]["flights"][0]["departure_airport"],
        "arrival_data" : return_results["other_flights"][0]["flights"][-1]["arrival_airport"],
        "return_airline" : [return_results["other_flights"][0]["flights"][0]["airline"],return_results["other_flights"][0]["flights"][-1]["airline"]],
        "return_flight_number" : [return_results["other_flights"][0]["flights"][0]["flight_number"],return_results["other_flights"][0]["flights"][-1]["flight_number"]]
    }
    results.append(return_flight)

    return results
    

