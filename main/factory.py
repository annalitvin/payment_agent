
import random

from api.piastrixlib import PiastrixApi
from flask import render_template, redirect

from app.utils import log_info
from api import settings
from api.constants import CurrencyCodes


class PiastrixViewFactory:

    def __init__(self, form_data, currency, **kwargs):
        self.currency = currency
        self.secret_key = settings.SECRET_KEY_PAYMENT
        self.shop_id = settings.SHOP_ID
        self._id = kwargs.get('_id')
        self.form_data = form_data
        self.piastrix = PiastrixApi(self.shop_id, self.secret_key, _id=self._id)

    def get_method(self):

        if self.currency == CurrencyCodes.EUR.value:
            description = {'description': self.form_data.get('description')}

            response = self.piastrix.pay(amount=self.form_data.pop('amount'),
                                         currency=CurrencyCodes.EUR.value,
                                         shop_order_id=random.randint(1, 200000),
                                         extra_fields=description)

            log_info.info(f'> {self._id} > Redirecting user to pay form')
            return render_template('forms/piastrix/pay.html', **response)
        elif self.currency == CurrencyCodes.USD.value:
            response = self.piastrix.bill(payer_currency=CurrencyCodes.USD.value,
                                          shop_amount=self.form_data.pop('amount'),
                                          shop_currency=CurrencyCodes.USD.value,
                                          shop_order_id=random.randint(1, 200000))
            redirect_url = response.get('data', {}).get('url')
            if redirect_url:
                log_info.info(f'> {self._id} > Redirecting user to url: {redirect_url}')
                return redirect(redirect_url, code=302)
            return render_template('forms/piastrix/pay.html', **self.form_data)
        elif self.currency == CurrencyCodes.RUB.value:
            response = self.piastrix.invoice(amount=self.form_data.pop('amount'),
                                             currency=CurrencyCodes.RUB.value,
                                             shop_order_id=random.randint(1, 200000),
                                             payway=settings.PAYWAY)

            log_info.info(f'> {self._id} > Redirecting user to invoice form')
            return render_template('forms/payeer/invoice.html',
                                   **{**response.get('data'),
                                      **response.get('data', {}).get('data')})

        log_info.error(f'> {self._id} > No valid Method for currency: {self.currency}')
