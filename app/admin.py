# File: admin.py
# File Url: app/admin.py

from wtforms.fields import SelectField, PasswordField

from flask import g, url_for,redirect,request
import flask_admin
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from __init__ import app, db

from models import Hourlyrate, Tag, User, Category, Dayrate, Rate,  Offence


class AdminAuthentication(object):

	def is_accessible(self):

		return g.user.is_authenticated and g.user.is_admin()


class BaseModelView(AdminAuthentication, ModelView):

	pass


class FileAdmin(AdminAuthentication):
	
	pass



class CategoryModelView(ModelView):
	
	column_filters = ['name']
	
	column_list = ['name']
	column_searchable_list = ['name']
	
	form_columns = ['name']
	

class  DayrateModelView(ModelView):
	
	column_filters = ['category']
	
	column_list = ['category','hourly_rates']
	column_searchable_list = ['id','category']
	
	form_columns = ['category']
	

class UserModelView(ModelView):

	column_filters = ('email', 'username', 'active', 'admin')
	column_list = ['uid', 'email','username', 'firstname','lastname', 'active', 'admin', 'created_timestamp']
	column_searchable_list = ['email', 'username', 'firstname', 'lastname']
	form_columns = ['email', 'username', 'firstname', 'lastname', 'password', 'admin', 'active']
	form_extra_fields = {'password': PasswordField('New password'),}
	def on_model_change(self, form, model, is_created):
		if form.password.data:
			model.password_hash = User.make_password(form.password.data)
		return super(UserModelView, self).on_model_change(form, model, is_created)


#
'''
class RateModelView(ModelView):

	column_filters = ('email', 'username', 'active', 'admin')
	column_list = ['uid', 'email','username', 'firstname','lastname', 'active', 'admin', 'created_timestamp']
	column_searchable_list = ['email', 'username', 'firstname', 'lastname']
	form_columns = ['email', 'username', 'firstname', 'lastname', 'password', 'admin', 'active']
	form_extra_fields = {'password': PasswordField('New password'),}
	def on_model_change(self, form, model, is_created):
		if form.password.data:
			model.password_hash = User.make_password(form.password.data)
		return super(UserModelView, self).on_model_change(form, model, is_created)



class DayRateModelView(ModelView):

	column_filters = ('email', 'username', 'active', 'admin')
	column_list = ['uid', 'email','username', 'firstname','lastname', 'active', 'admin', 'created_timestamp']
	column_searchable_list = ['email', 'username', 'firstname', 'lastname']
	form_columns = ['email', 'username', 'firstname', 'lastname', 'password', 'admin', 'active']
	form_extra_fields = {'password': PasswordField('New password'),}
	def on_model_change(self, form, model, is_created):
		if form.password.data:
			model.password_hash = User.make_password(form.password.data)
		return super(UserModelView, self).on_model_change(form, model, is_created)

'''



admin = Admin(app, 'Rates Index')

class IndexView(AdminIndexView):

	@expose('/')
	def index(self):

		if not (g.user.is_authenticated ): #and g.user.is_admin()):

			return redirect(url_for('login', next=request.path))

		return self.render('admin/index.html')

admin.add_view( DayrateModelView(Dayrate, db.session))

admin.add_view( CategoryModelView(Category, db.session))

#admin.add_view( TagModelView(Tag, db.session))

admin.add_view(UserModelView(User, db.session))

#admin.add_view(BlogFileAdmin(app.config['STATIC_DIR'], '/static/', name='StaticFiles'))

