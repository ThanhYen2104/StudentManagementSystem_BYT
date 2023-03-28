from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Stuman import db, app
from datetime import datetime


# Chỗ này thực hiện tạo db và phương thức truyền CSDL
class BaseModel(db.Model):
    # __abstract__ dùng cho các bảng kế thừa ==> Không tạo bảng mới khi thực thi
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


# Tạo bảng mới theo db.Model
# Bảng thông tin lớp học
class Grade(BaseModel):
    name_grade = Column(String(20), nullable=False) # Tên lớp
    num_grade = Column(Integer, nullable=False) # Chỉ số lớp
    descript_grade = Column(String(100))    # Mô tả thông tin lớp
    students = relationship('Student', backref='Grade', lazy=True)  # Học sinh thuộc lớp

    def __str__(self):
        return self.name_grade


# Bảng học sinh
class Student(BaseModel):
    # __tablename__ = 'Student'
    stu_name = Column(String(100), nullable=False)  # Tên HS
    stu_gender = Column(String(5))  # Giới tính HS
    stu_age = Column(Integer, nullable=False)  # Tuổi của HS
    stu_birthday = Column(DateTime, nullable=False)  # Ngày sinh nhật của HS
    stu_address = Column(String(200))  # Địa chỉ nhà
    stu_contact_1 = Column(Integer, nullable=False)  # Số đt PH
    stu_contact_2 = Column(Integer)  # Số đt PH
    stu_image = Column(String(100))  # Hình ảnh của học sinh
    created_date = Column(DateTime, default=datetime.now())  # Ngày tạo thông tin học sinh
    grase_id = Column(Integer, ForeignKey(Grade.id), nullable=False)  # Lớp chưa thông tin hoc sinh này

    def __str__(self):
        return self.stu_name


# Quản lý môn học
class Subject(BaseModel):
    sub_name = Column(String(50), nullable=False)
    sub_description = Column(Text)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
