# File: data_form.py
# Uri: platform/data_form.py

from __init__ import app, g, csrf

from models import User, Dayrate, Rate, Category, Tag

import datetime, wtforms
from datetime import datetime
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired, Regexp,  Email


'''
class CSRFMixin(object):
	@staticmethod
	@app.before_request
	def add_csrf():
		self._csrf_token = HiddenField(default=csrf.protect())
'''


class ImageForm(wtforms.Form):
    file = wtforms.FileField('file')
    

class LoginForm(wtforms.Form):

	username = wtforms.StringField("Username", 
		validators=[DataRequired()])
	password = wtforms.PasswordField("Password", 
		validators=[DataRequired()])
	remember_me = wtforms.BooleanField("Remember me?", default=True)

	# Methods
	def validate(self):
		if not super(LoginForm, self).validate():
			return False
		
		self.user = User.authenticate(self.username.data, self.password.data)
		if not self.user:
			self.username.errors.append("Invalid username or password.")
			return False
			
		return True


class RegistrationForm(wtforms.Form):
    username = wtforms.TextField( 'Username',
		validators=[InputRequired(),Length(min=3, max=32),
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
        'Usernames must have only letters, '
        'numbers, dots or underscores')] )
    password = wtforms.PasswordField( 'Password', validators=[InputRequired(),
		EqualTo( 'confirm',message='Passwords must match')])
    confirm = wtforms.PasswordField('Confirm Password', [InputRequired()])
    firstname = wtforms.TextField( 'Firstname',validators=[InputRequired(),
		Length(min=3, max=32), Regexp('^[A-Za-z][A-Za-z]*$',0,
        'Firstnames must have only letters '
        )] )
    lastname = wtforms.TextField('Lastname',validators=[InputRequired(),
		Length(3, 32), Regexp('^[A-Za-z][A-Za-z]*$',0,
        'Lastnames must have only letters '
       )])
    email =wtforms.TextField('Email Address',validators=[InputRequired(),
		Length(min=6, max=64), Email()])

    # dates 
    created_timestamp = wtforms.DateField('Date', default=datetime.now)

    submit = wtforms.SubmitField('Create User')    
    
    def save_user(self, user):

        self.populate_obj(user)
        user.get_id()
        return user



# Category Form
class CategoryForm(wtforms.Form):
    name = wtforms.StringField('Category Name') 



# Category Form
class TagForm(wtforms.Form):
    name = wtforms.StringField('Tag') 

#

class DayrateForm(wtforms.Form):

    # Identification
    category = wtforms.StringField('Job Category')
    l1_rate =  wtforms.FloatField('Level1 Rate')
    l2_rate =  wtforms.FloatField('Level2 Rate')
    l3_rate =  wtforms.FloatField('Level3 Rate')



class RateForm(wtforms.Form):
    categories = Category.query.all()



    # Identification
    title = wtforms.StringField('Title')
    category = wtforms.SelectField('Category',
        choices=[(category.id, category.name) for category in categories]
    )
    description = wtforms.StringField('Description')
    unit = wtforms.SelectField(
        'Unit',
        choices=[
            ('bg.', 'Bag'),
            ('bx.', 'Box.'),
            ('bdl', 'Bundle'),
            ('ea', 'Each'),
            ('no', 'Number'),
            ('doz', 'Dozen'),
            ('ld', 'Load'),
            ('lnt', 'Length'),
            ('bdl', 'Bundle.'),
            ('sht.', 'Sheet'),
            ('rll', 'Roll'),
            ('tnn', 'Ton'),
            ('ft', 'Run Ft'),
            ('ft2', 'Square Ft'),
            ('ft3', 'Cubic Feet'),
             ('yd', 'Yd'),
            ('yd2', 'Square Yd'),
            ('yd3', 'Cubic Yd')
            
            ]  
    )
    
    munit = wtforms.SelectField(
        'Metric Unit',
        choices=[
            ('bg.', 'Bag'),
            ('bx.', 'Box.'),
            ('bdl', 'Bundle'),
            ('ea', 'Each'),
            ('no', 'Number'),
            ('ld', 'Load'),
            ('lnt', 'Length'),
            ('bdl', 'Bundle.'),
            ('sht.', 'Sheet'),
            ('rll', 'Roll'),

            ('tnn', 'Ton'),
            ('m', 'Meter'),
            ('m2', 'Square Meter'),
            ('m3', 'Cubic Meter'),
             ('kg', 'Kilogram')           
            
            ]  
    )
    ado =  wtforms.FloatField('Average Daily Output')
    production =  wtforms.FloatField('production')
    mproduction =  wtforms.FloatField('Metric Production Rate')
    total_rate =  wtforms.FloatField('Total Rate')
    mtotal_rate =  wtforms.FloatField('Metric Rate')
    mproduction =  wtforms.FloatField('Metric Production Rate')
    tags =  wtforms.FloatField('Tags')


