from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from app import db 
from .models import User
from .forms import RegisterForm, LoginForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user= User(
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            username=form.username.data,
            telefono=form.telefono.data,
            soy_de_consolidacion=1 if form.soy_de_consolidacion.data else 0,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('security/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))  
        else:
            flash('Número de teléfono o contraseña incorrectos', 'danger')

    return render_template('security/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/listado')
def listado():
    return render_template('listado.html')

@bp.route('/ingresar_peticion')
def ingresar_peticion():
    return render_template('peticion.html')