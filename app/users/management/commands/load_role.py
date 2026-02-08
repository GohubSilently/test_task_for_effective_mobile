from .import_data import ImportData
from users.models import Role


class Command(ImportData):
    model = Role
