import json
from pathlib import Path
from unittest.mock import patch
from io import StringIO
import unittest

from hwmetadata_core import HWMDCore
from hwmetadata_utils import HWMDUtils


def get_snapshot(file_name: str) -> dict:
    """Gets a json fixture and parses it to a dict."""
    with Path(__file__).parent.joinpath('files/snapshots').joinpath(file_name + '.json').open() as file:
        return json.load(file)


class TestHWMD(unittest.TestCase):
    hwmd_core = HWMDCore()

    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_snapshot__check_stdout(self, stdout):
        """
        Test to check if function generate snapshot works properly.
        """
        snapshot = self.hwmd_core.generate_snapshot()
        expected_stdout = [' [INFO] Snapshot generated properly.']
        self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_post_snapshot__response_code_422(self):
        snapshot = get_snapshot('snapshot.empty')
        r = self.hwmd_core.post_snapshot(snapshot)
        if r:
            assert r['code'] == 422
        else:
            assert r == False

    #TODO add more tests


if __name__ == '__main__':
    unittest.main()
