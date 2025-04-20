<<<<<<< HEAD
=======
# your_app/router.py
>>>>>>> f1d7af53b2ec1c899a873523aef130c85bdfcbd5
class ActiveDirectoryRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'AD_EVS':
            return 'activedirectory'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'AD_EVS':
            return 'activedirectory'
        return None
<<<<<<< HEAD

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'AD_EVS':
            return db == 'activedirectory'
        return None
=======
>>>>>>> f1d7af53b2ec1c899a873523aef130c85bdfcbd5
