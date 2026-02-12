from typing import Any
from pydantic import BaseModel, ConfigDict

# Response format for selected functions
class FunctionCall(BaseModel):
    model_config = ConfigDict(extra="allow")

    functionName: str
    description: str
    parameters: dict[str, Any]
    check_results_before_next: bool

    # only for the final response
    # results: str

    @classmethod
    def get_description(cls) -> str:
        return """
        functionName: exact function name without braces or parameters.
        description: Why this function is needed to answer the user query.
        parameters: Parameters for the function.
        check_results_before_next: Boolean indicating if the results of the function call should be checked before calling the next function.
        """

class SingleFunctionSelectorResponse(BaseModel):
    function: FunctionCall
    enough: bool

    @classmethod
    def get_description(cls) -> str:
        return f"""
        function: FunctionCall instance for what function to call.
        enough: Boolean indicating if the data gathering is complete.
        Structure of SingleFunctionSelectorResponse instance:
        {FunctionCall.get_description()}
        """

# Response format for Function Selector
class IdentifiedIntent(BaseModel):
    functions: list[FunctionCall]
    enough: bool

    @classmethod
    def get_description(cls) -> str:
        return f"""
        functions: List of functions to run in exact order. Maximum number of functions to run is 5.
        enough: Boolean indicating if the data gathering is complete.

        Structure of Functions Instance:  
        {FunctionCall.get_description()}
        Do Not include any other parameters/variables.
        """

    def how_many_functions_left(self, function_index: int) -> int:
        return len(self.functions) - function_index - 1

# Input format for Data Interpreter
class RawData(BaseModel):
    datas: list[FunctionCall]

    @classmethod
    def get_description(cls) -> str:
        return f"""
        datas: List of function calls performed and their responses.
        structure of datas instance :
        {FunctionCall.get_description()}
        results: response from this Function Call
        """

# Functions List Structure
class FunctionItem(BaseModel):
    functionName: str
    description: str
    parameter_structure: dict[str, Any]

    @classmethod
    def get_description(cls) -> str:
        return f"""
        functionName: exact function name without braces or parameters.
        description: What this function does and what kind of data it can return.
        parameter_structure: Structure of the parameters for the function. This is a dict of keys and values mentioning the type of each parameter.
        """