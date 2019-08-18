# File: tables.py
# Implementing Flask Table
from flask_table import Table, Col, BoolCol, DatetimeCol

from models import User, Dayrate, Hourlyrate, Rate, Category, Tag, Offence

# TABLES DECLARATION
class DayrateTable(Table):
    category = Col('Job Category')
    
class UserTable(Table):
    uid = Col('User Id')
    username = Col('Username')
    firstname = Col('Firstname')
    lastname = Col('Lastname')
    email = Col('Email')
    active = BoolCol('State Active')
    admin = BoolCol('Role Admin')
    created_timestamp = DatetimeCol('Member Since')


user_table = UserTable(User.query.all())
dayrate_table = DayrateTable(Dayrate.query.all())