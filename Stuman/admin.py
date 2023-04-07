# from flask_login import current_user, login_user
from sqlalchemy import inspect
from StudentManagementSystem_BYT.Stuman import app, db
from flask_admin import Admin
from StudentManagementSystem_BYT.Stuman.models import Grade, Class, Student, StudentSubject, Semester
from StudentManagementSystem_BYT.Stuman.models import Subject, MarkColumn, MarkStudent
from flask_admin.contrib.sqla import ModelView


# class AdminView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__('Admin')
#
#
# class AuthenticatedView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated

class SemesterView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class GradeView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class ClassView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class StudentView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    # column_select_related_list = (Student.grade_id, Student.classes_id)


class SubjectView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class StudentSubjectView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class MarkColumnView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class MarkStudentView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


admin = Admin(app, name="QUẢN TRỊ BYT", template_mode='bootstrap4')
admin.add_view(GradeView(Semester, db.session, name="Học kì"))
admin.add_view(GradeView(Grade, db.session, name="Khối"))
admin.add_view(ClassView(Class, db.session, name="Lớp"))
admin.add_view(StudentView(Student, db.session, name="Học sinh"))
admin.add_view(SubjectView(Subject, db.session, name="Môn học"))
admin.add_view(StudentSubjectView(StudentSubject, db.session, name="HS đăng ký môn"))
admin.add_views(MarkColumnView(MarkColumn, db.session, name="Cột điểm"))
admin.add_view(MarkStudentView(MarkStudent, db.session, name="Nhập điểm"))
