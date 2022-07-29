from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    value_1=StringField("Value 1", validators=[DataRequired()])
    value_2=StringField("Value 2", validators=[DataRequired()])
    operatornya=SelectField("Operator", choices=[("","Choose Operator"),("*","X"),("+","+"),("-","-"),
                                                 ("/","/")])
    submit=SubmitField("Save")
    