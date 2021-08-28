from app import app, db
from app.models import User, Post

# main app module used to run the whole app

@app.shell_context_processor
def make_shell_cotext():
  """Creates the shell context and pre imports everything not like the normal python shell
    run: `flask shell` in terminal to view and reference app """
  return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
  app.run(debug=True)