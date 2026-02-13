from typing import Any
from LLM_Classes import RawData

# Static Queries

SINGLE_FUNCTION_SELECTOR_STATIC_QUERY = """
You are a helpful assistant that helps to select the function to call based on the intent of the user query.
Given:
- a list of functions
- a user query
- possibly the response of the previous function call.
Task:
- select the function that is most relevant to the user query.
- return the function name and the parameters to call the function.
- choose optimal plan to use minimal functions to answer the user query.
Function Map:
<FUNCTION_MAP>
Response Format:
<FUNCTION_SELECTOR_RESPONSE_FORMAT>
"""

ALL_FUNCTIONS_SELECTOR_STATIC_QUERY = """
You are a helpful assistant that helps to select the function to call based on the intent of the user query.
Given:
- a list of functions
- a user query
- possibly the response of the previous function call.
Task:
- select the function that is most relevant to the user query.
- return the list of function names and the parameters to call the functions.
- choose optimal plan to use minimal functions to answer the user query.
Function Map:
<FUNCTION_MAP>
Response Format:
<FUNCTION_SELECTOR_RESPONSE_FORMAT>
"""

DATA_INTERPRETER_STATIC_QUERY = """
You are an interpreter who takes multiple data types and makes it into human readable format.
Given: list of data that was fetched in response to the user query.
Task:
- interpret the data 
- return the response in a human readable format.
Input Data Structure:
<INPUT_DATA_STRUCTURE>
"""

CONTINUE_FUNCTION_SELECTOR_QUERY = """
Initial User Query: <INITIAL_USER_QUERY>
Completed Function: <COMPLETED_FUNCTION>
Total Functions Called: <TOTAL_FUNCTIONS_CALLED>
Task: Select the next function to call.
"""

def get_single_function_selector_static_query(functionMap: dict[str, Any], responseFormat: str) -> str:
    return (SINGLE_FUNCTION_SELECTOR_STATIC_QUERY
    .replace("<FUNCTION_MAP>", "\n".join([f"{function_name}: {function_description}" for function_name, function_description in functionMap.items()]))
    .replace("<FUNCTION_SELECTOR_RESPONSE_FORMAT>", responseFormat))

def get_all_functions_selector_static_query(functionMap: dict[str, Any], responseFormat: str) -> str:
    return (ALL_FUNCTIONS_SELECTOR_STATIC_QUERY
    .replace("<FUNCTION_MAP>", "\n".join([f"{function_name}: {function_description}" for function_name, function_description in functionMap.items()]))
    .replace("<FUNCTION_SELECTOR_RESPONSE_FORMAT>", responseFormat))

def get_data_interpreter_static_query(inputDataStructure: str) -> str:
    return (DATA_INTERPRETER_STATIC_QUERY
    .replace("<INPUT_DATA_STRUCTURE>", inputDataStructure))

def get_raw_data_query(rawData: RawData) -> str:
    return (f"Raw Data: {rawData.datas.model_dump_json()}")

def get_user_query(user_query: str) -> str:
    return (f"User Query: {user_query}")

def get_continue_function_selector_query(user_query: str, functionName: str, count: int) -> str:
    return (CONTINUE_FUNCTION_SELECTOR_QUERY
    .replace("<INITIAL_USER_QUERY>", user_query)
    .replace("<COMPLETED_FUNCTION>", functionName)
    .replace("<TOTAL_FUNCTIONS_CALLED>", count))