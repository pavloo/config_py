import unittest
import os
from unittest.mock import patch
from config_py.bin.config_py import config_py, CONF_DIR_NAME, ROOT_SRC_DIR, DEV_FILE
import shutil
from click.testing import CliRunner


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_CONFIG_DIR = os.path.join(SCRIPT_DIR, CONF_DIR_NAME)


class TestBinConfigPy(unittest.TestCase):

    def tearDown(self):
        super()
        shutil.rmtree(
            ROOT_CONFIG_DIR,
            ignore_errors=True
        )

    @patch('os.getcwd')
    def test_create_config_root(self, mock_get_cwd):
        mock_get_cwd.return_value = SCRIPT_DIR
        runner = CliRunner()
        result = runner.invoke(config_py)
        self.assertEqual(0, result.exit_code)
        with open(os.path.join(ROOT_SRC_DIR, '__init__.py'), 'r') as src, \
             open(os.path.join(SCRIPT_DIR, CONF_DIR_NAME, '__init__.py'), 'r') as dest:
            self.assertEqual(src.read(), dest.read())

        with open(os.path.join(ROOT_SRC_DIR, DEV_FILE), 'r') as src, \
             open(os.path.join(SCRIPT_DIR, CONF_DIR_NAME, DEV_FILE), 'r') as dest:
            self.assertEqual(src.read(), dest.read())


if __name__ == '__main__':
    unittest.main()
