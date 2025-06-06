import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.weather import Base, Weather, WindDirection
from datetime import datetime
import config

# Створення з'єднання з базою даних
engine = create_engine(config.SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Читання CSV-файлу
df = pd.read_csv("data/GlobalWeatherRepository.csv")

for _, row in df.iterrows():
    try:
        weather = Weather(
            country=row["country"],
            cloud=int(row["cloud"]),
            humidity=int(row["humidity"]),
            temperature_celsius=float(row["temperature_celsius"]),
            wind_dir=WindDirection[row["wind_direction"]]
                     if row["wind_direction"] in WindDirection.__members__ else WindDirection.N,
            last_updated=datetime.strptime(row["last_updated"], "%Y-%m-%d %H:%M").date(),
            air_quality_PM2_5=float(row["air_quality_PM2.5"]),
            air_quality_PM10=float(row["air_quality_PM10"]),
            air_quality_Carbon_Monoxide=float(row["air_quality_Carbon_Monoxide"]),
            air_quality_Ozone=float(row["air_quality_Ozone"]),
            air_quality_Nitrogen_dioxide=float(row["air_quality_Nitrogen_dioxide"]),
            air_quality_Sulphur_dioxide=float(row["air_quality_Sulphur_dioxide"]),
            sunrise = datetime.strptime(row["sunrise"], "%I:%M %p").time()
        )
        session.add(weather)
    except Exception as e:
        print("Error processing row:", row.to_dict(), "\nError:", e)

# Фіксування змін у базі даних
session.commit()
