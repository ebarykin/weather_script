import asyncio
from weather_api import get_weather_data
from db import save_weather_data
from data_to_excel import export_to_excel
import aioconsole


async def fetch_weather_periodically():
    """
    Асинхронно получает погодные данные периодически и сохраняет их.
    Вызывает функции get_weather_data() для получения данных и save_weather_data() для сохранения.

    :return: None
    """
    while True:
        data = get_weather_data()
        save_weather_data(data)
        await asyncio.sleep(60)  # Задать интервал в 180 сек. 60 указано для теста.


async def handle_export_command():
    """
    Асинхронно обрабатывает команды пользователя для экспорта данных в Excel.

    :return: None
    """
    while True:
        command = await aioconsole.ainput("Введите команду (export): ")
        if command == "export":
            try:
                export_to_excel()
                print("Данные экспортированы в weather_Date-Time.xlsx")
            except Exception as e:
                print(f"Ошибка при экспорте данных: {e}")


async def main():
    weather_task = asyncio.create_task(fetch_weather_periodically())
    export_task = asyncio.create_task(handle_export_command())

    await asyncio.gather(weather_task, export_task)


if __name__ == '__main__':
    asyncio.run(main())
