from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, SelectField, BooleanField, TextAreaField, validators,DecimalField
from wtforms.fields.core import StringField

class Addproducts(Form):
    name = StringField('Name',[validators.DataRequired()])
    price = DecimalField('Price',[validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock',[validators.DataRequired()])
    discription = TextAreaField('Discription',[validators.DataRequired()])
    
    image_1 = FileField('Image 1',validators=[FileAllowed(['jpg','png','gif','jpeg'])]) 
    image_2 = FileField('Image 2',validators=[FileAllowed(['jpg','png','gif','jpeg'])])  
    image_3 = FileField('Image 3',validators=[FileAllowed(['jpg','png','gif','jpeg'])])     
    