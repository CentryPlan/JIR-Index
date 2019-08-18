# File: auth_models.py
import datetime
import re
import genny
import math
#import application
#from flask import current_app


from __init__ import db, g
#current_app(application)

# UTILITIES
def sluger(s):
    return re.sub('[^\w]+', '-', s).lower()

def to_dict(model_instance, query_instance=None):
    if hasattr(model_instance, '__table__'):
        return {c.name: str(getattr(model_instance, c.name)) for c in model_instance.__table__.columns}
    else: 
        cols = query_instance.column_descriptions
        return { cols[i]['name'] : model_instance[i] for i in range(len(cols))}


# ASSOCIATIONS / JOINED TABLES
rate_category = db.Table('rate_category',
                          db.Column('category_id', db.Integer,
                                    db.ForeignKey('category.id')),
                          db.Column('rate_id', db.Integer,
                                    db.ForeignKey('rate.id'))
                          )

#
rate_tag = db.Table('rate_tag',
                          db.Column('tag_id', db.Integer,
                                    db.ForeignKey('tag.id')),
                          db.Column('rate_id', db.Integer,
                                    db.ForeignKey('rate.id'))
                          )

#
hour_dayrate = db.Table('hour_dayrate',
                          db.Column('hourlyrate_id', db.Integer,
                                    db.ForeignKey('hourlyrate.id')),
                          db.Column('dayrate_id', db.Integer,
                                    db.ForeignKey('dayrate.id'))
                          )


# DATA MODELS



class User(db.Model):

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64),
                    unique=True)
    username = db.Column(db.String(64), unique=True)
    # Personal
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    # Contact
    email = db.Column(db.String(64), unique=True)
    # Security
    password_hash = db.Column(db.String(255))
    # State
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    # Document
    created_timestamp = db.Column(db.DateTime,
		default=datetime.datetime.now())
    
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()
        self.get_uid()

    # Methods
    def generate_slug(self):
        if self.username:
            self.slug = sluger('U {name}'.format(name=self.username))

    # Login interface..
    def get_id(self):
        return self.id

    def get_uid(self):
        self.uid = genny.nameid(self.firstname,self.lastname)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, username, firstname, lastname, email, password, **kwargs):
        return User(
            username=username,
            firstname=firstname.capitalize(),
            lastname=lastname.capitalize(),
            email=email,
            password_hash=User.make_password(password),
            **kwargs
        )

    @staticmethod
    def authenticate(username, password):

        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            return user
        return False


# RATE CATEGORIES 
class Category(db.Model):

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)    
    # Document
                                
    
    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.get_id()
        
    def get_id(self):
    	if self.name:
            return self.id            
    
    def dictify(self):
        if self.name:
            return to_dict(self)
    
    def __repr__(self):
        return f'<Industry Rate Category: {self.name}'


# DICIPLINARY GUIDELINES

class Offence(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    offence_type = db.Column(db.String(220))

    first_offence = db.Column(db.String(64))
    second_offence = db.Column(db.String(64))
    third_offence = db.Column(db.String(64))


    def __init__(self, *args, **kwargs):
        super(Offence, self).__init__(*args, **kwargs)
        self.get_id()        

    def get_id(self):
        if self.offence_type:
            return self.id

    def __repr__(self):
        return f'<Diciplinary Guideline: {self.offence_type}'

   

class Tag(db.Model):

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)    
       
    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.get_id()
        
    def get_id(self):
    	if self.name:
            return self.id            
    
    def dictify(self):
        if self.name:
            return to_dict(self)
    
    def __repr__(self):
        return f'<Rate Tag: {self.name}'



class Hourlyrate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    note = db.Column(db.String(120))
   

    l1_rate = db.Column(db.Float())
    l2_rate = db.Column(db.Float())
    l3_rate = db.Column(db.Float())

    def __init__(self, *args, **kwargs):
        super(Hourate, self).__init__(*args, **kwargs)
       

    def __repr__(self):
        return f'<Hour Rate For: {self.title} {self.note}'


class Dayrate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))

    hourly_rates = db.relationship("Hourlyrate", secondary=hour_dayrate,
                            backref=db.backref("dayrate", lazy='dynamic'))


    def __init__(self, *args, **kwargs):
        super(DayRate, self).__init__(*args, **kwargs)
        self.get_id()        

    def get_id(self):
        if self.category:
            return self.id

    def __repr__(self):
        return f'<Day Rate: {self.name}'



class Rate(db.Model):

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.String(10),
                    unique=True)
    title = db.Column(db.String(168), unique=True)
    category = db.relationship("Category", secondary=rate_category,
                            backref=db.backref("rate", lazy='dynamic'))
    # Project Legal
    descriptiion = db.Column(db.String(264))
    ado = db.Column(db.Integer()) # Average Daily Output

    unit = db.Column(db.String(8))
    munit = db.Column(db.String(8))

    production = db.Column(db.Float())
    total_rate = db.Column(db.Float())  # Land

    m_production = db.Column(db.Float())
    m_total_rate = db.Column(db.Float())
    
    tags = db.relationship("Tag", secondary=rate_tag,
                            backref=db.backref("rate", lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Rate, self).__init__(*args, **kwargs)

        self.generate_slug()
        self.get_rid()
       

    # Methods
    def generate_slug(self):
        if self.title:
            self.slug = sluger(f'Rate {self.title}')

    def get_id(self):
        if self.title:
            return self.id

    def get_rid(self):
        self.rid = genny.nameid(self.title, self.unit)
    
    def dictify(self):
        if self.id:
            return to_dict(self)

    def __repr__(self):
        return f'<Rate: {self.title}'
