from sqlalchemy import create_engine, Column, Integer, Float, String, desc, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Dict, Type

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    surface_pressure = Column(Float)
    precipitation = Column(Float)
    rain = Column(Float)
    showers = Column(Float)
    snowfall = Column(Float)


engine = create_engine('sqlite:///weather.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def save_weather_data(data: Dict[str, float]) -> None:
    """
    Сохраняет погодные данные в базу данных.

    :param data: Словарь с погодными данными.
    :return: None
    """
    weather = WeatherData(
        timestamp=datetime.now(),
        temperature=data["temperature"],
        wind_speed=data["wind_speed"],
        wind_direction=data["wind_direction"],
        surface_pressure=data["surface_pressure"],
        precipitation=data["precipitation"],
        rain=data["rain"],
        showers=data["showers"],
        snowfall=data["snowfall"],
    )
    session.add(weather)
    session.commit()


def get_last_10_records() -> list[Type[WeatherData]]:
    """
    Возвращает последние 10 записей с погодными данными.

    :return: Список из 10 последних объектов WeatherData.
    """
    return session.query(WeatherData).order_by(desc(WeatherData.id)).limit(10).all()
