from unittest.mock import patch

from io import StringIO
import unittest
from workbench_lite import WorkbenchLite


class TestWorkbenchLite(unittest.TestCase):
    workbench_lite = WorkbenchLite()

    @patch('sys.stdout', new_callable=StringIO)
    def test_1_generate_snapshot(self, stdout):
        """
        Test to check if function generate snapshot works properly.
        """
        self.workbench_lite.generate_snapshot()
        expected_stoud = 'Snapshot json saved!\n'
        self.assertEqual(stdout.getvalue(), expected_stoud)


if __name__ == '__main__':
    unittest.main()
