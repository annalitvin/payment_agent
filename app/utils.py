import logging
import logging.config
import yaml


# logging settings
def get_log(filename='config/log/log.yaml'):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f.read())
        return logging.config.dictConfig(config)


log_info, log_error, log_debug, \
       log_warn = logging.getLogger('app.info'), logging.getLogger('app.error'), \
       logging.getLogger('app.debug'), \
       logging.getLogger('app.warn')
