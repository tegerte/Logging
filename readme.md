
# SOME TEST CODE FOR MY USE

Wichtig:

###  im model.py muss an der oberen Tabelle die beziehung zur untergeordneten Tabelle stehen:
```python
class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    level_id = Column(Integer, ForeignKey('levels.id'))
    ...

    level = relationship('Levels')

class Levels(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True)
    level_name = Column(String(20), unique=True, nullable=False)
```


### die Fremdschlüssel Tabelle muss eine unique constraint auf ihrem Attribut haben

```python
class Levels(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True)
    level_name = Column(String(20), unique=True, nullable=False)
```


### Man braucht im CRUD eine function die schaut ob es das attribut schon gibt, wenn nein muss es erzeugt werden
```python
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
```

### beim insert im Handler müssen zuerst die Fremdschlüsseltabellen befüllt/ geprüft werden:

```python
    level = my_crud.get_or_create(Levels, level_name=record.levelname)

    new_log = Log(module=record.module,
                  thread_name=record.threadName,
                  file_name=record.filename,
                  func_name=record.funcName,
                  line_no=record.lineno,
                  process_name=record.processName,
                  message=message,
                  last_line=last_line,
                  level_id=level.id)

    my_crud.insert(instances=new_log)
```

### Crud () als contextmanager:

```python
            try:
                my_crud = Crud()
                with my_crud:
                    level = my_crud.get_or_create(Levels, level_name=record.levelname)

                    new_log = Log(module=record.module,
                                  thread_name=record.threadName,
                                  file_name=record.filename,
                                  func_name=record.funcName,
                                  line_no=record.lineno,
                                  process_name=record.processName,
                                  message=message,
                                  last_line=last_line,
                                  level_id=level.id)

                    my_crud.insert(instances=new_log)
```
Dazu muss die Crud Klasse diese Methoden haben:
```python
    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            traceback.print_exception(exception_type, exception_value, traceback)
        self.close_session()
        self.close_all_connections()
```
Diese Methoden sollen die Verbindungen beenden:
```python
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
            
```



Todo:
- mehr fremdschlüsseltabellen
- logmesages farblich unterscheiden
- mehr logginglevel
- unterscheidung der ausgabemedien nach logginglevel
