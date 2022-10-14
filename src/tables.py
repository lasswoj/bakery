from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Item(Base):
    __tablename__ = "item"
    # id is only so that orm dont complain
    id = Column(Integer, autoincrement=True, primary_key=True)
    external_id = Column(String(80))
    name = Column(String(80), nullable=True)
    value = Column(Integer, nullable=True)
    cart_id = Column(ForeignKey("cart.id"))

    def __init__(self, external_id, *args, name=None, value=None, **kwargs):
        self.external_id = external_id
        self.name = name
        self.value = value


class Cart(Base):
    __tablename__ = "cart"
    id = Column(String(80), primary_key=True)

    items = relationship("Item", cascade="all,delete", backref="cart")

    def __init__(self, id):
        self.id = id
