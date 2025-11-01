from collections import defaultdict
from .base import Report

class AverageRatingReport(Report):
    def generate(self, data: list) -> list:
        """
        Вычисляет средний рейтинг среди всех брендов
        return
        Список
        """
        brand_ratings = defaultdict(list)

        for row in data:
            try:
                brand = row['brand']
                rating = float(row['rating'])
                brand_ratings[brand].append(rating)
            except (ValueError, KeyError):
                # Если попдется пустой список
                continue

        average_ratings = []
        for brand, ratings in brand_ratings.items():
            if ratings:
                avr_rating = sum(ratings) / len(ratings)
                average_ratings.append((brand, avr_rating))

        average_ratings.sort(key=lambda x: x[1], reverse=True)

        return average_ratings