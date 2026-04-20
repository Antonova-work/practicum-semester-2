import pytest
from unittest.mock import patch, Mock
from weather_client import get_weather


# Тест №1: Проверка успешного сценария
@patch("weather_client.requests.get")  # Подменяем requests.get внутри weather_client
def test_get_weather_success(mock_get):
    # Имитируем ситуацию, когда сервер ответил корректно (200 OK)
    # 1. Создаем фальшивый объект ответа (Mock)
    mock_response = Mock()
    mock_response.status_code = 200
    # 2. Настраиваем данные, которые якобы прислал сервер
    mock_response.json.return_value = {
        "name": "Moscow",
        "main": {"temp": 15.5},
        "weather": [{"description": "ясно"}]
    }
    # 3. Привязываем этот ответ к вызову нашей функции
    mock_get.return_value = mock_response

    # Выполняем функцию (она думает, что идет в интернет, но попадает в Mock)
    result = get_weather("Moscow", "fake_key")

    # Проверяем, что данные извлечены верно
    assert result["city"] == "Moscow"
    assert result["temp"] == 15.5
    assert "ясно" in result["description"]


# Тест №2: Проверка обработки ошибки "Город не найден"
@patch("weather_client.requests.get")
def test_get_weather_not_found(mock_get):
    # Имитируем ответ сервера 404 (город не найден)
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_weather("UnknownCity", "fake_key")

    # При ошибке API функция вернёт None
    assert result is None


# Тест №3: Проверка реакции на полный обрыв связи (Connection Error)
@patch("weather_client.requests.get")
def test_get_weather_network_error(mock_get):
    """
    Самый важный тест для изоляции. Имитируем исключение (ошибку сети).
    Здесь используется side_effect для генерации ошибки вместо возврата значения.
    """
    mock_get.side_effect = Exception("Connection error")

    # Функция должна поймать это исключение внутри блока try-except и вернуть None
    result = get_weather("Moscow", "fake_key")

    assert result is None