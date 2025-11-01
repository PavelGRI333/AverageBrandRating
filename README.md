Быстрый старт
В командной строке выполните:

    git clone https://github.com/PavelGRI333/AverageBrandRating.git
    cd AverageBrandRating

Если нет poetry:

    pip install poetry

С установленным poetry:

    poetry install

Активируем вертуальное окружение:

    .venv\Scripts\activate

Теперь можно составить отчет:
(загрузите фалы в корень проекта, по умолчанию загружены два готовых файлы)

    python main.py --files products1.csv products2.csv --report average-rating
