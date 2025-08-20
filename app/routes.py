from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app import db 
from .models import User, Discipulo, Peticiones, Nota
from .forms import RegisterForm, LoginForm, DiscipuloForm, PeticionesForm, NotaForm

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
            return redirect(url_for('main.listado'))  
        else:
            flash('Número de teléfono o contraseña incorrectos', 'danger')

    return render_template('security/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/listado', methods=['GET', 'POST'])
@login_required
def listado():
    consolidacion = current_user.soy_de_consolidacion
    lideres = User.query.all()
    discipulos = Discipulo.query.all()
    form = DiscipuloForm(request.form)
    form.lider.choices = [(None, "Ninguno")] + [(lider.id, f"{lider.nombres} {lider.apellidos}") for lider in lideres]
    form.genero.choices = [('Masculino', 'Masculino'), ('Femenino', 'Femenino')]
    if request.method == 'POST' and form.validate_on_submit():
        discipulo = Discipulo(
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            telefono=form.telefono.data,
            genero=form.genero.data,
            lider_id=form.lider.data,
            direccion=form.direccion.data
        )
        db.session.add(discipulo)
        db.session.commit()
        return redirect(url_for('main.listado'))
    return render_template('listado.html', lideres=lideres, form=form, discipulos=discipulos, consolidacion=consolidacion)

@bp.route('/discipulo/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_discipulo(id):
    discipulo = Discipulo.query.get_or_404(id)
    db.session.delete(discipulo)
    db.session.commit()
    return redirect(url_for('main.listado'))


@bp.route('/discipulo/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_discipulo(id):
    discipulo = Discipulo.query.get_or_404(id)
    form = DiscipuloForm(obj=discipulo)

    lideres = User.query.all()
    form.lider.choices = [(None, "Ninguno")] + [(lider.id, f"{lider.nombres} {lider.apellidos}") for lider in lideres]
    form.genero.choices = [('Masculino', 'Masculino'), ('Femenino', 'Femenino')]

    if request.method == 'POST' and form.validate_on_submit():
        discipulo.nombres = form.nombres.data
        discipulo.apellidos = form.apellidos.data
        discipulo.telefono = form.telefono.data
        discipulo.genero = form.genero.data
        discipulo.lider_id = form.lider.data
        discipulo.direccion = form.direccion.data

        db.session.commit()
        return redirect(url_for('main.listado'))

    return render_template('editar_discipulo.html', form=form, discipulo=discipulo)


@bp.route('/ingresar_peticion', methods=['GET', 'POST'])
def ingresar_peticion():
    form = PeticionesForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        peticion = Peticiones(
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            peticion=form.peticion.data,
            visita=1 if form.visita.data else 0,
            invasion=1 if form.invasion.data else 0
        )
        db.session.add(peticion)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('peticion.html', form=form)

@bp.route('/intersecion')
@login_required
def intersecion():
    peticiones = Peticiones.query.all()
    return render_template('intersecion.html', peticiones=peticiones)

@bp.route('/detalle_discipulo/<int:id>', methods=['GET', 'POST'])
@login_required
def detalle_discipulo(id):
    discipulo = Discipulo.query.get_or_404(id)
    form = NotaForm()

    if discipulo.lider_id != current_user.id:
        return redirect(url_for('main.listado'))
    
    if form.validate_on_submit():
        nota = Nota(
            contenido=form.contenido.data,
            discipulo_id=form.discipulo_id.data
        )
        db.session.add(nota)
        db.session.commit()
        return redirect(url_for('main.detalle_discipulo', id=id))
    form.discipulo_id.data = id

    notas = Nota.query.filter_by(discipulo_id=id).order_by(Nota.fecha.desc()).all()

    return render_template('detalle_discipulo.html', discipulo=discipulo, form=form, notas=notas)