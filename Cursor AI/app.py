# app.py
# Import necessary libraries
import subprocess                    # For executing Terminal/shell commands 
import platform                      # For detecting the platform. so LLM Model can be giving Platform specific commands to external functions
import google.generativeai as genai  # For using Gemini LLM model
from flask import Flask, request, jsonify, render_template      # Flask for web framework
from dotenv import load_dotenv                                  # For loading environment variables from .env file          
import os                                                       # For accessing environment variables



load_dotenv()   # Load environment variables from .env file
# It's crucial to get the API key from environment variables for security reasons.
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in the .env file.")
#  Gemini API
genai.configure(api_key=api_key)


app = Flask(__name__)

# Detect current platform (e.g., 'linux', 'windows',macOS)
current_platform = platform.system().lower()

# History to store past interactions to maintain context
History = []


# Function to execute shell/terminal commands
def execute_command(command):
    try:
        if current_platform == 'windows':
            # Use PowerShell with explicit -Command
            powershell_command = ["powershell", "-Command", command]
            result = subprocess.run(powershell_command, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.stderr:
            return f"Error: {result.stderr.strip()}"
            
        # 👇 Check if file was written, then read and return its content
        written_files = []
        for ext in ["index.html", "style.css", "script.js"]:
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file == ext and "calculator" in root.lower():
                        full_path = os.path.join(root, file)
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                code = f.read()
                                written_files.append(f"### `{file}`\n```{file.split('.')[-1]}\n{code}\n```")
                        except Exception as read_err:
                            written_files.append(f"Error reading {file}: {read_err}")

        code_block = "\n\n".join(written_files)
        return f"Success: {result.stdout.strip()}\n\n{code_block}"

    except Exception as e:
        return f"Error: {str(e)}"






# External functions for various tasks


# Details of external functions for eg what function does and what parameters it takes for better understanding
# Function Declarations describe the function's name, parameters, and purpose to the model.
# These declarations help the model understand how to use these functions when generating responses.
execute_command_Declaration = {
    "name": "execute_command",
    "description": "Executes a shell command on the host system and returns the output.",
    "parameters": {
        "type": "object",          # ye batata hai ki parameters ka type kya hai
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute on the host system.",
            }
        },
        "required": ["command"]           # ye batata hai ki command parameter required hai
    },
}
 



# ek dictionary bana raha hu kyuki jab execute_command function ko call kiya jayega to execute_command function call hoga
available_tools = {  
    "execute_command" : execute_command
}



# Serve the HTML frontend
@app.route("/")
def index():
    return render_template("index.html")  # Make sure your frontend is in a /templates folder

# Chat route for frontend POST requests
@app.route("/Chatting", methods=["POST"])

def Chatting():
    userProblem = request.json.get("message")
    if not userProblem:
        return jsonify({"error": "No message received"}), 400
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
            execute_command_Declaration
        ]
    }
    ],
    system_instruction=f""" You are an Website builder expert. You have to create the frontend of the website by analysing the user Input.
        You have access of tool, which can run or execute any shell or terminal command Automatically.
        
        Current user operation system is: {current_platform}
        Give command to the user according to its operating system support bcoz let's imagine this code will run on another platform then LLM
        Model know that on which platform is running the program so give command to user according to user Platform .


        <-- What is your job -->
        1: Analyse the user query to see what type of website the want to build
        2: Give them command one by one to user , step by step
        3: Use available tool executeCommand

        // Now you can give them command in following below points:
        1: First create a folder, Ex: mkdir "calulator"
        2: Inside the folder, create index.html , for eg: touch "calculator/index.html"
        3: Then create style.css , for eg: touch "calculator/style.css"
        4: Then create script.js , for eg: touch "calculator/script.js"
        5: Then write a code in html file
        6: Then write a code in css file
        7: Then write a code in js file

        You have to provide the terminal or shell command to user, they will directly execute it with the help of external function 
        execute_command.
        If Operating System is Window and you want to write a code in html, css or js file then you can use Set-Content command in PowerShell or echo command in Linux.
        Example of writing HTML to a file:
        @'
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>My First Page</title>
        </head>
        <body>
        <h1>Welcome to My Website</h1>
        <p>This is a sample paragraph.</p>
        <button>Click Me</button>
        </body>
        </html>
        '@ | Set-Content -Path "calculator\\index.html"

        Example of writing CSS:
        @'
        body (
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        color: #333;
        margin: 0;
        padding: 20px;
        )
        '@ | Set-Content -Path "calculator\\style.css"

        Example of writing JS:
        @'
        function updateDisplay() (
            const display = document.querySelector(".screen");
            display.value = "123";
            )
            updateDisplay();
            '@ | Set-Content -Path "calculator\\script.js"




        If Operating System is MacOS and you want to write a code in html, css or js file then you can use Set-Content command in PowerShell or echo command in Linux.
        Example of writing HTML to a file:
        cat << 'EOF' > "calculator/index.html"
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>My First Page</title>
        </head>
        <body>
        <h1>Welcome to My Website</h1>
        <p>This is a sample paragraph.</p>
        <button>Click Me</button>
        </body>
        </html>
        EOF

        Example of writing CSS:
        cat << 'EOF' > "calculator/style.css"
        body (
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        color: #333;
        margin: 0;
        padding: 20px;
        )
        EOF

        Example of writing JS:
        cat << 'EOF' > "calculator/script.js"
        function updateDisplay() (
            const display = document.querySelector(".screen");
            display.value = "123";
            )
            updateDisplay();
            EOF
            ALWAYS use PowerShell format and syntax.
                         
        """
    )
    try:
        while True:
            # Generate response from model using full history
            response = model.generate_content(contents=History)

            # Check for a function call
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function to call: {function_call.name}")
                args = dict(function_call.args)  #  Convert to dict
                print(f"Arguments: {args}")

                fun_call = available_tools[function_call.name]
                # print(fun_call)
                result = fun_call(**args)            # ye dekho yaha store ho ra hai vo string jo function ka naam hai 
                                                     # ye jayega upar or  avialable tools me dekhega or function ko call karega
                                                     # yha function ka output aake store ho jayega.

                # print(f"Function result: {result}")

           
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
                History.append({
                    "role": "model",
                    "parts": [response.text]
                })
                break
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
