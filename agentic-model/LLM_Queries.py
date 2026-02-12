from typing import Any
from LLM_Classes import FunctionCall, RawData, IdentifiedIntent

FUNCTION_SELECTOR_QUERY = """
You are a helpful assistant that helps to select the function to call based on the intent of the user query.
You are given a list of functions and a user query.
You need to select the function that is most relevant to the user query.
You need to return the function name and the parameters to call the function.
You can return a lust of multiple functions with their parameters to call but the call must be complete within 5 function calls.

Here is the list of functions:
<FUNCTIONS_LIST>

Here is the response format:
<FUNCTION_SELECTOR_RESPONSE_FORMAT>

Here is the User's Query:
<USER_QUERY>
"""

DATA_INTERPRETER_QUERY = """
You are a helpful assistant that helps to interpret the data returned by the functions.
You are given a list of data that was fetched in response to the user query.
You need to interpret the data and return the response in a human readable format.
You need to return the response in a human readable format.

Here is the input data structure:
<INPUT_DATA_STRUCTURE>

The response should be a humanized understanding of the data in the context of the user query.

Here is the raw data:
<RAW_DATA>
"""

def get_function_selector_query(functions: list[Any], user_query: str) -> str:
    return (FUNCTION_SELECTOR_QUERY
    .replace("<FUNCTIONS_LIST>", "\n".join([function.model_dump_json() for function in functions]))
    .replace("<FUNCTION_SELECTOR_RESPONSE_FORMAT>", IdentifiedIntent.get_description())
    .replace("<USER_QUERY>", user_query))

def get_data_interpreter_query(raw_data: RawData) -> str:
    raw_data_json = []
    for data in raw_data.datas:
        raw_data_json.append(data.model_dump_json())
    return (DATA_INTERPRETER_QUERY
    .replace("<INPUT_DATA_STRUCTURE>", RawData.get_description())
    .replace("<RAW_DATA>", raw_data_json))