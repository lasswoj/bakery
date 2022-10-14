
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.tables import Cart, Item, Base
import os


def setup_envvar_engine() -> Engine:
    u_name = os.getenv("u_name", "postgres")
    u_password = os.getenv("u_password", "admin")
    host = os.getenv("host", "localhost")
    db_name = os.getenv("db_name", "postgres")
    uri = f"postgresql://{u_name}:{u_password}@{host}/{db_name}"
    return setup_engine(uri)


def setup_engine(uri="sqlite:///:memory:") -> Engine:
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    return engine


def setup_session(engine: Engine) -> Session:
    return sessionmaker(bind=engine)


def add_item(cart_id: str, j_item: dict, session: Session):
    cart = None
    # so that new value gets updated to None if no supplied
    # (HELP should it work like this?)
    json_item = {"name": None, "value": None}
    json_item.update(j_item)
    new_item = Item(**json_item)
    carts = session.query(Cart).all()
    ids = [x.id for x in carts]
    if cart_id not in ids:
        cart = Cart(cart_id)
        session.add(cart)
        cart.items.append(new_item)
    else:
        cart = carts[ids.index(cart_id)]
        ids = [id.external_id for id in cart.items]
        exid = str(new_item.external_id)
        if exid in ids:
            items = cart.items[ids.index(exid)]
            for k, v in {**json_item}.items():
                setattr(items, k, v)
        else:
            cart.items.append(new_item)
