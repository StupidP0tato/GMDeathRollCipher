from flask import Flask, render_template_string, jsonify
import random
import os

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


# Route for the main page (initially displays an empty table)
@app.route("/")
def index():
    html = '''
    <html>
    <head><title>DnD Secret Death Roll</title></head>
    <script>
        // Function to fetch data and update the table when the button is clicked
        function GM_Cipher_Table() {
            fetch("/generate-data")
            .then(response => response.json())
            .then(data => {
                let table = document.getElementById("matrix-table");
                table.innerHTML = "";  // Clear any existing rows

                // Add table header
                let header = table.createTHead().insertRow();
                let th1 = document.createElement("th");
                let th2 = document.createElement("th");
                th1.innerHTML = "Number";
                th2.innerHTML = "Word";
                header.appendChild(th1);
                header.appendChild(th2);

                // Add rows for the numbers and words
                data.forEach(row => {
                    let newRow = table.insertRow();
                    let cell1 = newRow.insertCell(0);
                    let cell2 = newRow.insertCell(1);
                    cell1.innerHTML = row[0];
                    cell2.innerHTML = row[1];
                });
            });
        }

        // Function to fetch a random entry from cipher.txt
        function deathRoll() {
            fetch("/death-roll")
            .then(response => response.json())
            .then(data => {
                document.getElementById("death-roll-result").innerText = data.result;
            });
        }
    </script>
    </head>
    <body>
        <h1>Randomized Numbers and Words</h1>
        <button onclick="GM_Cipher_Table()">Fill Table</button>
        <br><br>
        <table border="1" cellpadding="10" id="matrix-table">
            <!-- Table starts empty -->
        </table>

        <h2>Death Roll</h2>
        <button onclick="deathRoll()">Roll</button>
        <p id="death-roll-result">Result</p>  <!-- This will display the random entry -->
    </body>
    </html>
    '''
    return render_template_string(html)


# Route to generate the data and send it to the frontend (AJAX)
@app.route("/generate-data")
def generate_data():
    numbers = generate_randomized_numbers()
    words = read_words_from_file()
    matrix = [(numbers[i], words[i] if i < len(words) else '') for i in range(20)]

    return jsonify(matrix)


# Route to get a random entry from cipher.txt
@app.route("/death-roll")
def death_roll():
    words = read_words_from_file()
    result = random.choice(words)  # Get a random word
    return jsonify(result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
