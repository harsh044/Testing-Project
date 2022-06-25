from django.conf import settings

def validate_register_params(department):
    if int(department) not in settings.DEPARTMENT:
        return 108
    return ""