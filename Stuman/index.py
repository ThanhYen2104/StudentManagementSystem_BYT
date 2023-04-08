from flask import render_template, request, redirect, url_for, session
from StudentManagementSystem_BYT.Stuman import app, models, login
from StudentManagementSystem_BYT.Stuman.admin import *
from flask_login import login_user, logout_user
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
def common_response():
    return {
        'grade': Grade.query.all()
    }


@login.user_loader
def user_load(user_id):
    return models.get_user_by_id(user_id=user_id)


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
            return redirect(url_for('login'))
    return render_template('register.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def login():
    err_msg = ""
    if request.method.__eq__('GET'):
        username = request.form['username']
        password = request.form['password']
        user = models.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/students")
def man_Student():
    students = models.get_students()
    return render_template("student.html", students=students)


@app.route("/student/<int:student_id>", methods=['GET', 'POST'])
def student_info(student_id):
    student = models.get_student_by_id(student_id)
    if request.method.__eq__('POST'):
        student_id.name = request.form['name']
        student_id.gender = request.form['gender']
        student_id.birthday = request.form['birthday']
        student_id.address = request.form['address']
        student_id.contact_1 = request.form['contact_1']
        student_id.email = request.form['email']
        db.session.commit()
        return redirect(url_for('student_info', student=student))
    else:
        return render_template('student.html', student=student)


@app.route("/class/<int:class_id>")
def man_Class(class_id):
    classes = models.get_class_by_id(class_id)
    return render_template("classes.html", classes=classes)


@app.route("/subject")
def man_Subject():
    return render_template("subject.html")


if __name__ == '__main__':
    from StudentManagementSystem_BYT.Stuman.admin import *

    app.run(debug=True)
