from flask.cli import FlaskGroup

from web import app, db
from web.db_handler import print_all_tables_data, seed_random_data

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    seed_random_data()


@cli.command("print_all")
def print_all():
    print_all_tables_data()


if __name__ == "__main__":
    cli()
