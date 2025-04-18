# your_app/router.py
class ActiveDirectoryRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'AD_EVS':
            return 'activedirectory'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'AD_EVS':
            return 'activedirectory'
        return None
