from app import app, settings

if __name__ == '__main__':
  app.run(host=settings.HOSTNAME,
          port=settings.HTTPS_PORT,
          debug=settings.DEBUG)
