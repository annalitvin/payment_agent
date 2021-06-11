# Piastrix payment service

## Run

``docker-compose build``

``docker-compose up -d``

## SSL

In future planed include ssl certificate.
Now this not work, because amazonaws.com happens to be on 
the blacklist Let’s Encrypt uses for high-risk domain names.

- init-letsencrypt.sh

The script generates a dummy certificate. 
Then, it deletes the dummy certificate once the genuine article has been received.

 - nginx config to include ssl located in ``config/ssl``.

