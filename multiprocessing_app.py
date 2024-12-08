import re
from collections import Counter
from multiprocessing import Process, Manager


class Keyword_search:
    def __init__(self, keywords):
        self.keywords = keywords

    def search(self, text, keywords):
        # Створюємо регулярний вираз для пошуку ключових слів
        pattern = r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b'
        matches = re.findall(pattern, text, re.IGNORECASE)

        # Підраховуємо кількість кожного знайденого слова
        return Counter(matches)


def process_file(filename, keywords, results):
    """Обробка файлу в окремому процесі."""
    searcher = Keyword_search(keywords=keywords)
    try:
        # Відкриваємо файл
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read().lower()

        # Пошук ключових слів
        word_counts = searcher.search(text, keywords)
        results[filename] = dict(word_counts)

    except Exception as e:
        results[filename] = f"Помилка: {e}"


def main():
    # Список файлів
    file_list = ['add.bmp', 'add2.txt']

    # Ключові слова для пошуку
    keywords = ['менеджер', 'проект', 'керування']

    # Використовуємо Manager для створення спільного словника
    with Manager() as manager:
        results = manager.dict() 

        # Створюємо окремий процес для кожного файлу
        processes = []
        for filename in file_list:
            process = Process(target=process_file, args=(filename, keywords, results))
            processes.append(process)
            process.start()

        # Очікуємо завершення всіх процесів
        for process in processes:
            process.join()

        # Виводимо результати
        for filename, result in results.items():
            print(f"\nРезультати для файлу {filename}:")
            if isinstance(result, dict):
                for word, count in result.items():
                    print(f"Слово '{word}' знайдено {count} разів")
            else:
                print(result)  


if __name__ == '__main__':
    main()
