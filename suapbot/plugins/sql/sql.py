from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Login(Base):
    __tablename__ = 'login'

    id = Column(String, primary_key=True)
    usuario = Column(String)
    senha = Column(String)

class Wait(Base):
	__tablename__ = "waiting"
	
	id = Column(String, primary_key=True)
	_for = Column(String)
	
class Disc(Base):
	__tablename__ = "disciplinas"
	
	id = Column(String, primary_key=True)
	sorted = Column(String)

engine = create_engine("postgresql://postgres:siiKAcHQoCfSHoXyvadPYvZiVFlDBhyF@junction.proxy.rlwy.net:48277/railway")
Base.metadata.create_all(engine)  


Session = sessionmaker(bind=engine)
session = Session()

def add_disc(id, sorted):
	discs = Disc(id=id, sorted=sorted)
	session.add(discs)
	session.commit()
	
def get_disc(id):
	if session.query(Disc).filter_by(id=id).first():
		sorted = session.query(Disc).filter_by(id=str(id)).first().sorted
		return sorted
	return None
	
def add_login(id, username, password):
	user = Login(id=id, usuario=username, senha=password)
	session.add(user)
	session.commit()
	
def remove_login(id):
	_id = session.query(Login).filter(Login.id==str(id)).first()
	if _id:
		session.delete(_id)
		session.commit()
	
def get_login(id):
	if session.query(Login).filter_by(id=id).first() is not None:
		return session.query(Login).filter_by(id=str(id)).first().usuario, session.query(Login).filter_by(id=id).first().senha
	return None
		
def add_wait(id, _for):
	wait = Wait(id=id, _for=_for)
	session.add(wait)
	session.commit()

def remove_wait(id):
	_id = session.query(Wait).filter(Wait.id==str(id)).first()
	if _id:
		session.delete(_id)
		session.commit()

def get_wait(id):
	try:
		return session.query(Wait).filter_by(id=id).first()
	except:
		return None
	finally:
		session.close()

def get_for(id):
	try:
		return session.query(Wait).filter_by(id=id).first()._for
	except:
		return None
	finally:
		session.close()
