class DatabaseRouter:
    """
    A database router to control how models are stored in multiple databases.
    """

    def db_for_read(self, model, **hints):
        """ Direct all read operations to the read_db (PostgreSQL) """
        return 'read_db'

    def db_for_write(self, model, **hints):
        """ Direct all write operations to the default (MySQL) """
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ Ensure all migrations apply to both databases """
        return True
