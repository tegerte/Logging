# crud.py
import sqlalchemy
from models import Base
from traceback import print_exc


class Crud:
    """
    Class to perform CRUD operations on database.

    """

    def __init__(
        self,
        connection_string=f"sqlite:///log_db.sqlite3",
        encoding="utf-8",
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
    ):

        self.connection_string = connection_string
        self.encoding = encoding
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.engine = None
        self.session = None
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.session = sqlalchemy.orm.Session(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            traceback.print_exception(exception_type, exception_value, traceback)
        self.close_session()
        self.close_all_connections()

    def get_or_create(self, model, **kwargs):
        inst = self.session.query(model).filter_by(**kwargs).first()
        if inst:
            return inst
        else:
            return self.insert(model(**kwargs))

    def insert(self, instances):
        try:
            self.session.add(instances)
            self.session.commit()
            self.session.flush()
            return instances
        except:
            self.session.rollback()
            return None

    def close_session(self):
        try:
            self.session.close()
        except:
            print_exc()
        finally:
            self.session = None

    def close_all_connections(self):
        try:
            self.engine.dispose()
        except:
            print_exc()
        finally:
            self.engine = None
