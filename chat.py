from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Create a chatbot instance
chatbot = ChatBot('BasicBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on the English language
trainer.train('chatterbot.corpus.english')

# Function to handle arithmetic operations
def perform_calculation(input_text):
    try:
        result = eval(input_text)
        return str(result)
    except Exception as e:
        return "Error: {}".format(str(e))

# Function to handle general knowledge questions
def get_general_knowledge_answer(question):
    # You can implement your logic to fetch answers from a knowledge base or use an external API here
    return "I'm sorry, I don't have information on that right now."

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for processing user input
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']

    # Check for specific commands
    if user_input.lower() in ['give me calendar', 'calendar']:
        response = "I'm sorry, I don't have a calendar feature yet."
    elif user_input.lower() in ['give me numbers', 'numbers']:
        response = "Sure, here are some numbers: 1, 2, 3, 4, 5"
    elif any(op in user_input for op in ['+', '-', '*', '/']):
        # Handle arithmetic operations
        response = perform_calculation(user_input)
    else:
        # Use ChatterBot for general conversation
        response = chatbot.get_response(user_input)

    return render_template('index.html', user_input=user_input, response=response)

if __name__ == '__main__':
    app.run(debug=True)
