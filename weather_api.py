import openmeteo_requests
from typing import Dict, Union

API_URL = "https://api.open-meteo.com/v1/forecast"
LOCATION = {"latitude": 55.751244, "longitude": 37.618423}  # Координаты Сколтеха


def wind_direction_to_text(degrees: float) -> str:
    """
    Конвертирует направление ветра в градусах в текстовое представление.

    :param degrees: Направление ветра в градусах (0-360).
    :return: Текстовое представление направления ветра.
    """
    if degrees < 0 or degrees >= 360:
        raise ValueError("Значение градусов должно быть в диапазоне от 0 до 360.")

    directions = ["С", "ССВ", "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ", "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ"]
    index = round(degrees / 22.5) % 16
    return directions[index]


def get_weather_data() -> Dict[str, Union[float, str]]:
    """
    Получает текущие погодные данные для заданной локации.

    :return: Словарь с текущими погодными данными.
    """
    open_meteo = openmeteo_requests.Client()
    params = {
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "current": ["temperature_2m", "precipitation", "rain", "showers", "snowfall", "surface_pressure", "wind_speed_10m", "wind_direction_10m"]
    }
    responses = open_meteo.weather_api(API_URL, params=params)

    response = responses[0]  # Обрабатываем первую локацию.
    current = response.Current()  # Текущие значения. Порядок переменных должен совпадать с запрошенным

    weather = {
        "temperature": current.Variables(0).Value(),
        "precipitation": current.Variables(1).Value(),
        "rain": current.Variables(2).Value(),
        "showers": current.Variables(3).Value(),
        "snowfall": current.Variables(4).Value(),
        "surface_pressure": current.Variables(5).Value(),
        "wind_speed": current.Variables(6).Value(),
        "wind_direction": wind_direction_to_text(current.Variables(7).Value()),
    }
    return weather


if __name__ == '__main__':
    weather_data = get_weather_data()
    print(weather_data)
