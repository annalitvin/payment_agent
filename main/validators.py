
from wtforms.validators import ValidationError

from api.constants import CurrencyNames


def amount_length_check(form, field):
    currency = form.currency.data
    amount_data = field.data

    if currency == CurrencyNames.RUB.value:
        if amount_data < 10.0 or amount_data > 1000000.0:
            raise ValidationError('Payer price amount is too small, min: 10.0')
    elif currency == CurrencyNames.USD.value:
        if amount_data < 1.0 or amount_data > 10000.0:
            raise ValidationError('Payer amount is too small, min: 1.0')

