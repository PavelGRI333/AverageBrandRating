import argparse
import csv
import sys

from tabulate import tabulate
import logging

from reports import AverageRatingReport

# Логирование
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# Отображение логов в консоли
hanlder = logging.StreamHandler()
hanlder.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hanlder.setFormatter(formatter)
logger.addHandler(hanlder)

def open_csv_file(files: list[str]) -> list[dict[str, str]]:
    """
    Функция читает данные из файлов csv и обьединяет их в список
    return
    Список словарей с данными из всех файлов
    """
    data = []
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8',) as csv_file:
                read = csv.DictReader(csv_file)
                for elem in read:
                    data.append(elem)
        except FileNotFoundError:
            logger.error(f'Файл {file_path} не найден')
            raise
        except Exception as e:
            logger.exception(f'Ошибка при чтении файла {file_path}: {e}')
            raise
    print(len(data))
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description='Анализ рейтинга брендов')
    parser.add_argument('--files',
                        nargs='+', required=True,
                        help='Путь в csv файлам',
                        )
    parser.add_argument('--report',
                        required=True,
                        help='Название отчета',
                        )
    argspars = parser.parse_args()

    data_from_file = open_csv_file(argspars.files)

    if argspars.report == 'average-rating':
        report = AverageRatingReport()
        result = report.generate(data_from_file)
        headers = ['brand', 'rating']
        table_data = [[brand, f'{rating:.2f}'] for brand, rating in result]
        print(tabulate(table_data, headers=headers, tablefmt='psql'))
        sys.exit(0)
    else:
        logger.error('Данный отчет не доступен')
        sys.exit(1)


if __name__ == "__main__":
    main()