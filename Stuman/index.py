from flask import render_template, request
from StudentManagementSystem_BYT.Stuman import app, models
from flask_admin import Admin

admin = Admin(app, name="BYT EDUCATION ADMINISTRATION", template_mode='bootstrap4')


@app.route("/")
def home():
    grade = models.get_grade()
    return render_template('index.html', grade=grade)


@app.route("/students")
def man_Student():
    return render_template("student.html")


@app.route("/class")
def man_Class():
    return render_template("classes.html")


@app.route("/subject")
def man_Subject():
    return render_template("subject.html")


if __name__ == '__main__':
    app.run(debug=True)
