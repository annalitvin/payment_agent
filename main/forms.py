from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, FloatField
from wtforms import validators

from app.settings import SECRET_KEY_CSRF
from main.validators import amount_length_check
from wtforms.csrf.session import SessionCSRF


class BaseForm(FlaskForm):
    class Meta:
        class Meta:
            csrf = True
            csrf_class = SessionCSRF
            csrf_secret = SECRET_KEY_CSRF


class RegistrationForm(BaseForm):
    amount = FloatField('Amount',
                        default=0.00,
                        render_kw={'type': 'number', 'step': 0.01},
                        validators=[
                            validators.required(),
                            validators.none_of((0.00, 00.00, 00),
                                               message='sum must be '
                                                       'greater than 0.0'),
                            amount_length_check], )

    currency = SelectField('Currency',
                           choices=[('USD', 'USD'),
                                    ('EUR', 'EUR'),
                                    ('RUB', 'RUB')],
                           validators=[validators.required(), ], )
    description = TextAreaField('Description',
                                validators=[validators.required(),
                                            validators.length(max=100)], )
