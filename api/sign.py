import hashlib

from api.abstractions import SignGenerator
from app.utils import log_info, log_error


class PiastrixSignGenerator(SignGenerator):

    def __init__(self, data: dict, keys_required: tuple, **kwargs):
        self.data = data
        self.keys_required = keys_required
        self._id = kwargs.get('_id')

    def _keys_is_valid(self):
        """Check if all required fields have been received.

        :param: None
        :return: bool (True or False)

        """
        data_keys = self.data.keys()
        return all(key in data_keys for key in self.keys_required)

    def _prepare_string(self, secret_key: str):
        """Form a string to generate sha256 hash

        :param secret_key: str
        :return: str (_string)

        """
        if self._keys_is_valid():
            sorted_values = [str(self.data.get(arg))
                             for arg in self.keys_required]
            _string = ':'.join(sorted_values) + secret_key
            log_info.info(f'{self._id} > Constructing string for secret key: '
                          f'{_string} by data: {self.data}')
            return _string
        else:
            log_error.error(f'{self._id} > Error during string preparation '
                            f'for secret generation by data: {self.data}')
            raise ValueError

    def generate_signature(self, secret_key: str):
        """Generate_signature

        :param secret_key:
        :return: str (_hash)

        """
        _secret_string = self._prepare_string(secret_key)
        _hash = hashlib.sha256(_secret_string.encode('utf-8')).hexdigest()
        log_info.info(f'{self._id} > Generating secret key: '
                      f'{_hash} by data: {self.data}')
        return _hash
