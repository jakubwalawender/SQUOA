from django.test import TestCase
from .tasks import login_users, add


# Create your tests here.
class CeleryTestCase(TestCase):
    def test_celery(self):
        res = add.delay(2, 5)
