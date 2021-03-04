from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views,forms

from app import create_app

app = create_app('development')
app.app_context().push()