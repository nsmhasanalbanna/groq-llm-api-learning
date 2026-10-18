expected_result ={
    "tool_name" : "search_flight_schedule",
}
def evaluate_tool(run_result):
    answer = "improper tool call"
    if run_result["tool_name"] == expected_result["tool_name"]:
        return {
            "passed" : True,
            "reason" : "exact tool was called"
        }
    return {
        "passed" : False,
        "reason" : answer
    }

