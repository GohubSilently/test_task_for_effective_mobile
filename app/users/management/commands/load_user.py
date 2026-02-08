from .import_data import ImportData
from users.models import User


class Command(ImportData):
    model = User
