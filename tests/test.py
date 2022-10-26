import json
from pathlib import Path
from unittest.mock import patch
from io import StringIO
import unittest

from workbench_core import WorkbenchCore


def get_snapshot(file_name: str) -> dict:
    """Gets a json fixture and parses it to a dict."""
    with Path(__file__).parent.joinpath('files/snapshots').joinpath(file_name + '.json').open() as file:
        return json.load(file)


class TestWorkbenchLite(unittest.TestCase):
    workbench = WorkbenchCore()

    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_snapshot__check_stdout(self, stdout):
        """
        Test to check if function generate snapshot works properly.
        """
        self.workbench.generate_snapshot()
        expected_stdout = 'Snapshot json saved!\n'
        self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_post_snapshot__response_code_201(self):
        snapshot = get_snapshot('snapshot.full')
        r = self.workbench.post_snapshot(snapshot)
        assert r['code'] == 201

    def test_post_snapshot__response_code_422(self):
        snapshot = get_snapshot('snapshot.empty')
        r = self.workbench.post_snapshot(snapshot)
        assert r['code'] == 422


if __name__ == '__main__':
    unittest.main()
