import os
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration settings are defined as class variables inside the Config class.added as more config files are needed
class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or '|\xf1<-\xde\xa8g6\x96\xf3\x9c\xcb\xd2\xf8\xce\x9et!\x99\xec\xc3\xd2l\xb3\x02\x92[\xae\xeagY\xa8'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
  