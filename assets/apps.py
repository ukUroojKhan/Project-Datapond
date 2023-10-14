from django.apps import AppConfig


class UploadFilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_import'

class DataTransformConfig(AppConfig):
    name = 'data_transform'

class DataVisualizationConfig(AppConfig):
    name = 'data_visualization'

class DbDirectoryConfig(AppConfig):
    name = 'db_directory'

class UserAuthConfig(AppConfig):
    name = 'user_auth'