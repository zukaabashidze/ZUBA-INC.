from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('ელ-ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('გაიმეორეთ პაროლი', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('რეგისტრაცია')

class LoginForm(FlaskForm):
    email = StringField('ელ-ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')

class PostForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired()])
    content = TextAreaField('შეტყობინება', validators=[DataRequired()])
    submit = SubmitField('გამოქვეყნება')


class TransactionForm(FlaskForm):
    amount = DecimalField('თანხა (₾)', places=2, validators=[DataRequired(), NumberRange(min=-99999999, max=99999999)])
    description = StringField('აღწერილობა', validators=[Length(max=200)])
    submit = SubmitField('დამატება')

class ContactForm(FlaskForm):
    name = StringField('სახელი', validators=[DataRequired(), Length(max=120)])
    email = StringField('ელ-ფოსტა', validators=[DataRequired(), Email()])
    message = TextAreaField('შეტყობინება', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('გაგზავნა')

