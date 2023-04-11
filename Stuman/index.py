from flask import render_template, request, redirect, url_for, session
from StudentManagementSystem_BYT.Stuman import app, models, login
from StudentManagementSystem_BYT.Stuman.admin import *
from flask_login import login_user, logout_user, current_user
import cloudinary.uploader


@app.route("/")
def home():
    grade_id = request.args.get('grade_id')
    classes = models.get_classes(grade_id=grade_id)
    classes_id = request.args.get('classes_id')
    kw = request.args.get('kw')
    student = models.get_students(kw=kw, grade_id=grade_id, classes_id=classes_id)
    return render_template('index.html', student=student, classes=classes)


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg1 = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        user_role = request.form.get('user_role')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                models.add_user(name=name, username=username, password=password, email=email,
                                avatar=avatar_path,
                                user_role=user_role)
            else:
                err_msg1 = 'Mật khẩu không trùng khớp!'
        except Exception as ex:
            err_msg1 = 'Hệ thống nhận được lỗi ' + str(ex)
        else:
            return redirect(url_for('user_login'))
    return render_template('register.html', err_msg1=err_msg1)


@app.route("/login", methods=['get', 'post'])
def user_login():
    err_msg2 = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = models.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg2 = 'Tên đăng nhập hoặc mật khẩu không chính xác!'

    return render_template('login.html', err_msg2=err_msg2)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route("/students")
def man_Student():
    grade_id = request.args.get('grade_id')
    classes = models.get_classes(grade_id=grade_id)
    classes_id = request.args.get('classes_id')
    student_id = request.args.get('student_id')
    kw = request.args.get('kw')
    students = models.get_students(kw=kw, classes_id=classes_id, grade_id=grade_id)
    return render_template("student.html", students=students, classes=classes)


@app.route("/user/<int:user_id>", methods=['GET', 'POST'])
def user_info(user_id):
    grade_id = request.args.get('grade_id')
    classes = models.get_classes(grade_id=grade_id)
    classes_id = request.args.get('classes_id')
    student_id = request.args.get('student_id')
    kw = request.args.get('kw')
    students = models.get_students(kw=kw, classes_id=classes_id, grade_id=grade_id)
    user_id = request.args.get('user_id')
    user = models.get_user_by_id(user_id=user_id)
    return render_template("user_info.html", user=user, students=students, classes=classes)


@app.route("/class/<int:class_id>")
def man_Class(class_id):
    grade_id = request.args.get('grade_id')
    classes = models.get_classes(grade_id=grade_id)
    classes_id = request.args.get('classes_id')
    student_id = request.args.get('student_id')
    kw = request.args.get('kw')
    students = models.get_students(kw=kw, classes_id=classes_id, grade_id=grade_id)
    return render_template("classes.html", students=students, classes=classes)


@app.route("/system")
def man_System():
    grade_id = request.args.get('grade_id')
    classes = models.get_classes(grade_id=grade_id)
    classes_id = request.args.get('classes_id')
    student_id = request.args.get('student_id')
    kw = request.args.get('kw')
    students = models.get_students(kw=kw, classes_id=classes_id, grade_id=grade_id)
    return render_template("edit_system.html", classes=classes, students=students)


@app.route('/new-student', methods=['GET', 'POST'])
def add_student():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        address = request.form.get('address')
        contact_1 = request.form.get('contact_1')
        contact_2 = request.form.get('contact_2')
        email = request.form.get('email')
        image_path = None
    try:
        image = request.files.get('image')
        if image:
            res = cloudinary.uploader.upload(image)
            image_path = res['secure_url']
            models.add_student(name=name, gender=gender,
                               birthday=birthday, address=address,
                               contact_1=contact_1, contact_2=contact_2,
                               email=email, image=image_path)
        else:
            err_msg = 'Thông tin đã nhập có vấn đề!'
    except Exception as ex:
        err_msg = 'Hệ thống nhận được lỗi ' + str(ex)
    else:
        return redirect(url_for('home'))


@app.route('/change_class/<int:student_id>', methods=['GET', 'POST'])
def change_class(student_id):
    err_msg = ""
    if current_user.is_authenticated or current_user.user_role.ADMIN:
        if request.method.__eq__('POST'):
            grade_id = request.args.get('grade_id')
            classes = models.get_classes(grade_id=grade_id)
            classes_id = request.args.get('classes_id')
            student_id = request.form.get('student_id')
            kw = request.args.get('kw')
            students = models.get_students(kw=kw, classes_id=classes_id, grade_id=grade_id)
            new_class_id = request.form.get('new_class_id')
        try:
            models.change_class_for_student(student_id=new_class_id)
        except Exception:
            err_msg = 'Chuyển đổi lớp không thành công!'
    else:
        return redirect(url_for('home'))
    return redirect(url_for('man_Student'))


@app.route('/add_marks', methods=['POST'])
def add_marks():
    err = ""
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    mark_column_name = request.form['name']
    mark_value = request.form['value']
    student_subject_id = models.get_markcolumn(student_id=student_id, subject_id=subject_id)
    try:
        mark = models.add_mark(student_id=student_id, subject_id=subject_id, mark_column_name=mark_column_name,
                               mark_value=mark_value)
        db.session.add(mark)
        db.session.commit()
    except Exception:
        err = "Nhập điểm không thành công!"
    return redirect(url_for('man_System'))


@app.context_processor
def common_response():
    return {
        'grade': Grade.query.all(),
        'user': User.query.all(),
        'subject': Subject.query.all()
    }


@login.user_loader
def user_load(user_id):
    return models.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from StudentManagementSystem_BYT.Stuman.admin import *

    app.run(debug=True)
