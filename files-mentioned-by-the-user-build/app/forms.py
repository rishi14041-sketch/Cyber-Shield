from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")
class PasswordForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    password = PasswordField("New password", validators=[DataRequired(), Length(min=12), EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm password", validators=[DataRequired()]); submit = SubmitField("Update password")
class AlertForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)]); description = TextAreaField("Description", validators=[DataRequired()])
    severity = SelectField("Severity", choices=[("Low","Low"),("Medium","Medium"),("High","High"),("Critical","Critical")])
    status = SelectField("Status", choices=[("Open","Open"),("In Progress","In Progress"),("Closed","Closed")])
    category = StringField("Category", validators=[Optional(), Length(max=80)]); source = StringField("Source", validators=[Optional(), Length(max=100)])
    notes = TextAreaField("Notes", validators=[Optional()]); submit = SubmitField("Save alert")
class IncidentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)]); priority = SelectField("Priority", choices=[("Low","Low"),("Medium","Medium"),("High","High"),("Critical","Critical")])
    status = SelectField("Status", choices=[("Open","Open"),("Investigating","Investigating"),("Contained","Contained"),("Closed","Closed")])
    affected_assets = TextAreaField("Affected assets"); investigation_notes = TextAreaField("Investigation notes"); recovery_steps = TextAreaField("Recovery steps"); root_cause = TextAreaField("Root cause"); final_report = TextAreaField("Final report")
    submit = SubmitField("Save incident")
