import google.generativeai as genai

genai.configure(api_key="YOUR API KEY")

# System prompt
system_instruction = """You are a Data structures and Algorithms mentor which helps students to learn and solving their problems. 
        You are very friendly and helpful. You always try to give the best possible solution to the user problem. Remember one thing,
        you answer only related to Data structures and Algorithms and nothing else. 
        for eg: if a user ask you to another topic then you talk him with rudely and tell him that are you dump or nonsense you know very 
        well that i am answers only related to Data structures and Algorithms then why are u asking me this question. like this sentence
        you give him and talk him with rudely."""

# Create chat object with system instruction
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])
chat.send_message(system_instruction)  # Set system behavior

# Chatting function
def Chatting(userProblem):
    print("\nChatbot is thinking...")
    response = chat.send_message(userProblem)
    print("\nGemini:", response.text)

# Main function
def main_fun():
    while True:
        userProblem = input("Ask me anything related to DSA (type 'exit' to quit) --> ")
        if userProblem.lower() == "exit":
            print("Goodbye!")
            break
        Chatting(userProblem)

# Start the chatbot
main_fun()

