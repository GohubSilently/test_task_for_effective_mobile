from .import_data import ImportData
from users.models import Resource


class Command(ImportData):
    model = Resource
