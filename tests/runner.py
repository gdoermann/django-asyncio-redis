from django.test.runner import DiscoverRunner


class DatabaselessTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        """ No Database """
        return

    def teardown_databases(self, old_config, **kwargs):
        """ No Database """
        return
