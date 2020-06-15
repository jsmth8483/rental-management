from app import create_app, db
from app.models import User, Property

import db_setup

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Property': Property}