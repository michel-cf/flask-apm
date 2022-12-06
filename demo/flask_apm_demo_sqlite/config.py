import os


def configure(app):
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    app.config['ALEMBIC'] = {
        'script_location': 'db/alembic/migrations'
    }

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI") or 'sqlite:///sqlite_db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Jinja2 template rendering
    app.jinja_options['trim_blocks'] = True
    app.jinja_options['lstrip_blocks'] = True

    # APM config
    app.config['APM'] = {
        'trace': {
            'logging': False
        }
    }
    