import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

# 1. Список URL для парсинга
urls = [
    "https://www.python.org",
    "https://www.google.com",
    "https://ria.ru",
    "https://www.github.com",
    "https://www.bing.com",
    "https://www.habr.com",
    "https://www.mozilla.org",
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.lenta.ru"
]


# 2. Функция парсинга
def parse_page(url):
    try:
        # Загрузка страницы с таймаутом
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Проверка на HTTP-ошибки

        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлечение заголовка. Если soup.title равен None, обращение к .string вызовет AttributeError
        title = soup.title.string.strip()
        return f"Успешно: {url} | Заголовок: {title}"

    except requests.exceptions.RequestException as e:
        # Обработка проблем с сетью
        return f"Сетевая ошибка: {url} | Детали: {e}"

    except AttributeError:
        # Обработка отсутствующих элементов (тега <title>)
        return f"Ошибка структуры: {url} | Тег <title> не найден"

    except Exception as e:
        # Прочие исключения
        return f"Неизвестная ошибка: {url} | {e}"


# 3. Последовательное выполнение для сравнения
def run_sequential(url_list):
    print("Запуск последовательного парсинга")
    start = time.time()
    results = []
    for url in url_list:
        results.append(parse_page(url))
    end = time.time()
    return results, end - start


# 4. Многопоточное выполнение (ThreadPoolExecutor)
def run_threaded(url_list):
    print(f"Запуск многопоточного парсинга (5 потоков)")
    start = time.time()
    # Создаем пул потоков
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Собираем результаты всех задач
        results = list(executor.map(parse_page, url_list))
    end = time.time()
    return results, end - start


# Выполнение обоих режимов для измерения производительности
res_seq, time_seq = run_sequential(urls)
res_th, time_th = run_threaded(urls)

# Вывод собранной информации
print("\nРЕЗУЛЬТАТЫ ПАРСИНГА:")
for r in res_th:
    print(r)

# 5. Измерение времени и выводы о производительности
print(f"\nСРАВНЕНИЕ СКОРОСТИ")
print(f"Время последовательного выполнения: {time_seq:.2f} сек.")
print(f"Время многопоточного выполнения: {time_th:.2f} сек.")

if time_th > 0:
    improvement = time_seq / time_th
    print(f"Вывод: Многопоточность ускорила работу в {improvement:.1f} раз(а).")