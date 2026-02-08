from .import_data import ImportData
from users.models import Action


class Command(ImportData):
    model = Action
