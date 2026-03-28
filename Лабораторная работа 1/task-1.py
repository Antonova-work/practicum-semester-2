import requests
from bs4 import BeautifulSoup

# 1. Настройки
url = "https://lenta.ru"
headers = {"User-Agent": "Mozilla/5.0"}

# 2. Получаем страницу
response = requests.get(url, headers=headers)
# Проверяем код ответа (должен быть 200)
print("Статус ответа:", response.status_code)


# 3. Готовим парсер
soup = BeautifulSoup(response.text, 'html.parser')

# 4. Ищем все ссылки на новости (тег 'a' с нужным классом)
news_items = soup.find_all('a', class_='card-mini')

# 5. Собираем данные в список
results = []
for item in news_items:
    title = item.text.strip()
    link = item.get('href')

    # Склеиваем ссылку, если она относительная
    if link.startswith('/'):
        link = "https://lenta.ru" + link

    results.append(f"{title}: {link}")

# 6. Печатаем первые 10 штук в консоль и сохраняем в файл
print(f"\nНайдено всего: {len(results)} новостей. Первые 10:\n")

with open("news.txt", "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")
        # Печатаем только первые 10, чтобы не забивать экран
        if results.index(line) < 10:
            print(line)

print("\nГотово! Проверьте файл news.txt")