import unittest
from unittest.mock import patch, MagicMock, ANY
import imp
import test
from config_py.lib import import_config


class TestLib(unittest.TestCase):

    def test_reimport_root(self):
        imp.reload(test.lib.config)
        from test.lib.config import TEST
        self.assertEqual('DEV', TEST)

    @patch('os.getenv')
    def test_root_pick_up_different_conf(self, mock_getenv):
        mock_getenv.return_value = 'test'

        imp.reload(test.lib.config)
        from test.lib.config import TEST
        self.assertEqual('TEST', TEST)

    @patch('os.getenv')
    @patch('importlib.import_module')
    def test_import_config_with_package(self, mock_importmodule, mock_getenv):
        global_mock = MagicMock()
        mock_getenv.return_value = 'production'
        to_be_exported = {
            'TEST': 'TEST'
        }
        mock_importmodule.return_value.__dict__ = to_be_exported

        import_config(global_mock, package='my.package.')

        mock_importmodule.assert_called_with(
            '.config_production',
            'my.package.config'
        )
        to_be_exported['env'] = ANY
        global_mock.update.assert_called_with(to_be_exported)

    @patch('importlib.import_module')
    def test_env(self, mock_getenv):
        global_mock = MagicMock()

        import_config(global_mock)

        env = global_mock.update.call_args[0][0]['env']

        self.assertTrue(env.is_dev())
        self.assertFalse(env.is_prod())
        self.assertEquals('dev', env.name)

        with self.assertRaises(AttributeError):
            env.rand()

    @patch('os.getenv')
    @patch('logging.warning')
    def test_root_pick_up_different_conf(self, mock_logging, mock_getenv):
        mock_getenv.return_value = 'stage'
        global_mock = MagicMock()

        import_config(global_mock)
        self.assertTrue(mock_logging.called)

    @patch('os.getenv')
    def test_custom_env_var_name(self, mock_getenv):
        env_var = 'MY_ENV'
        mock_getenv.return_value = 'stage'
        global_mock = MagicMock()

        import_config(global_mock, env_var=env_var)
        mock_getenv.assert_called_with(env_var, 'dev')
