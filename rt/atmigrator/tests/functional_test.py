import unittest2 as unittest
from zope.component import getUtility

from rt.atmigrator.testing import ATMIGRATOR_FUNCTIONAL_TESTING
from rt.atmigrator.migrator import migrateContents

class TestATMigratorMigrator(unittest.TestCase):

    layer = ATMIGRATOR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_migrator(self):
        """
        """