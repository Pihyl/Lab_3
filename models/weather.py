from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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
    sunrise = Column(Time)
    
    # Зв'язок з новою таблицею якості повітря (один до одного)
    air_quality = relationship("AirQuality", back_populates="weather", uselist=False)

class AirQuality(Base):
    __tablename__ = 'air_quality'
    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)
    air_quality_PM2_5 = Column(Float)
    air_quality_PM10 = Column(Float)
    air_quality_Carbon_Monoxide = Column(Float)
    air_quality_Ozone = Column(Float)
    air_quality_Nitrogen_dioxide = Column(Float)
    air_quality_Sulphur_dioxide = Column(Float)
    should_go_out = Column(Boolean)  # Нова булева колонка
    
    # Зворотній зв'язок
    weather = relationship("Weather", back_populates="air_quality")