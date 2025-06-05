from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class WindDirection(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    NE = "NE"
    NW = "NW"
    SE = "SE"
    SW = "SW"

class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    country = Column(String)
    cloud = Column(Integer)
    humidity = Column(Integer)
    temperature_celsius = Column(Float)
    wind_dir = Column(Enum(WindDirection))
    last_updated = Column(Date)
    air_quality_PM2_5 = Column(Float)
    air_quality_PM10 = Column(Float)
    air_quality_Carbon_Monoxide = Column(Float)
    air_quality_Ozone = Column(Float)
    air_quality_Nitrogen_dioxide = Column(Float)
    air_quality_Sulphur_dioxide = Column(Float)
    sunrise = Column(Time)