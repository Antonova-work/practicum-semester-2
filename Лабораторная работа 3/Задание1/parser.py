import requests
from bs4 import BeautifulSoup


def fetch_html(url):
    """
    Функция для загрузки HTML-кода страницы.
    Использует библиотеку requests для выполнения сетевого запроса.
    Изоляция этой функции позволяет подменить её в тестах через Mock.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    # Выполняем запрос с таймаутом, чтобы тест не завис при сбое сети.
    response = requests.get(url, headers=headers, timeout=5)

    # raise_for_status() проверяет код ответа (например, 200 - ОК, 404 - ошибка).
    # Если код ошибочный, будет вызвано исключение.
    response.raise_for_status()
    return response.text


def parse_news(html):
    """
    Функция парсинга (извлечения данных) из переданного HTML-текста.
    Использует BeautifulSoup для поиска элементов в структуре документа.
    Тестируется отдельно, что гарантирует работу парсера даже без интернета.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем все ссылки с определенным классом.
    news_items = soup.find_all('a', class_='card-mini')

    results = []
    for item in news_items:
        # Извлекаем текст (заголовок) и очищаем от лишних пробелов.
        title = item.text.strip()
        # Получаем значение атрибута 'href' (ссылку).
        link = item.get('href')

        # Если ссылка относительная (начинается с /), превращаем её в абсолютную.
        if link and link.startswith('/'):
            link = "https://lenta.ru" + link

        # Проверяем, что заголовок не пустой.
        if title:
            results.append(f"{title}: {link}")

    # Возвращаем список строк (результаты парсинга).
    return results


if __name__ == "__main__":
    # Точка входа для обычного запуска скрипта.
    target_url = "https://lenta.ru"
    try:
        html_content = fetch_html(target_url)
        news_list = parse_news(html_content)

        # Печатаем первые 10 новостей для демонстрации работы.
        print(f"Найдено новостей: {len(news_list)}")
        for entry in news_list[:10]:
            print(entry)
    except Exception as error:
        print(f"Произошла ошибка при работе парсера: {error}")