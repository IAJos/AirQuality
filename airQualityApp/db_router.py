class UserDatabaseRouter:
    @staticmethod
    def db_for_read(model, **hints):
        """
        Point read operations to the appropriate database.
        """
        if hasattr(model, '_database'):
            return model._database
        return 'default'

    @staticmethod
    def db_for_write(model, **hints):
        """
        Point write operations to the appropriate database.
        """
        if hasattr(model, '_database'):
            return model._database
        return 'default'

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database.
        """
        db_list = ['postgres_user', 'jos_user']
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        """
        Ensure that migrations are only applied to the default database.
        """
        return db == 'default'
