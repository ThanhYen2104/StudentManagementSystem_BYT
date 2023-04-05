from flask_admin import Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user
from StudentManagementSystem_BYT.Stuman import app, db, models
from StudentManagementSystem_BYT.Stuman.models import Class, Student


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__('Admin')


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name="QUẢN TRỊ BYT EDUCATION", template_mode='bootstrap4')
admin.add_views(AdminView(Student, db.session), name="Học sinh")
