import pytest
from unittest.mock import patch, Mock
# Импортируем функции из нашего основного файла для тестирования.
from parser import parse_news, fetch_html

# тесты логики парсера
def test_parse_news_success():
    """
    Тест проверяет корректность извлечения данных из заранее подготовленного HTML.
    Это гарантирует, что функция parse_news работает правильно независимо от сети.
    Используется стандартный assert из pytest.
    """
    # Создаем поддельный HTML, имитирующий структуру сайта.
    fake_html = """
    <html>
        <body>
            <a class="card-mini" href="/news/item1">Первая новость</a>
            <a class="card-mini" href="https://external.com/item2">Вторая новость</a>
        </body>
    </html>
    """
    results = parse_news(fake_html)

    # Проверка: результат должен быть списком.
    assert isinstance(results, list)
    # Проверка: найдено 2 элемента.
    assert len(results) == 2
    # Проверка: ссылки корректно обработаны (приклеен домен к относительной ссылке).
    assert "https://lenta.ru/news/item1" in results[0]
    # Проверка: заголовок извлечен без лишних пробелов.
    assert "Первая новость" in results[0]


def test_parse_news_empty_or_bad_format():
    # Тест проверяет поведение парсера, если на странице нет нужных данных.
    bad_html = "<html><body>Тут нет новостей с классом card-mini</body></html>"
    results = parse_news(bad_html)

    # Ожидаем пустой список, а не ошибку программы.
    assert results == []


# тесты сетевого взаимодействия с использованием Mock

@patch("parser.requests.get")
def test_fetch_html_mock_success(mock_get):
    """
    Используем patch, чтобы подменить реальный запрос в интернет на Mock-объект.
    Это делает тесты быстрыми и стабильными.
    """
    # Настраиваем имитацию ответа сервера.
    mock_response = Mock()
    # Имитация успешного HTTP-ответа (200 - ОК).
    mock_response.status_code = 200
    mock_response.text = "<html>Content OK</html>"
    # Указываем, что при вызове requests.get вернется наш "поддельный" ответ.
    mock_get.return_value = mock_response

    content = fetch_html("https://any-site.ru")

    # Убеждаемся, что функция вернула текст из нашего Mock-объекта.
    assert content == "<html>Content OK</html>"
    # Проверяем, что запрос действительно был отправлен (вызван Mock-объект).
    mock_get.assert_called_once()


@patch("parser.requests.get")
def test_fetch_html_server_error(mock_get):
    # Проверяем, как парсер обрабатывает ошибки сервера (например, 404).
    mock_response = Mock()
    mock_response.status_code = 404
    # Имитируем поведение raise_for_status при ошибке (вызов исключения).
    # Выкидываем исключение при вызове мока.
    mock_response.raise_for_status.side_effect = Exception("HTTP Error occurred")
    mock_get.return_value = mock_response

    # Проверяем, что наша функция fetch_html "пробрасывает" ошибку наверх.
    with pytest.raises(Exception, match="HTTP Error occurred"):
        fetch_html("https://bad-link.ru")