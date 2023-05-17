from flask import Flask, render_template, request, g
from random import randint
from dataclasses import dataclass
from typing import Union
import re
import sqlite3

DATABASE = '/Users/yaroslav.lvivskyi/Documents/GitHub/PyLessons/lesson_4/user.db'

app = Flask(__name__)

menu_items = {}
menu_links = """
          <li><a href="/login">Login</a></li>
          <li><a href="/register_user">Student registration</a></li>
          <li><a href="/select_course">Course selection</a></li>
          <li><a href="/get_grade">Get grade</a></li>
          <li><a href="/logout">Logout</a></li>"""

bottom = f"""
    <div>
        </br></br>
        <ul>
{menu_links}
        </ul>
    </div>
  </body>
</html>
"""


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db


def add_menu(func):
    def menu_wrapper(*args, **kwargs):
            return func(*args, **kwargs) + bottom
    return menu_wrapper


class ProgrammingCoursesException(Exception):
    def __init__(self, msg: str):
        self.error_msg = msg
    def __str__(self):
        return repr(self.error_msg)


class Course(): 
    def __init__(self, course_id: str, name: str) -> None:
        self.id = course_id
        self.name = name


class UserModel():
    def create_user(self, user_name: str, user_lang: str) -> Union[bool, ProgrammingCoursesException]:
        try:
            sql = f"INSERT INTO user(Name, Language, Course, Grade) VALUES('{user_name}', '{user_lang}', Null, Null);"
            cur = get_db().cursor()
            cur.execute(sql)
            get_db().commit()
        except sqlite3.Error as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise ProgrammingCoursesException('User with this name is already registered in the system. Please use /login form.')
            raise ProgrammingCoursesException(f'Please try again later. DB error code: {e.sqlite_errorcode} error: {e.sqlite_errorname}')
        finally:
            cur.close()
        return True
    
    def select_course(self, course_id: str, student_name: str) -> Union[bool, ProgrammingCoursesException]:
        try:
            sql = f"UPDATE user SET Course='{course_id}' WHERE Name = '{student_name}';"
            cur = get_db().cursor()
            cur.execute(sql)
            get_db().commit()
        except sqlite3.Error as e:
            raise ProgrammingCoursesException(f'Please try again later. DB error code: {e.sqlite_errorcode} error: {e.sqlite_errorname}')
        finally:
            cur.close()
        return True
        
    def set_grade(self, grade: int, student_name: str) -> Union[bool, ProgrammingCoursesException]:
        try:
            sql = f"UPDATE user SET Grade={grade} WHERE Name = '{student_name}';"
            cur = get_db().cursor()
            cur.execute(sql)
            get_db().commit()
        except sqlite3.Error as e:
            raise ProgrammingCoursesException(f'Please try again later. DB error code: {e.sqlite_errorcode} error: {e.sqlite_errorname}')
        finally:
            cur.close()
        return True
    
    def get_user(self, user_name: str) -> Union[dict, ProgrammingCoursesException]:
        user = {}
        try:
            sql = f"SELECT * FROM user WHERE Name='{user_name}'"
            cur = get_db().cursor()
            cur.execute(sql)
            user = cur.fetchone()
            print(f"User from DB: {user}")
        except sqlite3.Error as e:
            raise ProgrammingCoursesException(f'Please try again later. DB error code: {e.sqlite_errorcode} error: {e.sqlite_errorname}')
        finally:
            cur.close()
        return user
    

@dataclass(init=True)
class User():
    name: str = ''
    language: str = ''
    course: Course = None
    grade: int = 0


class ProgrammingCourses():
    def __init__(self, user_model: UserModel) -> None:
        self.courses = {}
        self.student = None
        self.user_model = user_model
    
    def add_course(self, course: Course):
        self.courses[course.id] = course

    def get_course_id_by_name(self, course_name: str) -> Union[str, ProgrammingCoursesException]:
        correct_id = ''
        for course_id, course in self.courses.items():
            if course_name == course.name:
                correct_id = course_id
                break
        
        print(f"Correct id: {correct_id}")
        if not correct_id:
            raise ProgrammingCoursesException('Not a valid course or it is not available yet!')
        
        return correct_id
    
    def create_user(self, request) -> Union[bool, ProgrammingCoursesException]:
        if self.student:
            raise ProgrammingCoursesException('You are already registered here!')

        user_name = request.form.get('name')
        self.validate_text_value(user_name)
        
        user_lang = request.form.get('langs')
        self.validate_text_value(user_lang)

        self.user_model.create_user(user_name, user_lang)

        self.student = User(name=user_name, language=user_lang)
        print(self.student)

        return True

    def select_course(self, request) -> Union[bool, ProgrammingCoursesException]:
        if not self.student:
            raise ProgrammingCoursesException('Please register yourself before trying to select a course!')

        selected_course = str(request.form.get('course_name'))
        print(f"Selected course: {selected_course}")
        course_id = self.get_course_id_by_name(selected_course)

        self.user_model.select_course(course_id=course_id, student_name=self.student.name)
        self.student.course = programming_courses[course_id]

        return True

    def get_student_grade(self) -> Union[bool, ProgrammingCoursesException]:
        if not self.student:
            raise ProgrammingCoursesException('Please register yourself before trying to get a grade!')

        if not self.student.grade:
            grade = randint(1, 12)
            self.user_model.set_grade(grade=grade, student_name=self.student.name)
            self.student.grade = grade

        return True
    
    def login(self, request) -> Union[bool, ProgrammingCoursesException]:
        if not self.student:

            user_name = request.form.get('name')
            self.validate_text_value(user_name)

            user = self.user_model.get_user(user_name=user_name)

            if user:
                self.student = User(
                    name=user['Name'],
                    language=user['Language'],
                    course=self.courses[user['Course']] if user['Course'] else None,
                    grade=int(user['Grade']) if user['Grade'] else None
                )
                print(f"Student: {self.student}")
                success = True
            else:
                success = False
            print(f"Login was successful: {success}")

            return success
        else:
            return False
        
    @staticmethod
    def validate_text_value(value) -> Union[None, ValueError]:
        if not value:
            raise ProgrammingCoursesException("Empty data is not allowed")
        
        pattern = re.compile("^[a-zA-Z]+$")
        if not pattern.match(value):
            raise ProgrammingCoursesException("Wrong value! Allowed only alphabet symbols")


programming_courses = ProgrammingCourses(UserModel())
programming_courses.add_course(Course('python_basic', 'Python Basic'))
programming_courses.add_course(Course('python_pro', 'Python Pro'))
programming_courses.add_course(Course('python_guru', 'Python Guru'))


@app.route("/register_user", methods=("POST","GET"), endpoint='register_user')
@add_menu
def register_user():
    error_msg = None
    if request.method == 'POST':
        try:
            programming_courses.create_user(request)
        except ProgrammingCoursesException as e:
            error_msg = e.error_msg
    elif request.method == 'GET' and programming_courses.student:
        error_msg = 'You are already registered here!'

    return render_template('register_user.html', user=programming_courses.student, error_msg=error_msg)


@app.route("/select_course", methods=("POST","GET"), endpoint='select_course')
@add_menu
def select_course():
    error_msg = None
    if request.method == 'POST':
        try:
            programming_courses.select_course(request)
        except ProgrammingCoursesException as e:
            error_msg = e.error_msg
    print(f"Error: {error_msg}")
    return render_template('select_course.html', user=programming_courses.student, courses=programming_courses.courses, error_msg=error_msg)


@app.route("/get_grade", methods=("GET",), endpoint='get_grade')
@add_menu
def get_grade():
    error_msg = None

    try:
        programming_courses.get_student_grade()
    except ProgrammingCoursesException as e:
        error_msg = e.error_msg
    return render_template('get_grade.html', user=programming_courses.student, error_msg=error_msg)


@app.route("/login", methods=("GET","POST"), endpoint='login')
@add_menu
def login():
    error_msg = None
    if request.method == 'POST':
        try:
            programming_courses.login(request)
        except ProgrammingCoursesException as e:
            error_msg = e.error_msg
    return render_template('login.html', user=programming_courses.student, error_msg=error_msg)


@app.route("/logout", methods=("GET",), endpoint='logout')
@add_menu
def logout():
    if programming_courses.student:
        programming_courses.student = None
        return render_template('logout.html', success=True)
    else:
        return render_template('logout.html', success=False)
    

@app.errorhandler(404)
def page_not_found(error):
    return 'Wrong URL'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
