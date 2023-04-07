from flask import render_template, request, redirect, url_for
from StudentManagementSystem_BYT.Stuman import app, models
import cloudinary.uploader


@app.route("/")
def home():
    grade_id = request.args.get('grade_id')
    classes = models.get_classes(grade_id=grade_id)
    classes_id = request.args.get('classes_id')
    kw = request.args.get('kw')
    student = models.get_students(kw=kw, grade_id=grade_id, classes_id=classes_id)
    return render_template('index.html', student=student, classes=classes)


@app.context_processor
def common_reponse():
    return {
        'grade': Grade.query.all()
    }


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                models.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
            else:
                err_msg = 'Mật khẩu không trùng khớp!'
        except Exception as ex:
            err_msg = 'Hệ thống nhận được lỗi ' + str(ex)
        else:
            return redirect(url_for('home'))
    return render_template('register.html', err_msg=err_msg)


@app.route("/students")
def man_Student():
    students = models.get_students()
    return render_template("student.html", students=students)


@app.route("/student/<int:student_id>")
def student_info(student_id):
    student_id = models.get_student_by_id(student_id)


@app.route("/class")
def man_Class():
    students = models.get_students()
    return render_template("classes.html", students=students)


@app.route("/subject")
def man_Subject():
    return render_template("subject.html")


if __name__ == '__main__':
    from StudentManagementSystem_BYT.Stuman.admin import *

    app.run(debug=True)
