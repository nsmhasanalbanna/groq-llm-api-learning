from evaluations.geographical_evaluation import evaluate_geographical_location
from evaluations.schema_evaluation import evaluate_schema
from evaluations.temporal_evaluation import evaluate_temporal
from evaluations.tool_evaluation import evaluate_tool

def evaluate_all(run_result):
    schema_result = evaluate_schema(run_result)
    overall_eval_data ={
        "schema" : schema_result
    }
    if not schema_result["passed"]:
        overall_passed = False
    else:
        overall_eval_data["tool"] = evaluate_tool(run_result)
        overall_eval_data["temporal"] = evaluate_temporal(run_result)
        #overall_eval_data["geographical"] = evaluate_geographical_location(run_result)
        overall_passed = True
        for datum in overall_eval_data.values():
            if datum["passed"] is False:
                overall_passed = False
                break

    overall_eval_data["overall_passed"] = overall_passed
    return overall_eval_data
        
     