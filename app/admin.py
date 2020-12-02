from flask import flash, redirect
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


class MyController(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin == True:
            return True
    def inaccessible_callback(self, admin, **kwargs):
        flash(f'Access denied: only admin users allowed', 'danger')
        return redirect('/')

class MyAdminController(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin == True:
            return True
    def inaccessible_callback(self, admin, **kwargs):
        flash(f'Access denied: only admin users allowed', 'danger')
        return redirect('/')
