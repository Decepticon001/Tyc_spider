
from sqlalchemy import Column, String, Integer, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Comp(Base):
    __tablename__ = 'e_corp'
    # __tablename__ = 'comp_info'
    Corp_Id = Column(Integer,primary_key=True)
    Corp_Code = Column(String)
    Corp_Name = Column(String)
    Corp_Type = Column(String)
    Corp_Desc = Column(String)
    legal_person = Column(String)
    Phone = Column(String)
    Email = Column(String)
    Corp_HomePage = Column(String)
    Address = Column(String)
    Area = Column(String)
    Reg_Tm = Column(DateTime)
    Industry = Column(String)
    Scope_Of_Business = Column(String)
    Corp_Product = Column(String)
    Corp_Keywords = Column(String)
    Corp_Product_Desc=Column(String)
    Update_Tm = Column(DateTime)
    # Tyc_Id = Column(String)