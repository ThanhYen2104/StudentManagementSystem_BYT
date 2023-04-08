# from flask_login import current_user, login_user
from sqlalchemy import inspect
from StudentManagementSystem_BYT.Stuman import app, db
from flask_admin import Admin
from StudentManagementSystem_BYT.Stuman.models import Grade, Class, Student, StudentSubject, Semester
from StudentManagementSystem_BYT.Stuman.models import Subject, MarkColumn, MarkStudent, User
from flask_admin.contrib.sqla import ModelView


# class AdminView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__('Admin')
#
#
# class AuthenticatedView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated


class UserView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(User).mapper.column_attrs]


class GradeView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Grade).mapper.column_attrs]


class ClassView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Class).mapper.column_attrs]


class StudentView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Student).mapper.column_attrs]
    # column_select_related_list = (Student.grade_id, Student.classes_id)


class SubjectView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Subject).mapper.column_attrs]


class StudentSubjectView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(StudentSubject).mapper.column_attrs]


class MarkColumnView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(MarkColumn).mapper.column_attrs]


class MarkStudentView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(MarkStudent).mapper.column_attrs]


admin = Admin(app, name="QUẢN TRỊ BYT", template_mode='bootstrap4')
admin.add_view(ModelView(Semester, db.session, name="Học kì"))
admin.add_view(GradeView(Grade, db.session, name="Khối"))
admin.add_view(ClassView(Class, db.session, name="Lớp"))
admin.add_view(StudentView(Student, db.session, name="Học sinh"))
admin.add_view(SubjectView(Subject, db.session, name="Môn học"))
admin.add_view(StudentSubjectView(StudentSubject, db.session, name="Thêm môn cho HS"))
admin.add_views(MarkColumnView(MarkColumn, db.session, name="Cột điểm"))
admin.add_view(MarkStudentView(MarkStudent, db.session, name="Nhập điểm"))
admin.add_view(UserView(User, db.session, name="Tài khoản"))
