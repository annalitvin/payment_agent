
class PiastrixErrorCode:
    ExtraFieldsError = 1000
    IpError = 1001
    SignError = 1002
    ShopAmountError = 1003
    ShopCurrencyError = 1004
    StatusError = 1005
    LanguageError = 1006
    AmountTypeError = 1007


class PiastrixRequestException(Exception):
    def __init__(self, message, error_code):
        self.error_code = error_code
        super().__init__(message)
