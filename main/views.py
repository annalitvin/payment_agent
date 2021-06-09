
from flask import render_template, request, session

from api.constants import CurrencyCodes
from app.utils import log_info
from main.utils import get_transaction_identifier
from flask import Blueprint


from main.forms import RegistrationForm
from main.factory import PiastrixViewFactory

pages = Blueprint(name='pages', import_name=__name__,
                  template_folder='templates', static_folder='static',
                  static_url_path='/main/static')


@pages.route('/', methods=['get', 'post'])
def pay():

    _id = get_transaction_identifier()
    form = RegistrationForm(request.form, meta={'csrf_context': session})
    if request.method == 'POST' and form.validate():
        try:
            currency_code = getattr(CurrencyCodes, form.currency.data).value
            print(form.data)
        except AttributeError:
            message = 'Invalid currency code'
            return render_template('main.html',
                                   form=form, message=message)
        _data = form.data.copy()
        log_info.info(f'{_id} > Received data from form {_data}')
        method = PiastrixViewFactory(form.data, currency_code, _id=_id)
        return method.get_method()

    elif form.csrf_token.errors:
        log_info.error(f'> {_id} > Form submitted without CSRF')

    return render_template('forms/main.html', form=form)
