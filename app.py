from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Access API keys from environment variables
api_key = os.getenv('API_KEY')
app = Flask(__name__)

# Define route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    titles = []  # Initialize titles list

    if request.method == 'POST':
        dropdown1_value = request.form.get('dropdown1')
        dropdown2_value = request.form.get('dropdown2')

        template = f"""I want you to generate me {dropdown1_value} youtube titles 
            on the niche {dropdown2_value}. I want you just list down only the titles and not anything else
            The output should be in the form of
            1. Title1
            2. Title2 
            etc """
        
        llm = ChatOpenAI(openai_api_key=api_key)
        output = llm.invoke(template)
        output = str(output).split('content=')[1]
        output = output.split("'")[1]
        titles = output.split(r"\n")
        for i in titles:
            print(i)
        
        # Return the selected values as JSON to update the page
        return jsonify({
            'dropdown1': dropdown1_value,
            'dropdown2': dropdown2_value,
            'titles': titles  # Pass titles to the template
        })

    return render_template('index.html', titles=titles)  # Pass titles to the template

if __name__ == '__main__':
    app.run(debug=True)
