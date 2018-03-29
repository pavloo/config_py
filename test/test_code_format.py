import unittest
import pycodestyle
from os.path import dirname, join

SCRIPT_PATH = dirname(dirname(__file__))


class TestCodeFormat(unittest.TestCase):

    def test_conformance(self):
        """Test that we conform to PEP-8."""
        path_to_config = join(SCRIPT_PATH, 'setup.cfg')
        style = pycodestyle.StyleGuide(quiet=True, config_file=path_to_config)
        result = style.check_files(['./'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings). {0}".format(result.messages))


if __name__ == '__main__':
    unittest.main()
