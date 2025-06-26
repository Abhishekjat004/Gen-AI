# generative ai module import kar ra hu
import google.generativeai as genai

# web page request karne ke liye module import kar ra hu
import requests as request

from google.genai import types

#  ye meri api key hai
client = genai.configure(api_key="YOUR API KEY")

# konsa model use kar ra hu
# model = genai.GenerativeModel("gemini-2.0-flash")

# Manual history for chat context
History = []




# External functions for various tasks
def sum(a,b):
    return a + b



def is_prime(a):
    if a <= 1:
        return False
    for i in range(2, int(a**0.5) + 1):
        if a % i == 0:
            return False
    return True



def getcrypto_price(currency_name):
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={currency_name}'
    response = request.get(url)
    return response.json()



# Details of external functions for eg what function does and what parameters it takes for better understanding
# Function Declarations describe the function's name, parameters, and purpose to the model.
# These declarations help the model understand how to use these functions when generating responses.
# we want that kind of format   name : sum
                            #   args : {a,b} 

sum_Declaration = {
    "name": "sum",
    "description": "Calculate the sum of two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "integer",
                "description": "this is the first number that going to be added",
            },
            "b": {
                "type": "integer",
                "description": "this is the second number that going to be added",
            }
        },
        "required": ["a","b"],
    },
}

is_prime_Declaration = {
    "name": "is_prime",
    "description": "Determine Given number is a prime number or not",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "integer",
                "description": "this is the first number that going to be added",
            }
        },
        "required": ["a"],
    },
}

getcrypto_price_Declaration = {
    "name": "getcrypto_price",
    "description": "Get the current price of a cryptocurrency",
    "parameters": {
        "type": "object",
        "properties": {
            "currency_name": {
                "type": "string",
                "description": "Name of the cryptocurrency to get the price for (e.g., bitcoin, ethereum)",
            }
        },
        "required": ["currency_name"],
    },
}
 



# ek dictionary bana raha hu kyuki jab sum function ko call kiya jayega to sum function call hoga
available_tools = {
    "sum": sum,      # jo key me sum likha hai vo actually me string hai or jo value hai vo function hai. 
                              #or jab apan kisi function ko call kar re hai to vo string ki format me hai to usse map karna hoga
    "is_prime": is_prime,
    "getcrypto_price": getcrypto_price
}







def Chatting(userProblem):
    # Append user input to history
    History.append({
        "role": "user",
        "parts": [userProblem]
    })
    
    model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools = [
    {
        "function_declarations": [
            sum_Declaration,
            is_prime_Declaration,
            getcrypto_price_Declaration
        ]
    }
    ],
    system_instruction="""You are a helpful assistant that give answer of userProblem and u have some additional functionality 
    that you can perform various tasks such as calculating sums, checking if numbers are prime, and fetching cryptocurrency prices. 
    if user ask some general question then u can give also answer those general question and if user ask some specific question related to
    sum, prime number, or cryptocurrency prices then you can use the tools that are available to you.
    You can use the tools to perform calculations, check prime numbers, and fetch cryptocurrency prices."""
    )
    while True:
        # Generate response from model using full history
        response = model.generate_content(contents=History)

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"Function to call: {function_call.name}")
            args = dict(function_call.args)  # 👈 Convert to dict
            print(f"Arguments: {args}")

            fun_call = available_tools[function_call.name]
            # print(fun_call)
            result = fun_call(**args)            # ye dekho yaha store ho ra hai vo string jo function ka naam hai 
                                          # ye jayega upar or  avialable tools me dekhega or function ko call karega
                  # yha function ka output aake store ho jayega.

            # print(f"Function result: {result}")

            # # Create a function response part
            # function_response_part = types.Part.from_function_response(
            # name=function_call.name,
            # response={"result": result},
            # )

            # LLM model ne jo function ko call karne ke liye bola hai usse history me save kara ra hu
            History.append({
            "role": "model",
            "parts": [response.candidates[0].content.parts[0].function_call]
            })


            # result ko history me store kar raha hu or jo bi function ka output hai vo hi result hai
            History.append({
            "role": "user",
            "parts": [f'function_result: {result}'],
            })
            
        else:
            # agar user general question puchta hai or koi function call nahi hota hai to else part me aake result print kara dega 
            #or context ke liye history me store kara de ra hu
            History.append({
            "role": "model",
            "parts": [response.text]
            })
            print("No External function call found in the response.")
            print("\nGemini:", response.text)
            break


    

# Main function
def fun():
    while True:
        userProblem = input("Ask me anything (type 'exit' to quit) --> ")
        if userProblem.lower() == "exit":
            print("Goodbye!")
            break
        Chatting(userProblem)
# Start chat
fun()

