import cli
from io import StringIO
from unittest import TestCase, mock


class TestLocalInstaller(TestCase):

    @mock.patch('cli.is_git_repository', return_value=True)
    def test_paths(self, mock_is_git_repository):
        installer = cli.Installer(mode='local', path='\\path\\to\\repository')
        self.assertEqual(installer.get_git_attributes_path(), '\\path\\to\\repository\\.gitattributes')
        self.assertEqual(installer.get_git_attributes_path(), '\\path\\to\\repository\\.gitattributes')

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_frozen', return_value=True)
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=False)
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_can_install_when_files_do_not_exist(self, mock_file_open, mock_path_exists,
                                                 mock_is_git_repository, mock_is_frozen, mock_run):
        installer = cli.Installer(mode='local', path='\\path\\to\\repository')
        installer.install()
        mock_run.assert_has_calls([
            mock.call(['git', 'config', 'diff.xl.command', 'git-xl-diff.exe'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8'),
        ])
        mock_file_open.assert_has_calls([
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('*.xla diff=xl\n*.xlam diff=xl\n*.xls diff=xl\n*.xlsb diff=xl\n*.xlsm diff=xl\n*.xlsx diff=xl\n*.xlt diff=xl\n*.xltm diff=xl\n*.xltx diff=xl'),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitignore', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('~$*.xla\n~$*.xlam\n~$*.xls\n~$*.xlsb\n~$*.xlsm\n~$*.xlsx\n~$*.xlt\n~$*.xltm\n~$*.xltx'),
            mock.call().__exit__(None, None, None)
        ])

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_frozen', return_value=True)
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=True)
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='something\n')
    def test_can_install_when_files_exist(self, mock_file_open, mock_path_exists,
                                          mock_is_git_repository, mock_is_frozen, mock_run):
        installer = cli.Installer(mode='local', path='\\path\\to\\repository')
        installer.install()
        mock_run.assert_has_calls([
            mock.call(['git', 'config', 'diff.xl.command', 'git-xl-diff.exe'], cwd='\\path\\to\\repository', stderr=-1,
                      stdout=-1, universal_newlines=True, encoding='utf-8')
        ])
        mock_file_open.assert_has_calls([
            mock.call('\\path\\to\\repository\\.gitattributes', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),

            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('*.xla diff=xl\n*.xlam diff=xl\n*.xls diff=xl\n*.xlsb diff=xl\n*.xlsm diff=xl\n*.xlsx diff=xl\n*.xlt diff=xl\n*.xltm diff=xl\n*.xltx diff=xl\nsomething'),
            mock.call().__exit__(None, None, None),

            mock.call('\\path\\to\\repository\\.gitignore', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),

            mock.call('\\path\\to\\repository\\.gitignore', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('something\n~$*.xla\n~$*.xlam\n~$*.xls\n~$*.xlsb\n~$*.xlsm\n~$*.xlsx\n~$*.xlt\n~$*.xltm\n~$*.xltx'),
            mock.call().__exit__(None, None, None)
        ])

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=False)
    @mock.patch('cli.os.remove')
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_can_uninstall_when_files_do_not_exist(self, mock_file_open, mock_os_remove,  mock_path_exists, mock_is_git_repository, mock_run):
        installer = cli.Installer(mode='local', path='\\path\\to\\repository')
        installer.uninstall()
        mock_run.assert_called_once_with(['git', 'config', '--list'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')
        mock_os_remove.assert_has_calls([])


    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=True)
    @mock.patch('cli.os.remove')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='something')
    def test_can_uninstall_when_files_exist(self, mock_file_open, mock_os_remove,  mock_path_exists, mock_is_git_repository, mock_run):
        installer = cli.Installer(mode='local', path='\\path\\to\\repository')
        installer.uninstall()
        mock_run.assert_called_once_with(['git', 'config', '--list'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')
        self.assertEqual(mock_os_remove.call_count, 0)
        mock_file_open.assert_has_calls([
            mock.call('\\path\\to\\repository\\.gitattributes', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('something'),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('something'),
            mock.call().__exit__(None, None, None)
        ])


class TestGlobalInstaller(TestCase):

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.Installer.get_git_attributes_path')
    @mock.patch('cli.Installer.get_git_ignore_path')
    def test_global_gitconfig_dir(self, mock_get_git_ignore_path, mock_get_git_attributes_path, mock_run):
        installer = cli.Installer(mode='global')
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_has_calls([
            mock.call(['git', 'config', '--global', '--list', '--show-origin'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8'),
            mock.call(['git', 'config', '--global', '--list'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')
        ])

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.Installer.get_global_gitconfig_dir')
    @mock.patch('cli.Installer.get_git_ignore_path')
    def test_global_gitattributes_path(self, mock_get_git_ignore_path, get_global_gitconfig_dir, mock_run):
        mock_completed_process = mock.Mock()
        mock_completed_process.configure_mock(**{'stdout': '.gitconfig'})
        mock_run.return_value = mock_completed_process
        installer = cli.Installer(mode='global')
        self.assertEqual(mock_run.call_count, 1)
        mock_run.assert_called_once_with(['git', 'config', '--global', '--get', 'core.attributesfile'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')


class TestHelp(TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_generic_help(self, mock_stdout):
        command_parser = cli.CommandParser(['help'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.HELP_GENERIC + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help_install(self, mock_stdout):
        command_parser = cli.CommandParser(['help', 'install'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.HELP_INSTALL + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help_uninstall(self, mock_stdout):
        command_parser = cli.CommandParser(['help', 'uninstall'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.HELP_UNINSTALL + '\n')


class CommandParser(TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        command_parser = cli.CommandParser(['version'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.GIT_XL_VERSION + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_env(self, mock_stdout):
        command_parser = cli.CommandParser(['env'])
        command_parser.execute()
        self.assertTrue(mock_stdout.getvalue())

