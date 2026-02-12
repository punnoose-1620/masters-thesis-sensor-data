import os
from dotenv import load_dotenv
from LLM_Classes import FunctionCall, IdentifiedIntent, RawData
from LLM_Queries import get_function_selector_query, get_data_interpreter_query
from LLM_Connectors import generate_gpt_response, generate_gemini_response

from Database_Functions import *
from SharePoint_Functions import *
from WikiEndpoints import *

FUNCTION_REGISTRY = {}      
# Function Name : {
#     "function_instance": function_instance,
#     "parameter_structure": { parameter_name: parameter_type },
#     "description": description
# }

def function_limit_checker(functions: list[FunctionCall]) -> bool:
    return len(functions) <= 5

def append_result_to_instance(instance: FunctionCall, result: str) -> FunctionCall:
    instance.results = result
    return instance

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

def get_function_mapping():
    # TODO: Implement this function with entire function mapping for all sources
    # Functions are mapped with parameters according to FunctionItem class in a json file. 
    # Load Json File
    # Map Function names and instances to FUNCTION_REGISTRY
    functions = []
    return functions

def select_functions(user_query: str) -> IdentifiedIntent:
    """
    Selects the functions to call based on the user query.
    Arguments:
        user_query (str): The user query to select the functions for.
    Returns (Response):
        IdentifiedIntent: The identified intent containing the functions to call.
    Raises:
        ValueError: If no API_KEY is found in environment variables.
    """
    functions = get_function_mapping()
    query = get_function_selector_query(functions, user_query)
    api_key, model_type = get_api_key()
    if model_type == 'gpt':
        gpt_model_name = "gpt-4o-mini"
        response = generate_gpt_response(query, gpt_model_name)
    elif model_type == 'gemini':
        gemini_model_name = "gemini-2.5-flash"
        response = generate_gemini_response(api_key, query, gemini_model_name)
    return response

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

def call_functions(identified_intent: IdentifiedIntent) -> RawData:
    """
    Calls the functions based on the identified intent.
    Arguments:
        identified_intent (IdentifiedIntent): The identified intent containing the functions to call.
    Returns (Response):
        RawData: The raw data from the functions.
    """
    functions_to_call = identified_intent.functions
    for function in functions_to_call:
        try:
            response = run_function(function)
            function.results = response
        except ValueError as e:
            # Function not in registry or error running it
            function.results = f"Error: {e}"
        except TypeError as e:
            # e.g. wrong arguments for **parameters
            function.results = f"Error (wrong arguments): {e}"
        except Exception as e:
            function.results = f"Error: {e}"
    
    if len(functions_to_call) == 0:
        raise ValueError("No functions to call.")
    
    return RawData(datas=functions_to_call)

def interpret_data(raw_data: RawData) -> str:
    """
    Interprets the data returned by the functions.
    Arguments:
        raw_data (RawData): The raw data from the functions.
    Returns (Response):
        The interpreted data.
    """
    data = raw_data.datas
    
    query = get_data_interpreter_query(data)
    api_key, model_type = get_api_key()
    try:
        if model_type == 'gpt':
            gpt_model_name = "gpt-4o-mini"
            response = generate_gpt_response(query, gpt_model_name)
        elif model_type == 'gemini':
            gemini_model_name = "gemini-2.5-flash"
            response = generate_gemini_response(api_key, query, gemini_model_name)
        return response
    except TypeError as e:
        raise ValueError(f"Error interpreting data (wrong arguments): {e}")
    except Exception as e:
        raise ValueError(f"Error interpreting data: {e}")