import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        for content in response.candidates:
            messages.append(content.content)

    
        function_results = []
    
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)   

        if response.function_calls is None:        
            print("Response:")
            print(response.text)
            return
        else:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose = args.verbose)
                if not function_call_result.parts:
                    raise Exception("Parts List is empty")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("There is no FunctionResponse")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("No response Field")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    print("Maximum iterations reached")
    exit(1)
            


if __name__ == "__main__":
    main()