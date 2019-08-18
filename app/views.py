# File: platform.py
import os, datetime

from flask import redirect, render_template, request, url_for, flash, json
from flask_classful import FlaskView, route
from werkzeug import secure_filename

from models import Dayrate, Hourlyrate, Rate, Category, Tag, Offence
from forms import DayrateForm, RateForm, TagForm, CategoryForm
from tables import dayrate_table, user_table

from __init__ import app,db

# APPLICATION INDEX ROUTE
@app.route('/')
def home():
    return render_template('index.html',
        title='Ping Test'
    )


# GUIDELINES AND RULES
class GuideView(FlaskView):
        def guidelines(self):
                return render_template('guideline.html',
                title='Industrial Council Guidelines')

        @route('/offences')
        def offence(self):
                return render_template('offences.html',
                title = 'Diciplinary Guidelines',
                offences_ = Offence.query.all()
                )



# INDUSTRIAL RATES INDEX 
class RateView(FlaskView):
        def index(self):
                return render_template('index.html',
                        title='Industrial Rates Index',
                        form = CategoryForm(),
                        dr_form=DayrateForm(),
                        r_form=RateForm(),
                        t_form=TagForm(),
                        dayrates=Dayrate.query.all(),
                        rates=Rate.query.all(),
                        ratecategory=Category.query.all(),
                        tags=Tag.query.all())

                    
        @route('/createcategory', methods=['get', 'post'])    
        def createcategory(self):
                message=""
                if request.method == 'POST':
                        name = request.form.get('name')
                        message = f'New Category {name} created!'

                        categ =Ratecategory(name=name)
                        db.session.add(categ)
                        db.session.commit()
                
                flash(message)
                return redirect(url_for('RateView:index'))
                 
        @route('/createdayrate', methods=['get', 'post'])    
        def createdayrate(self):
                message=""
                if request.method == 'POST':
                        dayrate = DayRate(
                        category = request.form.get('category'),
                        l1_rate = request.form.get('l1_rate'),
                        l2_rate = request.form.get('l2_rate'),
                        l3_rate = request.form.get('l3_rate'),

                        )
                        db.session.add(dayrate)
                        db.session.commit()
                
                flash(f"Day rate {dayrate.category} created")
                return redirect(url_for('RateView:index'))
        
        @route('/createrate', methods=['get', 'post'])    
        def createrate(self):
               
                if request.method == 'POST':
                        rate = Rate(
                        title = request.form.get('title'),
                       
                        descriptiion = request.form.get('description'),
                        ado = request.form.get('ado'),
                        unit = request.form.get('unit'),
                        munit = request.form.get('munit'),

                        production = request.form.get('production'),
                        total_rate = request.form.get('total_rate'),

                        m_production = request.form.get('mproduction'),
                        m_total_rate = request.form.get('mtotal_rate')
                       
                        )
                        category = Ratecategory(name=request.form.get('category')).first()
                        tags = Tag(name=request.form.get('tags')).first()
                        rate.category.append(category)
                        rate.tags.append(tags)

                        db.session.add(rate)
                        db.session.commit()
                
                flash(f"Job rate {rate.title} created")
                return redirect(url_for('RateView:index'))


        @route('dayrate')
        def dayrate(self):
                return render_template('dayrate_index.html',
                        title='Industrial Rates Index',
                        hr_form = Hourlyrate.query.all(),
                        dr_form=DayrateForm(),
                        dayrates=Dayrate.query.all(),
                        table=dayrate_table,
                        usertable = user_table
                        )





# REGISTER VIEWS
GuideView.register(app)
RateView.register(app)