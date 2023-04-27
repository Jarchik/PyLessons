from flask import Flask

app = Flask(__name__)

constant = [1, 2, 3]


@app.route("/")
def show_items():
    return f"<h3>Our Items are: {constant}!!!<h3>"


@app.route("/delete_item")
def delete_item():
    ...


@app.route("/add_item")
def add_item():
    ...


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)