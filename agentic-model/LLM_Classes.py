from typing import Any
from pydantic import BaseModel, ConfigDict

class FunctionCall(BaseModel):
    model_config = ConfigDict(extra="allow")

    functionName: str
    description: str
    parameters: list[Any]
    check_results_before_next: bool

    # only for the final response
    # results: str

    @classmethod
    def get_description(cls) -> str:
        return """
        functionName: exact function name without braces or parameters.
        description: Why this function is needed to answer the user query.
        parameters: list of parameters for the function.
        check_results_before_next: Boolean indicating if the results of the function call should be checked before calling the next function.
        """

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
