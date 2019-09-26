import os
import shutil
import subprocess
import tempfile
import unittest

from mkdocs import config
from mkversion.entry import Entry


# noinspection PyCallByClass,PyCallByClass
class TestEntry(unittest.TestCase):
    temp_dir_path = tempfile.mkdtemp()
    git_repo = 'https://github.com/zayd62/mkdocs-versioning-test'
    setUpFailed = True
    cfg = None

    # noinspection PyCallByClass
    @classmethod
    def setUpClass(cls) -> None:
        """
        Clones the test repository into a temporary directory and navigates into it
        """
        try:
            os.chdir(TestEntry.temp_dir_path)
            print('attempting to download test repository', TestEntry.git_repo, 'to directory', TestEntry.temp_dir_path)
            subprocess.run(['git', 'clone', TestEntry.git_repo], check=True)
            # noinspection PyArgumentList
            os.chdir(os.listdir()[0])
        except OSError as e:
            print(e)
            print('failed to change directory. Could be because the temporary directory was not created')
        except Exception as e:
            print(e)
            print('git clone failed')
        else:
            TestEntry.setUpFailed = False

        if TestEntry.setUpFailed:
            # noinspection PyCallByClass
            TestEntry.fail(TestEntry, 'setup failed. Stopping tests')

        try:
            TestEntry.cfg = config.load_config('mkdocs.yml')
        except Exception as e:
            print(e)
            # noinspection PyCallByClass
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
