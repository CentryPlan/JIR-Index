# File: main.py

from __init__ import  app, db

import admin
import models


from auth import AuthView
import views

# from platform.views import HomeView, SysView

# Components Registration
AuthView.register(app)



if __name__ == '__main__':
    app.run(app.config['HOST'], app.config['PORT'])
