import requests

# 1. Настройки
api_key = "КЛЮЧ"  # Сюда вставляется ключ
city = "Moscow"  # Можно поменять на любой город
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

# 2. Делаем запрос к серверу
response = requests.get(url)

# 3. Превращаем ответ из JSON в словарь Python
data = response.json()

# Проверяем, нашел ли сервер город
if data.get("cod") == 200:
    # 4. Извлекаем нужные данные из словаря
    city_name = data["name"]
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    # 5. Вывод результата
    print(f"Погода в городе: {city_name}")
    print(f"Температура: {temp} C")
    print(f"На улице: {description}")
    print(f"Влажность: {humidity}%")
    print(f"Скорость ветра: {wind_speed} м/с")
else:
    print("Ошибка! Проверь API-ключ или название города.")
    print("Ответ сервера:", data.get("message"))