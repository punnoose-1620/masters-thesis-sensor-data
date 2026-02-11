from LLM_Classes import FunctionCall

def function_limit_checker(functions: list[FunctionCall]) -> bool:
    return len(functions) <= 5

def append_result_to_instance(instance: FunctionCall, result: str) -> FunctionCall:
    instance.results = result
    return instance