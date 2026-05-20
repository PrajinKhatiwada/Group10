from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField
from wtforms import IntegerField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional,ValidationError
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username  = StringField('Username',    validators=[InputRequired(), Length(min=3, max=50)])
    password  = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    email     = StringField('Email',      validators=[InputRequired(), Email()])
    firstname = StringField('First Name', validators=[InputRequired()])
    surname   = StringField('Surname',    validators=[InputRequired()])
    phone     = StringField('Phone',      validators=[InputRequired()])
    role      = SelectField('Account Type',
                            choices=[('buyer', 'Buyer / Tenant'),
                                     ('seller', 'Seller / Agent')])
    submit = SubmitField('Create Account')


class PropertyForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[InputRequired()]
    )

    address = StringField(
        'Address',
        validators=[InputRequired()]
    )

    suburb = StringField(
        'Suburb',
        validators=[InputRequired()]
    )

    description = TextAreaField(
        'Description',
        validators=[InputRequired()]
    )

    price = FloatField(
        'Asking Price ($)',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    original_price = FloatField(
        'Original Price ($)',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    category = SelectField(
        'Category',
        choices=[
            ('House', 'House'),
            ('Apartment', 'Apartment')
        ],
        validators=[InputRequired()]
    )

    status = SelectField(
        'Status',
        choices=[
            ('Active', 'Active'),
            ('Under Offer', 'Under Offer'),
            ('Sold', 'Sold'),
            ('Withdrawn', 'Withdrawn')
        ],
        validators=[InputRequired()]
    )

    bedrooms = IntegerField(
        'Bedrooms',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    bathrooms = IntegerField(
        'Bathrooms',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    car_spaces = IntegerField(
        'Car Spaces',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    size_sqft = IntegerField(
        'Size (sq ft)',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    images = MultipleFileField(
        'Upload Property Images',
        validators=[
            InputRequired(),
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'webp'],
                'Only JPG, JPEG, PNG, and WEBP images are allowed.'
            )
        ]
    )

    features = StringField(
        'Key Features (comma-separated)',
        validators=[Optional()]
    )

    document_name = StringField(
        'Document Name',
        validators=[Optional()]
    )

    document_file = FileField(
        'Upload Document',
        validators=[
            Optional(),
            FileAllowed(
                ['pdf', 'doc', 'docx'],
                'Only PDF, DOC, and DOCX files are allowed.'
            )
        ]
    )

    submit = SubmitField('Save Listing')

    def validate_images(self, field):
        uploaded_images = [file for file in field.data if file and file.filename]

        if len(uploaded_images) == 0:
            raise ValidationError('Please upload at least one property image.')

        if len(uploaded_images) > 5:
            raise ValidationError('You can upload maximum 5 property images only.')
class EnquiryForm(FlaskForm):
    message = TextAreaField('Your Message', validators=[InputRequired(),
                             Length(min=10, max=1000)])
    submit  = SubmitField('Submit Enquiry')


class OfferForm(FlaskForm):
    amount  = FloatField('Your Offer Amount ($)', validators=[InputRequired(),
                          NumberRange(min=1)])
    message = TextAreaField('Message (optional)', validators=[Optional(),
                             Length(max=500)])
    submit  = SubmitField('Submit Offer')


class BookmarkNotesForm(FlaskForm):
    notes  = TextAreaField('Your Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Notes')


class AdminCreateUserForm(FlaskForm):
    username  = StringField('Username',    validators=[InputRequired(), Length(min=3)])
    password  = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    email     = StringField('Email',      validators=[InputRequired(), Email()])
    firstname = StringField('First Name', validators=[InputRequired()])
    surname   = StringField('Surname',    validators=[InputRequired()])
    phone     = StringField('Phone',      validators=[InputRequired()])
    role      = SelectField('Role',
                            choices=[('buyer',  'Buyer'),
                                     ('seller', 'Seller'),
                                     ('admin',  'Admin')])
    submit = SubmitField('Create User')
