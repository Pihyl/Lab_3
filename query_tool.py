from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Імпортуємо наші ORM-моделі
from models.weather import Weather
from config import SQLALCHEMY_DATABASE_URL

def main():
    # Створюємо engine та session
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Запит параметрів у користувача
    country = input("Введіть країну: ").strip()
    date_input = input("Введіть дату (YYYY-MM-DD): ").strip()
    
    # Перетворення введеної дати у datetime.date
    try:
        last_updated_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Невірний формат дати. Використовуйте YYYY-MM-DD.")
        return
    
    # Якщо бажаєте додати ще параметри, можна розширити цей блок
    # Наприклад, запитати поріг температури, мінімальну вологость тощо
    # threshold = input("Введіть мінімальну температуру: ").strip()  # Приклад додаткового фільтру

    # Виконуємо запит до бази даних, фільтруючи за країною та датою оновлення
    weather_records = session.query(Weather).filter(
        Weather.country == country,
        Weather.last_updated == last_updated_date
    ).all()
    
    if not weather_records:
        print("Немає даних про погоду для заданих параметрів!")
        return

    # Виводимо дані для кожного знайденого запису
    for weather in weather_records:
        print("\n----------------------------")
        print("Інформація про погоду:")
        print(f"ID: {weather.id}")
        print(f"Країна: {weather.country}")
        print(f"Дата оновлення: {weather.last_updated}")
        print(f"Температура (°C): {weather.temperature_celsius}")
        print(f"Вологість (%): {weather.humidity}")
        print(f"Хмарність: {weather.cloud}")
        print(f"Час сходу: {weather.sunrise}")
        print(f"Напрямок вітру: {(weather.wind_dir.value if weather.wind_dir else 'Невідомо')}")
        
        # Перевіряємо наявність пов'язаної інформації про якість повітря
        if weather.air_quality:
            aq = weather.air_quality
            print("\nІнформація про якість повітря:")
            print(f"PM2.5: {aq.air_quality_PM2_5}")
            print(f"PM10: {aq.air_quality_PM10}")
            print(f"Carbon Monoxide: {aq.air_quality_Carbon_Monoxide}")
            print(f"Ozone: {aq.air_quality_Ozone}")
            print(f"Nitrogen Dioxide: {aq.air_quality_Nitrogen_dioxide}")
            print(f"Sulphur Dioxide: {aq.air_quality_Sulphur_dioxide}")
            recommendation = "Можна виходити на вулицю" if aq.should_go_out else "Краще залишайтесь вдома"
            print(f"Рекомендація: {recommendation}")
        else:
            print("\nІнформації про якість повітря немає.")
    print("\n----------------------------")

if __name__ == '__main__':
    main()
