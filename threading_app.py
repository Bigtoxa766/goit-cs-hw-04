from collections import Counter
from threading import Thread
import re


class Keyword_search:
    def __init__(self, file, keywords):
        self.file = file
        self.keywords = keywords
        self.results = {}
    
    def search(self, text, keywords):
        # Створення регулярного виразу для пошуку слів

        pattern = r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b(?:[\s,;:.!?-]*\b(' + '|'.join(map(re.escape, keywords)) + r')\b)*'
        matches = re.findall(pattern, text, re.IGNORECASE)

        # Підрахунок кількості кожного знайденого слова
        return Counter(matches)

def prcess_file(filename, keywords, results):
    # Обробка файлу в окремому потоці

    searcher = Keyword_search(file=None, keywords=keywords)

    try:
        # Відкриваємо файл
        with open(filename, 'r', encoding='utf-8') as f:
            text =f.read().lower()

        # Пошук ключових слів
        word_counts = searcher.search(text, keywords)
        results[filename] = dict(word_counts)

    except Exception as e:
        results[filename] = f"Помилка: {e}"


def main():
    # Список файлів
    file_list = ['add.bmp', 'add2.txt']
    # Ключові слова для пошуку
    keywords = ['менеджер']

    # Створення словника для збереження результатів та список потоків
    results = {}
    threads = []
    
    # Створення та запуск потоків
    for filename in file_list:
        thread = Thread(target=prcess_file, args=(filename, keywords, results))
        threads.append(thread)
        thread.start()

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    # Вивід результатів
    for filename, result in results.items():
        print(f"\nРезультати для файлу {filename}:")

        if isinstance(result, dict):
            for word, count in result.items():
                print(f"Слово '{word}' знайдено {count} разів")
        else:
            print(result)

if __name__ == '__main__':
    main()


