import os
from dotenv import load_dotenv

from LLM_Classes import *
from LLM_Queries import *
from LLM_Connectors import *

from SharePoint_Functions import *
from Database_Functions import *
from WikiEndpoints import *

FUNCTION_REGISTRY = {}      
# Function Name : {
#     "function_instance": function_instance,
#     "parameter_structure": { parameter_name: parameter_type },
#     "description": description
# }

def get_api_key():
    load_dotenv()
    gpt_api_key = os.getenv("OPENAI_API_KEY")
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    if not gpt_api_key and not gemini_api_key:
        raise ValueError("No API_KEY not found in environment variables.")
    if gpt_api_key:
        return gpt_api_key, 'gpt'
    if gemini_api_key:
        return gemini_api_key, 'gemini'
    raise ValueError("No API_KEY found in environment variables.")

def select_functions_in_loop(user_query: str) -> RawData:
    """
    Performs the following in loop:
    - Select what function to run
    - Run the function
    - If LLM decides this data is enough, stop the loop and return functions + results
    - If LLM decides this data is not enough, select the next function to run
    - Limit loop to 5 functions to avoid infinite loops
    Arguments:
        user_query (str): The user query to select the functions for.
    Returns (Response):
        RawData: The raw data from the functions.
    """
    enough = False
    limit = 5
    index = 0
    functions_called = []

    static_query = get_single_function_selector_static_query(
        FUNCTION_REGISTRY, 
        SingleFunctionSelectorResponse.get_description()
        )
    api_key, model_type = get_api_key()

    while (not enough) and (index < limit):
        query_to_run = ""
        if index == 0:
            query_to_run = get_user_query(user_query)
        else:
            query_to_run = get_continue_function_selector_query(
                user_query=user_query,
                functionName=functions_called[index-1].functionName,
                count=index+1
            )
        # Decide what function to call
        if model_type == 'gpt':
            gpt_instance = initialize_gpt_instance(api_key)
            response = generate_gpt_response(
                instance=gpt_instance,
                static_query=static_query,
                user_query=query_to_run,
                responseClassVariable=SingleFunctionSelectorResponse,
            )
        elif model_type == 'gemini':
            gemini_instance = initialize_gemini_instance(api_key)
            response = generate_gemini_response(
                instance=gemini_instance,
                static_query=static_query,
                user_query=query_to_run,
                responseClassVariable=SingleFunctionSelectorResponse,
            )
        # Call the function and get the result
        result = run_function(response.function)
        response.function.result = result
        # Append Function Data with Result to the list of functions called
        functions_called.append(response.function)
        if response.enough:
            enough = True
        index += 1
    return RawData(datas=functions_called)

def run_function(function: FunctionCall):
    """
    Runs a function based on the function call.
    Arguments:
        function (FunctionCall): The function call to run.
    Returns (Response):
        The response from the function.
    """
    function_name = function.functionName
    parameters = function.parameters
    try:
        function_instance = FUNCTION_REGISTRY[function_name]["function_instance"]
        response = function_instance(**parameters)
        return response
    except KeyError:
        raise ValueError(f"Function {function_name} not found in the registry.")
    except Exception as e:
        raise ValueError(f"Error running function {function_name}: {e}")

def interpret_data(raw_data: RawData) -> str:
    """
    Interprets the data returned by the functions.
    Arguments:
        raw_data (RawData): The raw data from the functions.
    Returns (Response):
        The interpreted data.
    """
    static_query = get_data_interpreter_static_query(RawData.get_description())
    query = get_raw_data_query(raw_data)
    api_key, model_type = get_api_key()

    try:
        if model_type == 'gpt':
            gpt_model_name = "gpt-4o-mini"
            gpt_instance = initialize_gpt_instance(api_key)
            response = generate_gpt_response(
                instance=gpt_instance,
                static_query=static_query,
                user_query=query,
                responseClassVariable=str,
                model_name=gpt_model_name
            )
        elif model_type == 'gemini':
            gemini_model_name = "gemini-2.5-flash"
            gemini_instance = initialize_gemini_instance(api_key)
            response = generate_gemini_response(
                instance=gemini_instance,
                static_query=static_query,
                user_query=query,
                responseClassVariable=str,
                model_name=gemini_model_name
            )
        return response
    except TypeError as e:
        raise ValueError(f"Error interpreting data (wrong arguments): {e}")
    except Exception as e:
        raise ValueError(f"Error interpreting data: {e}")

"""
How To Run the LLM Agentic Model : 
1. select_functions_in_loop(user_query)
2. interpret_data(raw_data)
"""