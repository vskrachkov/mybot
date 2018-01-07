from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

__all__ = ['db', 'migrate']

convention = {
    "ix": 'i_%(column_0_label)s',
    "uq": "u_%(table_name)s_%(column_0_name)s",
    "ck": "c_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(db=db)