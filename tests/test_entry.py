import logging
import os
import shutil
import subprocess
import tempfile
import unittest

from mkdocs import config

from mkversion.entry import Entry


class TestEntry(unittest.TestCase):
    temp_dir_path = tempfile.mkdtemp()
    git_repo = 'https://github.com/zayd62/mkdocs-versioning-test'
    setUpFailed = True
    cfg = None
    logging.disable(logging.CRITICAL)

    @classmethod
    def setUpClass(cls) -> None:
        """
        various setup code such as;
            - cloning test repository from GitHub into a temporary directory
            - setting up a basic argparse to test the cli commands
        """

        # cloning the test repository
        try:
            os.chdir(TestEntry.temp_dir_path)
            print('attempting to download test repository', TestEntry.git_repo, 'to directory', TestEntry.temp_dir_path)
            subprocess.run(['git', 'clone', TestEntry.git_repo], check=True)
            os.chdir(os.listdir()[0])
        except OSError as e:
            print(e)
            print('failed to change directory. Could be because the temporary directory was not created')
        except Exception as e:
            print(e)
            print('git clone failed')
        else:
            TestEntry.setUpFailed = False

        # failing the test should the setup fail
        if TestEntry.setUpFailed:
            TestEntry.fail(TestEntry, 'setup failed. Stopping tests')

        # loading mkdocs.yml and failing tests if loading fails
        try:
            TestEntry.cfg = config.load_config('mkdocs.yml')
        except Exception as e:
            print(e)
            TestEntry.fail(TestEntry, 'setup failed. Stopping tests')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        delete the cloned git repository from the temporary directory
        """
        print('deleting cloned git repository from', TestEntry.temp_dir_path)
        shutil.rmtree(TestEntry.temp_dir_path)

    def test_extract_version_num(self):
        self.assertTrue(TestEntry.cfg['plugins']['mkdocs-versioning'].extract_version_num() == '2.0.0')

    def test_docs_exists(self):
        folder_name = '1.0.0'
        os.mkdir(folder_name)
        self.assertTrue(Entry.docs_exists(folder_name))

    def test_is_serving(self):
        self.assertTrue(Entry.is_serving(os.getcwd()))


if __name__ == '__main__':
    unittest.main()
