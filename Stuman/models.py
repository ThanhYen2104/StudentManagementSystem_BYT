from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from StudentManagementSystem_BYT.Stuman import db, app
from datetime import datetime
from enum import Enum as UserEnum
import hashlib


# Chỗ này thực hiện tạo db và phương thức truyền CSDL
class BaseModel(db.Model):
    # __abstract__ dùng cho các bảng kế thừa ==> Không tạo bảng mới khi thực thi
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    STUDENT = 2
    USER = 3


# Tạo bảng mới theo db.Model
class User(BaseModel, UserMixin):
    name = Column(String(100), nullable=False)
    avatar = Column(String(100), default=None)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    student = relationship('Student', uselist=False, backref='User')

    def __str__(self):
        return self.name


# Bảng thông tin năm học
class Semester(BaseModel):
    __tablename__ = 'semester'
    name = Column(String(30), nullable=False)
    key = Column(String(10), nullable=False)
    year_start = Column(DateTime, nullable=False)
    year_end = Column(DateTime, nullable=False)
    student = relationship('Student', backref='semester', lazy=True)
    grade = relationship('Grade', backref='semester', lazy=True)
    classes = relationship('Class', backref='semester', lazy=True)
    subject = relationship('Subject', backref='semester', lazy=True)

    def __str__(self):
        return self.name


# Bảng thông tin khối lớp học
class Grade(BaseModel):
    __tablename__ = 'grade'
    name = Column(String(20), nullable=False)  # Tên lớp
    value = Column(Integer, nullable=False)  # Chỉ số lớp
    description = Column(String(100))  # Mô tả thông tin lớp
    students = relationship('Student', backref='grade', lazy=False)  # Học sinh thuộc lớp
    classes = relationship('Class', backref='grade', lazy=False)
    semester_id = Column(Integer, ForeignKey(Semester.id))

    def __str__(self):
        return self.name


# Bảng thông tin lớp học
class Class(BaseModel):
    __tablename__ = 'class'
    name = Column(String(250), nullable=False)
    student = relationship('Student', backref='class', lazy=True)
    grade_id = Column(Integer, ForeignKey(Grade.id))
    semester_id = Column(Integer, ForeignKey(Semester.id))

    def __str__(self):
        return self.name


# Bảng học sinh
class Student(BaseModel):
    __tablename__ = 'student'
    name = Column(String(100), nullable=False)  # Tên HS
    gender = Column(String(5))  # Giới tính HS
    birthday = Column(DateTime, nullable=False)  # Ngày sinh nhật của HS
    address = Column(String(200))  # Địa chỉ nhà
    contact_1 = Column(Integer, nullable=False)  # Số đt PH
    contact_2 = Column(Integer)  # Số đt PH
    email = Column(String(200))
    image = Column(String(100))  # Hình ảnh của học sinh
    created_date = Column(DateTime, default=datetime.now())  # Ngày tạo thông tin học sinh
    grade_id = Column(Integer, ForeignKey(Grade.id))
    classes_id = Column(Integer, ForeignKey(Class.id))
    semester_id = Column(Integer, ForeignKey(Semester.id))
    user_id = Column(Integer, ForeignKey(User.id))
    stu_sub = relationship('StudentSubject', backref='student', lazy=True)
    mark = relationship('MarkStudent', backref='student', lazy=True)

    def __str__(self):
        return self.name


# Quản lý môn học
class Subject(BaseModel):
    __tablename__ = 'subject'
    name = Column(String(250), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id))
    sub_stu = relationship('StudentSubject', backref='subject', lazy=True)
    mark_column = relationship('MarkColumn', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class StudentSubject(BaseModel):
    __tablename__ = 'student_subject'
    student_id = Column(Integer, ForeignKey(Student.id))
    subject_id = Column(Integer, ForeignKey(Subject.id))
    quantity = Column(Integer, default=0)


class MarkColumn(BaseModel):
    __tablename__ = 'mark_column'
    name = Column(String(150), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id))
    mark_id = relationship('MarkStudent', backref='mark_column', lazy=True)


class MarkStudent(BaseModel):
    __tablename__ = 'mark_student'
    value = Column(Float, nullable=False, default=0)
    student_id = Column(Integer, ForeignKey(Student.id))
    markcol_id = Column(Integer, ForeignKey(MarkColumn.id))


# Viết hàm định nghĩa các chức năng

def get_classes(grade_id=None):
    classes = Class.query
    if grade_id:
        classes = classes.filter(Class.grade_id.__eq__(grade_id))
    return classes.all()


def get_students(kw=None, classes_id=None, grade_id=None):
    student = Student.query
    if kw:
        student = student.filter(Student.name.contains(kw))
    if classes_id and grade_id:
        student = student.filter(Student.grade_id.__eq__(grade_id))
        student = student.filter(Student.classes_id.__eq__(classes_id))
    return student.all()


def get_student_by_id(student_id):
    return Student.query.get(student_id)


def get_student_by_class(class_id=None):
    student = Student.query
    if class_id:
        student.filter(Student.classes_id.__eq__(class_id))
    return student.all()


def get_class_by_id(class_id):
    return Class.query.get(class_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


# def get_mark(mark_id):
#     pass


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
