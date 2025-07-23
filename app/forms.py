from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class RegisterForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=15)])
    soy_de_consolidacion = BooleanField('Soy de consolidación')
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

class DiscipuloForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=15)])
    genero = SelectField('Género', validators=[DataRequired()])
    lider = SelectField('Líder', coerce=lambda x: int(x) if x and x != 'None' else None, validators=[Optional()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    submit = SubmitField('Registrar Discipulo')

class PeticionesForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=15)])
    peticion = StringField('Petición', validators=[DataRequired(), Length(min=2, max=500)])
    invasion = BooleanField('Invasión')
    submit = SubmitField('Registrar Petición')