import requests
from typing import Optional, Dict, Any

def get_weather(city: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Получает текущие метеоданные для указанного города через OpenWeatherMap API.

    Функция отправляет сетевой запрос, обрабатывает ответ в формате JSON и
    извлекает основные показатели: название города, температуру и описание погоды.

    Args:
        city (str): Название города на английском языке (например, "Moscow").
        api_key (str): Персональный ключ доступа к API OpenWeatherMap.

    Returns:
        Optional[Dict[str, Any]]: Словарь с данными (city, temp, description)
            в случае успеха или None, если город не найден или возникла сетевая ошибка.

    Raises:
        requests.exceptions.RequestException: Может быть вызвано при критических
            проблемах с сетевым соединением.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None

        data = response.json()
        return {
            "city": data.get("name"),
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except Exception:
        return None