from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    name_grade = Column(String(20), nullable=False)
    num_grade = Column(Integer, nullable=False)
    descript_grade = Column(String(100))
    students = relationship('Student', backref='Grade', lazy=True)

    def __str__(self):
        return self.name_grade


# Bảng học sinh
class Student(BaseModel):
    # __tablename__ = 'Student'
    stu_name = Column(String(100), nullable=False)
    stu_gender = Column(String(5))
    stu_age = Column(Integer, nullable=False)
    stu_birthday = Column(DateTime, nullable=False)
    stu_address = Column(String(200))
    stu_contact = Column(Integer)
    stu_image = Column(String(100))
    created_date = Column(DateTime, default=datetime.now())
    grase_id = Column(Integer, ForeignKey(Grade.id), nullable=False)

    def __str__(self):
        return self.stu_name


# Bảng điểm học sinh
class Mark(BaseModel):
    mark_name = Column(String(30), nullable=False)
    mark_num = Column(Integer, nullable=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
