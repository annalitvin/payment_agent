
import requests

from urllib.parse import urljoin

from api.abstractions import ApiBase
from api.exeptions import PiastrixErrorCode, PiastrixRequestException
from api.sign import PiastrixSignGenerator
from api import settings

from app.utils import log_info, log_error


class Api(ApiBase):
    def __init__(self, *args, **kwargs):
        self.piastrix_url = settings.PIASTRIX_URL
        self.timeout = 10
        self._id = kwargs.get('_id')

    def post(self, endpoint, req_dict, *args, **kwargs):
        try:
            response = requests.post(urljoin(self.piastrix_url, endpoint),
                                     json=req_dict,
                                     timeout=self.timeout, *args, **kwargs)
            if response is not None and \
                    getattr(response, 'status_code') == 200:
                result = response.json()
                log_info.info(f'> {self._id} > Received responce: {result}')
                if result.get('result'): return result
                elif result.get('error_code'):
                    log_error.info(f'> {self._id} > Error processing '
                                   f'response: {result}')
                raise PiastrixRequestException(result['message'], result['error_code'])
        except requests.exceptions.HTTPError as err:
            log_error.info(f'> {self._id} > HTTPError: {err}')
            raise SystemExit(err)


class PiastrixApi(Api):

    def __init__(self, shop_id: int, secret_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shop_id = shop_id
        self.secret_key = secret_key
        self.headers = {
            'Content-Type': 'application/json',
        }

    def _sign(self, form_data, required_fields):
        return PiastrixSignGenerator(form_data, required_fields, _id=self._id) \
            .generate_signature(self.secret_key)

    @staticmethod
    def _check_extra_fields_keys(extra_fields, req_dict):
        for key in extra_fields:
            if key in req_dict:
                raise PiastrixRequestException("Wrong key in extra_fields. Don't use the same keys as req_dict",
                                              PiastrixErrorCode.ExtraFieldsError)

    def bill(self, payer_currency: int, shop_amount: float, shop_currency: int,
             shop_order_id: str, extra_fields: dict or None = None) -> dict:

        """Billing for payment - bill method

        :param:
            payer_currency: int
            shop_amount: float
            shop_currency: int
            shop_order_id: str
            extra_fields: dict or None (influencing keys: description, payer_account, failed_url,
                            success_url, callback_url)
        :return:
            response: dict (with keys: created, id, lifetime, payer_account,
                    payer_currency, payer_price, shop_amount, shop_currency,
                    shop_id, shop_order_id, shop_refund, url)
        """

        required_fields = ['payer_currency', 'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id']
        req_dict = {
            "payer_currency": payer_currency,
            "shop_amount": shop_amount,
            "shop_currency": shop_currency,
            "shop_id": self.shop_id,
            "shop_order_id": shop_order_id
        }
        if extra_fields is not None:
            self._check_extra_fields_keys(extra_fields, req_dict)
            req_dict.update(extra_fields)
        req_dict.update({'sign': self._sign(req_dict, required_fields)})
        return super().post('bill/create', req_dict, headers=self.headers)

    def invoice(self, amount: float, currency: int, shop_order_id: str,
                payway: str, extra_fields: dict or None = None) -> dict:

        """Billing for other currencies - invoice method

        :param:
            amount: float
            currency: int
            shop_order_id: str
            payway: str
            extra_fields: dict or None (influencing keys: description, phone, failed_url,
                            success_url, callback_url)
        :return:
            response: dict (with keys: data(ac_account_email, ac_amount, ac_currency, ac_fail_url,
                    ac_order_id, ac_ps, ac_sci_name, ac_sign, ac_sub_merchant_url, ac_success_url), id, method, url)
        """

        required_fields = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id']
        req_dict = {
            "amount": amount,
            "currency": currency,
            "shop_id": self.shop_id,
            "payway": payway,
            "shop_order_id": shop_order_id
        }
        if extra_fields is not None:
            self._check_extra_fields_keys(extra_fields, req_dict)
            req_dict.update(extra_fields)
        req_dict.update({'sign': self._sign(req_dict, required_fields)})
        return super().post('invoice/create', req_dict, headers=self.headers)

    def pay(self, amount: float, currency: int, shop_order_id: str,
            extra_fields: dict or None = None, lang: str = 'ru') -> dict:

        """Billing for payment with pay method

        :param:
            amount: float
            currency: int
            shop_order_id: str
            extra_fields: dict or None (influencing keys: description, payway, payer_account,
                    failed_url, success_url, callback_url)
            lang: str ('ru' or 'en', default='ru')
        :return:
            response: tuple (dict (with keys: amount, shop_id, currency, shop_order_id,
                    description, sign) and url)
        """

        if lang not in ('ru', 'en'):
            raise PiastrixRequestException(f'{lang} is not valid language', PiastrixErrorCode.LanguageError)
        required_fields = ['amount', 'currency', 'shop_id', 'shop_order_id']
        form_data = {
            "amount": amount,
            "shop_id": self.shop_id,
            "currency": currency,
            "shop_order_id": shop_order_id
        }
        if extra_fields is not None:
            self._check_extra_fields_keys(extra_fields, form_data)
            form_data.update(extra_fields)
        form_data.update({'sign': self._sign(form_data, required_fields)})

        url = f"https://pay.piastrix.com/{lang}/pay"
        form_data.update({"url": url})
        return form_data
