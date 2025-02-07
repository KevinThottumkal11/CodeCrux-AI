"""This a bot called CodeCruxGPT which answers your questions and queries related to programming or general computer science.

The bot is capable of answer ing your questions and also helps to debug and find errors in your code. It also helps you to 
prepeare for you programming exmans by creating mock questions for you.

Kevin Binu Thottumkal, Mohawk College, 15 November 2024"""

from openai import OpenAI
import os
from dotenv import load_dotenv

client = OpenAI(os.getenv('OPENAI_API_KEY'))

# holds the chat history
chat_history = [];

def classify_utterance(utterance):
    """This function is used to classify the user query into different categories.
    
    OpenAI completion API is used to categorize the user query.
    gpt-3.5-turbo-instruct model is used here."""

    prompt = f"""Classify the following utterance that are related to programming or computer science into one of the given categories:
    - fundamental_questions: For utterances that ask for explanation or extra informations about fundamental concepts of programming or programming languages or computer science.
    - debug_code: For utterances that focuses on identifying, debugging, fixing code errors, or optimizing the performance of code.
    - questions_request: For utterances that ask for programming-related practice questions or exercise questions for exams or just for practising or training.
    - other_topic: For utterances that are not related to programming or computer science.
    
    Utterance: {utterance}
    
    Only give one of the category name as the response."""

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=20,
        temperature=0.5,
    )

    # print(response.choices[0].text)

    return response.choices[0].text

def get_chat_context(chat_history):
    """This functions is used to get the context of the chat between the user and the bot.
    THe last 5 conversations are provided for the context."""

    if not chat_history:
        return ""
    
    chat_context = ""
    for chat in chat_history[-5:]:  # last 5 conversations
        if chat["role"] == "user":
            role = "User"
        else:
            role = "Assistant"
        
        chat_context += f"{role}: {chat["content"]}"

    return chat_context

def query_response(category, utterance, chat_history):
    """This function is used to create a response for the user query based on the category in which the user query falls on.
    Prompt engineering techniques is used to create a response for the different categories. The prevoius 5 conversation are provided as context to generate response using Prompt engineering.
    
    OpanAI chat API is used here to create a response."""

    chat_context = get_chat_context(chat_history)

    if category.strip() == "fundamental_questions":
        prompt = f""""You are a very helpful programming mentor. Explain the programming question or concept in a very simple way. Use examples or analogies where needed. Give a very clear and beginner-friendly explanation in a professional and friendly response. Also check the previous chat history to know if the user is asking questions regarding a code or concepts from previous conversations.
        
        Previous chat history: {chat_context}

        Current query: {utterance}"""

    elif category.strip() == "debug_code":
        prompt = f"""You are a very helpful programming mentor. Explain how to debug and fix code errors in a very simple way. Use examples or analogies where needed. Give a very clear and step-by-step guidance in a very professional and friendly response. If the user asks to find an error and if the code is not provided check the previous chat history for any code to debug.
        
        Previous chat history: {chat_context}

        Current query: {utterance}"""

    elif category.strip() == "questions_request":
        prompt = f"""You are a very helpful programming mentor. Create suitable questions or coding exercise based on the request with appropriate difficulty. Also provide some hints for the coding exercises if necessary. Also check the previous chat history for any connections to the current query.
        
        Previous chat history: {chat_context}

        Current query: {utterance}"""

    elif category.strip() == "other_topic":
        prompt = f"""You are a very helpful programming mentor focused on programming questions. If the query is a greeting or something like that greet back. Explain why the query is not related to programming or computer science in a very polite manner and let them know that you can answer questions related to programming or computer science if the query is not a greeting message or anything like that. 
        
        Current query: {utterance}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": utterance}
        ],
        temperature=0.7,
        max_tokens=400
    )

    # print(response.choices[0].message.content)

    return response.choices[0].message.content

def understand(utterance):
    """This function is used to understand the user utterance. There is a help command added here that gives extra information about the bot.
    And it is used to to classify the utterance using the classify_utterance function."""
    # Help Command
    if utterance.lower().strip() == ".help":
        return "help"
    
    try:
        return classify_utterance(utterance)
    except Exception as e:
        print(f"Error : {e}")
        return "error"
    
def generate(intent, utterance):
    """This functions analuzes the user intent and provide appropriate response.
    It gets response using the query_response function call. This function also adds the conversation to the chat history."""
    # https://stackoverflow.com/questions/74711107/openai-api-continuing-conversation-in-a-dialogue
    if intent == "help":
        return """
        ***CodeCruxGPT Bot***
        I can answer your programming related questions and I can also help you debug your code.
        
        Example queries:
        - What are dictionaries in Python
        - Can you find the error in my code: [your code]
        - Give me a coding exercise question about Java to practice for my midterm.
        """
    
    if intent == "error":
        return "I'm sorry! I didn't quite understand that. Can you please rephrase your question or provide more details?"
    
    try:
        response = query_response(intent, utterance, chat_history)

        chat_history.append({
            "role": "user",
            "content": utterance
        })

        chat_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    except Exception as e:
        print(f"Error : {e}")
        return "I'm sorry! There was an error processing your request. Please try again."
    
def main():
    """Main method for the CodeCruxGPT bot and implments a bot sessions in the shell."""
    print("Hello! I'm your CodeCrux Bot. I can help you with programming questions and help to debug your code. I can also help you for preparing for you programming exams with mock exercise questions")
    print("Type '.help' to know what exactly I can do.")
    print("Type 'goodbye' to exit.\n")

    while True:
        utterance = input(">>> ").strip()
        if utterance.lower() == "goodbye":
            break

        intent = understand(utterance)
        response = generate(intent, utterance)
        print(response)
        print()

    print("Goodbye! Have a great day!")

if __name__ == "__main__":
    main()