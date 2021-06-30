import requests
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import URL, Email, InputRequired, NumberRange, ValidationError


# ---------- Quantity Form ---------------- #
class QuantityForm(FlaskForm):
    """This is a class to generate a form to give user an option to specify
    a quantity of entries in the database required (it is set up to 1000 by default).
    Consists of one Decimal Field to input integer in range 1-5000 (the biggest possible randomuser.me API response)
    and a submit button.
    Validators to check if there any entry and if that's an integer in range 1-5000 are established.
    class: 'FlaskForm'
    """

    quantity = DecimalField(
        "",
        validators=[
            InputRequired(),
            NumberRange(
                min=1, max=5000, message="Only integers in range 1-5000 are allowed"
            ),
        ],
    )
    submit = SubmitField(label="Change Number")


# ---------- Edit Form ---------------- #
def check_if_image(link):
    """Returns True if link passed in leads to an image file,
    False otherwise.

    :param link: any URL
    :type link: str

    :return:True if link passed in leads to an image file, False otherwise
    :rtype: bool
    """
    response = requests.get(link)
    headers = response.headers
    if headers.get("content-type").startswith("image"):
        return True
    else:
        return False


def image_validator(form, field):
    """Custom validator for FlaskForm to check if link passed in leads to an image file"""
    if not check_if_image(field.data):
        raise ValidationError("Link does not lead to an image")


class EditForm(FlaskForm):
    """This is a class to generate a form to provide options
    to create new entry to the dataset or edit an existing one.
    All the fields have 'InputRequired' validator and EmailField has also an Email validator.
    class: 'FlaskForm'
    """

    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    gender = StringField("Gender", validators=[InputRequired()])
    cell = StringField("Cell Number", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    location = StringField("Location", validators=[InputRequired()])
    pic_link = StringField(
        "Link to a photo_file", validators=[InputRequired(), URL(), image_validator]
    )
    submit = SubmitField(label="Save Data")
