import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from blargh.models import Entry
import blargh.api


class EntryResourceTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        

    def tearDown(self):
        self.testbed.deactivate()
