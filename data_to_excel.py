import pandas as pd
from db import get_last_10_records
from datetime import datetime


def export_to_excel() -> None:
    """
    Экспортирует последние 10 записей погодных данных в Excel файл.

    :return: None
    """
    try:
        records = get_last_10_records()
        cur = datetime.now()
        formatted_time = cur.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"weather_{formatted_time}.xlsx"

        data = [{
            "timestamp": r.timestamp,
            "temperature": r.temperature,
            "wind speed": r.wind_speed,
            "wind direction": r.wind_direction,
            "surface_pressure": r.surface_pressure,
            "precipitation": r.precipitation,
            "rain": r.rain,
            "showers": r.showers,
            "snowfall": r.snowfall

        } for r in records]

        df = pd.DataFrame(data)
        df = df.iloc[::-1]
        df.to_excel(file_name, index=False)
    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")
