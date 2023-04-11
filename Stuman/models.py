from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from StudentManagementSystem_BYT.Stuman import db, app
from datetime import datetime
from flask_login import UserMixin
import enum
import hashlib


# Chỗ này thực hiện tạo db và phương thức truyền CSDL
class BaseModel(db.Model):
    # __abstract__ dùng cho các bảng kế thừa ==> Không tạo bảng mới khi thực thi
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(enum.Enum):
    ADMIN = 1
    TEACHER = 2
    USER = 3


class MarkName(enum.Enum):
    HOUR_TEST = 7
    MINUTES_15_TEST = 8
    FINAL_EXAM_MARK = 9


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


# Bảng thông tin khối lớp học
class Grade(BaseModel):
    __tablename__ = 'grade'
    name = Column(String(20), nullable=False)  # Tên khối lớp
    value = Column(Integer, nullable=False)  # Chỉ số lớp
    description = Column(String(100))  # Mô tả thông tin khối lớp
    students = relationship('Student', backref='grade', lazy=False)  # Học sinh thuộc khối lớp
    classes = relationship('Class', backref='grade', lazy=False)

    def __str__(self):
        return self.name


# Bảng thông tin lớp học
class Class(BaseModel):
    __tablename__ = 'class'
    name = Column(String(250), nullable=False)
    student = relationship('Student', backref='class', lazy=True)
    grade_id = Column(Integer, ForeignKey(Grade.id))

    def __str__(self):
        return self.name


# Bảng học sinh
class Student(BaseModel):
    __tablename__ = 'student'
    name = Column(String(100), nullable=False)  # Tên HS
    gender = Column(String(10), default="Không có")  # Giới tính HS
    birthday = Column(String(12))  # Ngày sinh nhật của HS
    address = Column(String(200))  # Địa chỉ nhà
    contact_1 = Column(Integer, nullable=False)  # Số đt PH
    contact_2 = Column(Integer)  # Số đt PH
    email = Column(String(200))
    image = Column(String(100))  # Hình ảnh của học sinh
    created_date = Column(DateTime, default=datetime.now())  # Ngày tạo thông tin học sinh
    grade_id = Column(Integer, ForeignKey(Grade.id))
    classes_id = Column(Integer, ForeignKey(Class.id))
    user_id = Column(Integer, ForeignKey(User.id))
    student_sub = relationship('StudentSubject', backref='student', lazy=True)
    mark = relationship('MarkColumn', backref='student', lazy=True)

    def __str__(self):
        return self.name


# Quản lý môn học
class Subject(BaseModel):
    __tablename__ = 'subject'
    name = Column(String(250), nullable=False)
    subject_student = relationship('StudentSubject', backref='subject', lazy=True)
    mark = relationship('MarkColumn', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class StudentSubject(BaseModel):
    __tablename__ = 'student_subject'
    student_id = Column(Integer, ForeignKey(Student.id))
    subject_id = Column(Integer, ForeignKey(Subject.id))
    quantity = Column(Integer, default=1)


class MarkColumn(BaseModel):
    __tablename__ = 'mark_column'
    name = Column(Enum(MarkName), default=MarkName.MINUTES_15_TEST)
    value = Column(Float, nullable=False, default=0.0)
    student_id = Column(Integer, ForeignKey(Student.id))
    subject_id = Column(Integer, ForeignKey(Subject.id))

    def __str__(self):
        return self.name


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


def get_markcolumn_by_id(mark_column_id):
    return MarkColumn.query.get(mark_column_id)


def get_markcolumn(student_id=None, subject_id=None):
    markcolumn = MarkColumn.query
    if student_id and subject_id:
        markcolumn.filter(MarkColumn.student_id.__eq__(student_id))
        markcolumn.filter(MarkColumn.subject_id.__eq__(subject_id))
    return markcolumn.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'),
                user_role=kwargs.get('user_role'))
    db.session.add(user)
    db.session.commit()


def add_student(name, **kwargs):
    student = Student(name=name,
                      gender=kwargs.get('gender'),
                      birthday=kwargs.get('birthday'),
                      address=kwargs.get('address'),
                      contact_1=kwargs.get('contact_1'),
                      contact_2=kwargs.get('contact_2'),
                      email=kwargs.get('email'),
                      image=kwargs.get('image'))
    db.session.add(student)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        # db.session.commit()
        # db.drop_all()
        db.create_all()
