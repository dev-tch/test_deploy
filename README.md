## creation  project and application  

- django-admin startproject tcnproject

- python manage.py startapp tcn

## commit description (TCH 25/06/2024) 
name commit: add module authentication for users of the application

setting.py
- config database credentials
- add tcn app  INSTALLED_APPS
- config LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, AUTH_USER_MODEL and STATIC_URL

tcn/templates/tcn:
- /registration/login.html : template for login
- /registration/signup : template for signup
- base.html  : generic template extendet by other templates
- home.html :home page for each authenticated users

tcn/static/tcn
- add static files like images

tcn/forms.html
- add  the class the controller from validation and creation

- tcn/urls.py : add urls paths used by application

tcn/views

- process request and map it to some template
tcnproject/tcn/urls.py
- include the urls used by the app

run migration to save the model into the configured database

-  tcn/migrations/0001_initial.py


