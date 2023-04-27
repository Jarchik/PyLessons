from flask import Flask
from random import randint

app = Flask(__name__)

items = [1, 2, 3]
top = """
<html>
  <header><h1>Items v1</h1></header>
  <body>
    </br>
    <div>
"""
bottom = """
    </div>
    <div>
        </br></br>
        <ul>
          <li><a href="/">Show items</a></li>
          <li><a href="/add_item">Add item</a></li>
          <li><a href="/delete_item">Delete last item</a></li>
        </ul>
    </div>
  </body>
</html>
"""

def add_body_and_menu(func):
    print("inside add")
    def menu_wrapper(*args, **kwargs):
            return top + func(*args, **kwargs) + bottom
    return menu_wrapper


@app.route("/", endpoint='show_items')
@add_body_and_menu
def show_items():
    return f"<h4>Our Items are: {items}<h4>"


@app.route("/delete_item", endpoint='delete_item')
@add_body_and_menu
def delete_item():
    if items:
        return f"<span>Item {items.pop()} was deleted</span></br><span>Our Items are: {items}<span>"
    else:
        return f"<span>Not items in left</span>"


@app.route("/add_item", endpoint='add_item')
@add_body_and_menu
def add_item():
    new_item = randint(1, 9)
    items.append(new_item)
    return f"New item {new_item} was added.</br><span>Our Items are: {items}<span>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
