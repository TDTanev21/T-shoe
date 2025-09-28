from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, current_user
from . import auth_bp
from .forms import LoginForm, RegistrationForm