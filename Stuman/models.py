from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from StudentManagementSystem_BYT.Stuman import db, app
from datetime import datetime
import hashlib


# Chỗ này thực hiện tạo db và phương thức truyền CSDL
class BaseModel(db.Model):
    # __abstract__ dùng cho các bảng kế thừa ==> Không tạo bảng mới khi thực thi
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


# Tạo bảng mới theo db.Model
class User(BaseModel, UserMixin):
    name = Column(String(100), nullable=False)
    avatar = Column(String(100), default=None)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(String(20), default='user')

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

    def __str__(self):
        return self.name


# Bảng thông tin lớp học
class Class(BaseModel):
    __tablename__ = 'class'
    name = Column(String(250), nullable=False)
    grade_id = Column(Integer, ForeignKey('grade.id'))
    student = relationship('Student', backref='class', lazy=True)

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
    grade_id = Column(Integer, ForeignKey('grade.id'))
    classes_id = Column(Integer, ForeignKey('class.id'))
    stu_sub = relationship('StudentSbject', backref='student', lazy=True)
    mark = relationship('MarkStudent', backref='student', lazy=True)

    def __str__(self):
        return self.name


# Quản lý môn học
class Subject(BaseModel):
    __tablename__ = 'subject'
    name = Column(String(250), nullable=False)
    sub_stu = relationship('StudentSbject', backref='subject', lazy=True)
    mark_column = relationship('MarkColumn', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class StudentSbject(BaseModel):
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
    value = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id))
    markcol_id = Column(Integer, ForeignKey(MarkColumn.id))


# Viết hàm định nghĩa các chức năng
def get_grade():
    return Grade.query.all()


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
