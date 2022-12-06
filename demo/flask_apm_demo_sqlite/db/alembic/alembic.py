from flask_alembic import Alembic

ALEMBIC = {
    'script_location': 'flask_apm_demo_sqlite/db/alembic/migrations'
}

alembic = Alembic()


def init_app(app):
    alembic.init_app(app)
