from flask import render_template, request
from StudentManagementSystem_BYT.Stuman import app, models


@app.route("/")
def home():
    grade = models.get_grade()
    grade_id = request.args.get('grade_id')
    kw = request.args.get('kw')
    student = models.get_students(kw=kw, grade_id=grade_id)
    return render_template('index.html', grade=grade, student=student)


@app.route("/students")
def man_Student():
    students = models.get_students()
    return render_template("student.html", students=students)


@app.route("/class")
def man_Class():
    return render_template("classes.html")


@app.route("/subject")
def man_Subject():
    return render_template("subject.html")


if __name__ == '__main__':
    from StudentManagementSystem_BYT.Stuman.admin import *

    app.run(debug=True)
