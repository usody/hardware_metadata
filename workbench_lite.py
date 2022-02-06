import subprocess
import json
import uuid

from datetime import datetime


class WorkbenchLite:

    def __init__(self):
        self.type = 'Snapshot'
        self.timestamp = datetime.now()
        self.uuid = uuid.uuid4()
        self.software = 'WorkbenchLite'
        self.version = '14.0.0'

    def dmidecode_package_version(self):
        """Getting packages version of dmidecode."""
        cmd = ['dmidecode --version']
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dmidecode_version, errors = proc.communicate()
        proc.wait()

        print('Dmidecode version: ', dmidecode_version)

    def generate_snapshot(self):
        """ Getting dmi table data using dmidecode package
            and generate and save snapshot.json with dmidecode output.
        """
        command = ['dmidecode']
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = proc.communicate()
        proc.wait()

        dmidecode_output = str(output.decode('utf8'))

        snapshot = {'type': 'Snapshot', 'uuid': str(self.uuid), 'version': "14.0.0",
                    'software': 'WorkbenchLite', 'timestamp': str(self.timestamp), 'debug': dmidecode_output}

        with open('snapshot.json', 'w') as file:
            json.dump(snapshot, file, indent=2)

        print('Snapshot json saved!')


if __name__ == '__main__':

    workbench_lite = WorkbenchLite()
    print("Start WB Lite!")
    workbench_lite.generate_snapshot()
    print("Finished WB Lite!")
