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
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(String(20), default='user')

    def __str__(self):
        return self.name


# Bảng thông tin khối lớp học
class Grade(BaseModel):
    __tablename__ = 'grade'
    grd_name = Column(String(20), nullable=False)  # Tên lớp
    grd_num = Column(Integer, nullable=False)  # Chỉ số lớp
    grd_descript = Column(String(100))  # Mô tả thông tin lớp
    grd_student = relationship('Student', backref='grade', lazy=True)  # Học sinh thuộc lớp

    grd_class = relationship('Class', backref='grade', lazy=True)

    def __str__(self):
        return self.name_grade


# Bảng thông tin lớp học
class Class(BaseModel):
    __tablename__ = 'class'
    cls_name = Column(String(250), nullable=False)

    cls_grd_id = Column(Integer, ForeignKey('grade.id'))
    cls_grade = relationship('Grade', backref='class', lazy=True)
    cls_student = relationship('Student', backref='class', lazy=True)
    def __str__(self):
        return self.cls_name


# Bảng học sinh
class Student(BaseModel):
    __tablename__ = 'student'
    stu_name = Column(String(100), nullable=False)  # Tên HS
    stu_gender = Column(String(5))  # Giới tính HS
    stu_birthday = Column(DateTime, nullable=False)  # Ngày sinh nhật của HS
    stu_address = Column(String(200))  # Địa chỉ nhà
    stu_contact_1 = Column(Integer, nullable=False)  # Số đt PH
    stu_contact_2 = Column(Integer)  # Số đt PH
    stu_email = Column(String(200))
    stu_image = Column(String(100))  # Hình ảnh của học sinh
    stu_created_date = Column(DateTime, default=datetime.now())  # Ngày tạo thông tin học sinh
    stu_grd_id = Column(Integer, ForeignKey(Grade.id), nullable=False)  # Lớp chưa thông tin hoc sinh này

    stu_cls_id = Column(Integer, ForeignKey('class.id'))
    stu_class = relationship('Class', backref='Student', lazy=True)

    def __str__(self):
        return self.stu_name


# Quản lý môn học
class Subject(BaseModel):
    __tablename__ = 'subject'
    sub_name = Column(String(250), nullable=False)
    sub_scores = relationship('Score', backref='Subject', lazy=True)
    sub_student = relationship('Student', secondary='sub_scores')

    def __str__(self):
        return self.sub_name


class MarkColumn(BaseModel):
    __tablename__ = 'mark_column'
    makcol_name = Column(String(150), nullable=False)
    makcol_score = relationship('Score', backref='mark_column', lazy=True)


class Mark(BaseModel):
    __tablename__ = 'mark'
    mk_value = Column(Integer, nullable=False)
    mk_stu_id = Column(Integer, ForeignKey('student.id'))
    mk_student = relationship('Student', backref='mark', lazy=True)
    mk_sub_id = Column(Integer, ForeignKey('subject.id'))
    mk_subject = relationship('Subject', backref='mark', lazy=True)
    mk_makcol_id = Column(Integer, ForeignKey('subject.id'))
    mk_markcol_name = relationship('MarkColumn', backref='mark', lazy=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
