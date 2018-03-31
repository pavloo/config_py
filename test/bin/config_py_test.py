import unittest
import os
from unittest.mock import patch
from config_py.bin.config_py import config_py, CONF_DIR_NAME, ROOT_SRC_DIR, DEV_FILE
import shutil
from click.testing import CliRunner
import filecmp
import re


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_CONFIG_DIR = os.path.join(SCRIPT_DIR, CONF_DIR_NAME)
CUST_MODULE_DIST = 'my_module'


class TestBinConfigPy(unittest.TestCase):

    def tearDown(self):
        super()
        shutil.rmtree(
            ROOT_CONFIG_DIR,
            ignore_errors=True
        )
        shutil.rmtree(
            os.path.join(SCRIPT_DIR, CUST_MODULE_DIST),
            ignore_errors=True
        )

    @patch('os.getcwd')
    def test_create_config_root(self, mock_get_cwd):
        mock_get_cwd.return_value = SCRIPT_DIR
        runner = CliRunner()
        result = runner.invoke(config_py)

        self.assertEqual(0, result.exit_code)

        self.assertTrue(
            filecmp.cmp(
                os.path.join(ROOT_SRC_DIR, '__init__.py'),
                os.path.join(SCRIPT_DIR, CONF_DIR_NAME, '__init__.py')
            )
        )

        self.assertTrue(
            filecmp.cmp(
                os.path.join(ROOT_SRC_DIR, DEV_FILE),
                os.path.join(SCRIPT_DIR, CONF_DIR_NAME, DEV_FILE)
            )
        )

    @patch('os.getcwd')
    def test_create_config_root_fail(self, mock_get_cwd):
        mock_get_cwd.return_value = SCRIPT_DIR
        os.makedirs(ROOT_CONFIG_DIR)

        runner = CliRunner()
        result = runner.invoke(config_py)

        self.assertEqual(1, result.exit_code)

    @patch('os.getcwd')
    def test_create_config_package(self, mock_get_cwd):
        mock_get_cwd.return_value = SCRIPT_DIR
        runner = CliRunner()
        result = runner.invoke(config_py, ['--package', CUST_MODULE_DIST])

        print(result.exception)
        self.assertEqual(0, result.exit_code)

        self.assertTrue(
            filecmp.cmp(
                os.path.join(SCRIPT_DIR, 'fixtures', '__init__.py_'),
                os.path.join(
                    SCRIPT_DIR,
                    CUST_MODULE_DIST,
                    CONF_DIR_NAME,
                    '__init__.py'
                )
            )
        )

        self.assertTrue(
            filecmp.cmp(
                os.path.join(SCRIPT_DIR, 'fixtures', DEV_FILE + '_'),
                os.path.join(
                    SCRIPT_DIR,
                    CUST_MODULE_DIST,
                    CONF_DIR_NAME,
                    DEV_FILE
                )
            )
        )

    @patch('os.getcwd')
    def test_create_config_package_fail(self, mock_get_cwd):
        mock_get_cwd.return_value = SCRIPT_DIR
        os.makedirs(os.path.join(SCRIPT_DIR, CUST_MODULE_DIST, CONF_DIR_NAME))

        runner = CliRunner()
        result = runner.invoke(config_py, ['--package', CUST_MODULE_DIST])

        self.assertEqual(1, result.exit_code)

    def test_get_version(self):
        runner = CliRunner()
        result = runner.invoke(config_py, ['--version'])

        self.assertEqual(0, result.exit_code)
        self.assertRegexpMatches(result.output, re.compile('\d\.\d\.\d'))


if __name__ == '__main__':
    unittest.main()
