from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional


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
    title         = StringField('Title',       validators=[InputRequired()])
    address       = StringField('Address',     validators=[InputRequired()])
    suburb        = StringField('Suburb',      validators=[InputRequired()])
    description   = TextAreaField('Description', validators=[InputRequired()])
    price         = FloatField('Asking Price ($)', validators=[InputRequired(),
                                NumberRange(min=0)])
    original_price = FloatField('Original Price ($)', validators=[InputRequired(),
                                 NumberRange(min=0)])
    category      = SelectField('Category',
                                choices=[('House', 'House'),
                                         ('Apartment', 'Apartment')])
    status        = SelectField('Status',
                                choices=[('Active', 'Active'),
                                         ('Under Offer', 'Under Offer'),
                                         ('Sold', 'Sold'),
                                         ('Withdrawn', 'Withdrawn')])
    bedrooms      = IntegerField('Bedrooms',   validators=[InputRequired(),
                                  NumberRange(min=0)])
    bathrooms     = IntegerField('Bathrooms',  validators=[InputRequired(),
                                  NumberRange(min=0)])
    car_spaces    = IntegerField('Car Spaces', validators=[InputRequired(),
                                  NumberRange(min=0)])
    size_sqft     = IntegerField('Size (sq ft)', validators=[InputRequired(),
                                  NumberRange(min=0)])
    image         = StringField('Image Filename (e.g. property-for-sale-first.jpg)',
                                validators=[InputRequired()])
    features      = StringField('Key Features (comma-separated)',
                                validators=[Optional()])
    submit = SubmitField('Save Listing')


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
