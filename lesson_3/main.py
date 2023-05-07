from flask import Flask, request
from random import randint
from dataclasses import dataclass
from typing import Union
import re

app = Flask(__name__)

menu_items = {}
menu_links = """
          <li><a href="/register_user">Student registration</a></li>
          <li><a href="/select_course">Course selection</a></li>
          <li><a href="/get_grade">Get grade</a></li>"""

top = """
<html>
  <header><h1>Welcome</h1></header>
  <body>
    </br>
    <div>
"""
bottom = f"""
    </div>
    <div>
        </br></br>
        <ul>
{menu_links}
        </ul>
    </div>
  </body>
</html>
"""

def add_menu(func):
    print("inside add")
    def menu_wrapper(*args, **kwargs):
            return top + func(*args, **kwargs) + bottom
    return menu_wrapper


class Course(): 
    def __init__(self, course_id: str, name: str) -> None:
        self.id = course_id
        self.name = name

    def __repr__(self):
            return f"""
                <div>
                <input type="radio" id="{self.id}" name="course_name" value="{self.name}">
                <label for="{self.id}">{self.name}</label>
                </div>
            """
    
@dataclass
class User():
    name: str = ''
    language: str = ''
    course: str = ''
    grade: int = 0

    def __init__(self, name='', language=''):
        self.name = name
        self.language = language

    def choose_course(self, course: Course):
        self.course = course

    @staticmethod
    def get_grade():
        return randint(1, 12)

class ProgrammingCourses():
    def __init__(self) -> None:
        self.courses = {}
        self.student = None
    
    def add_course(self, course: Course):
        self.courses[course.id] = course
    
    def get_course_id_by_name(self, course_name: str) -> Union[str, ValueError]:
        correct_id = ''
        for course_id, course in self.courses.items():
            if course_name == course.name:
                correct_id = course_id
                break
        
        print(f"Correct id: {correct_id}")
        if not correct_id:
            raise ValueError("Wrong course name!")
        return correct_id
    
    def get_html_radio_list(self) -> str:
        html = '<fieldset><legend>Select a course:</legend>'
        for _, course in self.courses.items():
            html = html + repr(course)
        html = html + '</fieldset>'
        
        return html
    
    def show_courses_form(self):
        return f"""
        <h3>Programming courses registration</h3>
        <form action="/select_course" method="POST">
        {self.get_html_radio_list()}
            <div>
            <button type="submit">Submit</button>
            </div>
        </form>"""

    def show_user_form(self):
        return f"""
            <h3>Programming courses registration</h3>
            
            <form action="/register_user" method="POST">
                <div>
                    <label for="user_name">Please enter new student's name</label>
                    <input name="name" id="user_name" value="Enter user name" />
                </div>
                <div>
                    <label for="lang">Choose a language:</label>

                    <select name="langs" id="langs">
                    <option value="ukr" selected>Ukrainian</option>
                    <option value="eng">English</option>
                    </select>
                </div>
                <button>Register</button>
            </form>  
        """
    
    def create_user(self, request):
        if not self.student:
            try:
                user_name = request.form.get('name')
                self.validate_text_value(user_name)
                
                user_lang = request.form.get('langs')
                self.validate_text_value(user_lang)

                self.student = User(name=user_name, language=user_lang)
                print(self.student)

            except ValueError as e:
                return 'Wrong data! User cannot be created.' + str(e)
            except TypeError as e:
                return 'Wrong data! User name and language should be specified!'
            return 'Registred!'
        else:
            return 'You have been already registrated here!'

    def select_course(self, request):
        if not self.student:
            return 'Please register yourself before trying to select a course!'

        try:
            selected_course = str(request.form.get('course_name'))
            print(f"Selected course: {selected_course}")
            course_id = self.get_course_id_by_name(selected_course)
        except ValueError as e:
            return 'Not a valid course or it is not available yet!' + str(e)
        
        self.student.choose_course(self.courses[course_id])

        return 'Good choice!'

    def get_student_grade(self):
        if not self.student:
            return 'Please register yourself before trying to select a course!'

        return f"Your mark is: {self.student.get_grade()}"
    
    def validate_text_value(self, value):
        pattern = re.compile("^[a-zA-Z]+$")
        if not pattern.match(value):
            raise ValueError("Wrong value! Allowed only alphabet symbols")


programming_courses = ProgrammingCourses()
programming_courses.add_course(Course('python_basic', 'Python Basic'))
programming_courses.add_course(Course('python_pro', 'Python Pro'))
programming_courses.add_course(Course('python_guru', 'Python Guru'))


@app.route("/register_user", methods=("POST","GET"), endpoint='register_user')
@add_menu
def register_user():
    if request.method == 'POST':
        return programming_courses.create_user(request)
    else:
        return programming_courses.show_user_form()

@app.route("/select_course", methods=("POST","GET"), endpoint='select_course')
@add_menu
def select_course():
    if request.method == 'POST':
        return programming_courses.select_course(request)
    else:
        return programming_courses.show_courses_form()

@app.route("/get_grade", methods=("GET",), endpoint='get_grade')
@add_menu
def get_mark():
    return programming_courses.get_student_grade()


@app.errorhandler(404)
def page_not_found(error):
    return 'Wrong URL'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
