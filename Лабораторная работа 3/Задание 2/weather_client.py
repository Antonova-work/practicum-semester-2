import requests


def get_weather(city, api_key):
    """
    Функция-клиент для получения метеоданных.
    Инкапсулирует логику сетевого запроса и обработки JSON.
    """
    # Формируем URL для запроса к OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    try:
        # Устанавливаем timeout=5, чтобы тест не завис при проблемах с сетью
        response = requests.get(url, timeout=5)

        # Если API вернул ошибку (например, 404 или 401), возвращаем None по условию
        if response.status_code != 200:
            return None

        # Превращаем JSON-строку в словарь Python
        data = response.json()

        # Извлекаем только нужные поля для возврата
        return {
            "city": data.get("name"),
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except Exception:
        # Любая сетевая ошибка (отсутствие связи и т.д.) перехватывается здесь.
        # Вместо краша программы возвращаем None, чтобы тесты прошли успешно.
        return None


if __name__ == "__main__":
    # Пример вызова для проверки вручную
    result = get_weather("Moscow", "КЛЮЧ")
    print(result)


