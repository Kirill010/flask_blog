import sqlalchemy as sa
from sqlalchemy import orm
import sqlalchemy.ext.declarative as dec

ORMBase = dec.declarative_base()
__maker = None


def init(db_path):
    global __maker

    if __maker:
        return

    print('Подключение к БД..')

    engine = sa.create_engine(f'sqlite:///{db_path}?check_same_thread=False', echo=False)
    __maker = orm.sessionmaker(bind=engine)

    from . import models

    ORMBase.metadata.create_all(engine)

    print('Подключение к БД прошло успешно')


def create():
    if __maker is None:
        raise RuntimeError('Сначала нужно инициализироваться ORM!')
    return __maker()
