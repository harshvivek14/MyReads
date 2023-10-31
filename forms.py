from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms.validators import InputRequired, Length

# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=35)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=35)])
    username = StringField("Username", validators=[InputRequired(), Length(max=15)])
    password = PasswordField("Password", validators=[InputRequired()])

# Logic form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=15)])
    password = PasswordField("Password", validators=[InputRequired()])
