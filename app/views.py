# File: platform.py
import os, datetime

from flask import redirect, render_template, request, url_for, flash, json
from flask_classful import FlaskView, route
from werkzeug import secure_filename
from models import Dayrate, Rate, Category, Tag
from forms import DayrateForm, RateForm, TagForm, CategoryForm

from __init__ import app,db

# APPLICATION INDEX ROUTE
@app.route('/')
def home():
    return render_template('index.html',
        title='Ping Test'
    )


# INDUSTRIAL RATES INDEX 
class RateView(FlaskView):
        def index(self):
                return render_template('rate_index.html',
                        title='Industrial Rates Category',
                        form = CategoryForm(),
                        dr_form=DayrateForm(),
                        r_form=RateForm(),
                        t_form=TagForm(),
                        dayrates=DayRate.query.all(),
                        rates=Rate.query.all(),
                        ratecategory=Ratecategory.query.all(),
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





# REGISTER VIEWS
RateView.register(app)