# from flask_login import current_user, login_user
from StudentManagementSystem_BYT.Stuman import app, db
from flask_admin import Admin
from StudentManagementSystem_BYT.Stuman.models import Grade, Class, Student
from flask_admin.contrib.sqla import ModelView

# class AdminView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__('Admin')
#
#
# class AuthenticatedView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated


admin = Admin(app, name="QUẢN TRỊ BYT EDUCATION", template_mode='bootstrap4')
admin.add_view(ModelView(Grade, db.session, name="Khối"))
admin.add_view(ModelView(Class, db.session, name="Lớp", category="Grade"))
admin.add_view(ModelView(Student, db.session, name="Học sinh", category="Class"))
