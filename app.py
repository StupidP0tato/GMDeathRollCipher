from flask import Flask, render_template_string
import random

app = Flask(__name__)

# Function to read words from the cipher.txt file
def read_words_from_file():
    try:
        with open("cipher.txt", "r") as file:
            words = [line.strip() for line in file.readlines()]
        return words
    except FileNotFoundError:
        return ["Error: cipher.txt not found"] * 20

# Generate randomized numbers
def generate_randomized_numbers():
    numbers = list(range(1, 21))  # 1 to 20
    random.shuffle(numbers)
    return numbers

# Route for the main page
@app.route("/")
def display_matrix():
    numbers = generate_randomized_numbers()
    words = read_words_from_file()

    # Create the 20x2 matrix
    matrix = [(numbers[i], words[i] if i < len(words) else '') for i in range(20)]

    # Simple HTML table structure
    html = '''
    <html>
    <head><title>Random Matrix</title></head>
    <body>
        <h1>Randomized Numbers and Words</h1>
        <table border="1" cell padding="10">
            <tr><th>Number</th><th>Word</th></tr>
            {% for row in matrix %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
            </tr>
            {% end for %}
        </table>
    </body>
    </html>
    '''

    return render_template_string(html, matrix=matrix)

if __name__ == "__main__":
    app.run(debug=True)
