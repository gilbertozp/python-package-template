"""
Basic tests for packagetemplate

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2017-07-17
"""
import unittest

import packagetemplate

class BasicTest(unittest.TestCase):

    def test_version(self):
        """Test main module has '__version__' attribute"""
        self.assertTrue(hasattr(packagetemplate, '__version__'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
