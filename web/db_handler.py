import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy.sql.expression import func

from web import db


SECONDS_IN_YEAR = 86400 * 365


class Superheroes(db.Model):
    __tablename__ = "superheroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    power = db.Column(db.Integer, db.CheckConstraint('1 <= power and power <= 10'), nullable=False)
    is_villain = db.Column(db.Boolean, nullable=False)
    deceased_date = db.Column(
        db.DateTime(timezone=True),
    )

    def __repr__(self):
        side = "bad" if self.is_villain else "good"
        return f"{self.name}, power {self.power}, {side} guy"


class Chronicles(db.Model):
    __tablename__ = "chronicles"

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('superheroes.id', ondelete="CASCADE"))
    year = db.Column(db.Integer, db.CheckConstraint('2000 <= year and year <= 2100'), nullable=False)
    text = db.Column(db.String)
    hero = db.relationship('Superheroes')


def fill_out_random_data():
    fake = Faker()
    for i in range(1, 21):
        hero = Superheroes(
            name=fake.name(),
            power=random.randint(1, 10),
            is_villain=random.choice((True, False))
        )
        db.session.add(hero)
    db.session.commit()
    heroes = Superheroes.query.all()
    for hero in heroes:
        chronicle = Chronicles(
            hero_id=hero.id,
            year=random.randint(2000, 2010),
            text="Finished Python school"
        )
        db.session.add(chronicle)
    db.session.commit()


def get_heroes():
    return Superheroes.query.order_by(Superheroes.id).all()


def get_chronicles():
    return Chronicles.query.order_by(Chronicles.year).all()


def print_all_tables_data():
    tables = db.engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    for table in tables:
        result = db.engine.execute(f"SELECT * FROM {table.table_name}")
        if result.rowcount == 0:
            print(f"{table.table_name}. Table is empty")
            continue
        print(f"{table.table_name}, {result.rowcount} entries")
        for row in result:
            print(row)


def thanos_snap(hero_id: int):
    hero = Superheroes.query.get(hero_id)
    if not hero:
        print(f"Hero {hero_id} not found")
        return

    db.session.delete(hero)
    db.session.commit()
    print(f"Hero {hero_id} deleted")


def heroes_encounter(year: int):
    heroes = Superheroes.query.filter_by(deceased_date=None)
    bad_guy = heroes.filter_by(is_villain=True).order_by(func.random()).first()
    good_guy = heroes.filter_by(is_villain=False).order_by(func.random()).first()
    if not bad_guy or not good_guy:
        print("Not enough heroes in this Universe!")
        return
    goodness_wins = random.randint(0, 1) == 1
    battle_date = date(year, 1, 1) + timedelta(seconds=random.randint(1, SECONDS_IN_YEAR))
    if goodness_wins:
        defeated = bad_guy
        winner = good_guy
    else:
        defeated = good_guy
        winner = bad_guy
    defeated.deceased_date = battle_date
    chronicle = Chronicles(
        hero_id=winner.id,
        year=year,
        text=f"Defeated {defeated.name}"
    )
    db.session.add(chronicle)
    db.session.commit()


def seed_random_data():
    fill_out_random_data()
    hero = Superheroes.query.order_by(func.random()).first()
    thanos_snap(hero.id)
    for i in range(5):
        heroes_encounter(random.randint(2050, 2100))
