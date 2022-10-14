from sqlalchemy import false
from src.tables import Cart, Item
from src.db import add_item, setup_engine, setup_session, setup_envvar_engine
from sqlalchemy.orm import Session, sessionmaker
from pytest import fixture
import pytest


@fixture
def setup():
    Session = setup_session(setup_engine())
    yield Session


@fixture(scope="session")
def setup_eng():
    yield setup_envvar_engine()


@fixture
def setup_psql(setup_eng):
    engine = setup_eng
    Session = setup_session(engine)
    with Session.begin() as session:
        session.execute("""TRUNCATE TABLE cart CASCADE""")
    yield Session


def _add(Session: Session):
    with Session.begin() as session:
        assert session.query(Item).count() == 0
        assert session.query(Cart).count() == 0
        item = {
            "external_id": 1,
            "name": "item",
            "value": 1,
        }

        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).count() == 1
        assert session.query(Cart).count() == 1


def _add_multiple(Session: Session):
    with Session.begin() as session:
        assert session.query(Item).count() == 0
        assert session.query(Cart).count() == 0
        item = {
            "external_id": 1,
            "name": "item",
            "value": 1,
        }

        add_item("chocolate_cokkie", item, session)
        item["external_id"] = 2
    with Session.begin() as session:
        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).count() == 2
        assert session.query(Cart).count() == 1


def _update(Session: Session):
    with Session.begin() as session:
        assert session.query(Item).count() == 0
        assert session.query(Cart).count() == 0
        item = {
            "external_id": 1,
            "name": "item",
            "value": 1,
        }
        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).first().name == "item"
        item["name"] = "dsfsdf"
    with Session.begin() as session:
        add_item("chocolate_cokkie", item, session)
        item_q = session.query(Item)
        assert item_q.count() == 1
        assert session.query(Cart).count() == 1
        assert item_q.first().name == "dsfsdf"


def _add_bad(Session: Session):
    with Session.begin() as session:
        assert session.query(Item).count() == 0
        assert session.query(Cart).count() == 0
        item = {
            "external_id": 1,
        }

        add_item("chocolate_cokkie", item, session)
        item_q = session.query(Item)
        assert item_q.count() == 1
        assert session.query(Cart).count() == 1
        assert item_q.first().name == None
        assert item_q.first().value == None
    with Session.begin() as session:
        item = {
            "external_id": 1,
            "name": "item",
            "value": 1,
        }
        add_item("chocolate_cokkie", item, session)
        item_q = session.query(Item)
        all = item_q.all()
        assert item_q.count() == 1
        assert session.query(Cart).count() == 1
        assert item_q.first().name == "item"
        assert item_q.first().value == 1
    with Session.begin() as session:
        item = {
            "external_id": 1,
        }

        add_item("chocolate_cokkie", item, session)
        item_q = session.query(Item)
        assert item_q.count() == 1
        assert session.query(Cart).count() == 1
        assert item_q.first().name == None
        assert item_q.first().value == None


def _add_same(Session: Session):
    with Session.begin() as session:
        assert session.query(Item).count() == 0
        assert session.query(Cart).count() == 0
        item = {
            "external_id": 1,
            "name": "item",
            "value": 1,
        }
    with Session.begin() as session:
        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).count() == 1
        assert session.query(Cart).count() == 1
    with Session.begin() as session:
        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).count() == 1
        assert session.query(Cart).count() == 1


def _multiple_cookies(Session: Session):
    with Session.begin() as session:
        assert session.query(Item).count() == 0
        assert session.query(Cart).count() == 0
        item = {
            "external_id": 1,
            "name": "item",
            "value": 1,
        }
    with Session.begin() as session:
        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).count() == 1
        assert session.query(Cart).count() == 1
    with Session.begin() as session:
        add_item("chocolate_cokkie", item, session)
        assert session.query(Item).count() == 1
        assert session.query(Cart).count() == 1
    with Session.begin() as session:
        add_item("white_chocolate_cokkie", item, session)
        assert session.query(Item).count() == 2
        assert session.query(Cart).count() == 2


def test_add(setup: Session):
    _add(setup)


def test_add_bad(setup: Session):
    _add_bad(setup)


def test_add_multiple(setup: Session):
    _add_multiple(setup)


def test_update(setup: Session):
    _update(setup)


def test_add_same(setup: Session):
    _add_same(setup)


def test_multiple_cookies(setup: Session):
    _multiple_cookies(setup)


@pytest.mark.slow
def test_psql_add(setup_psql: Session):
    _add(setup_psql)


def test_psql_add_bad(setup_psql: Session):
    _add_bad(setup_psql)


@pytest.mark.slow
def test_psql_add_multiple(setup_psql: Session):
    _add_multiple(setup_psql)


@pytest.mark.slow
def test_psql_update(setup_psql: Session):
    _update(setup_psql)


@pytest.mark.slow
def test_psql_add_same(setup_psql: Session):
    _add_same(setup_psql)


@pytest.mark.slow
def test_psql_multiple_cookies(setup_psql: Session):
    _multiple_cookies(setup_psql)
