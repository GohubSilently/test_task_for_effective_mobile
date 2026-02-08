from .import_data import ImportData
from users.models import Permission


class Command(ImportData):
    model = Permission
