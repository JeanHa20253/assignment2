from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


##WTForm

class ProductInfo(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    intro = StringField("Brief intro", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    url = StringField("Project URL", validators=[DataRequired(), URL()])
    describe = CKEditorField("Project content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")