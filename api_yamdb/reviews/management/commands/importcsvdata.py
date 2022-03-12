import csv
import logging

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
    encoding='utf-8'
)

CSV_PATH = 'static/data/'

FOREIGN_KEY_FIELDS = ('category', 'author')

DICT = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def CSVSerializer(csvData, model):
    objs = []
    for row in csvData:
        for field in FOREIGN_KEY_FIELDS:
            if field in row:
                row[f'{field}_id'] = row[field]
                del row[field]
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def handle(self, *args, **kwargs):
        for model in DICT:
            try:
                with open(
                    CSV_PATH + DICT[model],
                    newline='',
                    encoding='utf8'
                ) as csv_file:
                    CSVSerializer(csv.DictReader(csv_file), model)
            except Exception as error:
                CommandError(error)
        logging.info('Successfully loaded all data into database')
