from core import Core


if '__main__' == __name__:
    software = 'Workbench'
    software_version = '2023.2.0-beta'

    core = Core(software, software_version)

    print('------------------- [ STARTING ] -------------------')

    core.print_snapshot_info()

    step1 = '___________________(STEP 1:Generating Snapshot)_______________'
    print(step1)
    core.logs.debug('%s' %step1)
    snapshot = core.snapshot.generate_snapshot()

    step2 = '___________________(STEP 2:Saving Snapshot)___________________'
    print(step2)
    core.logs.debug('%s' %step2)    
    json_file = core.snapshot.save_snapshot(snapshot)

    step3 = '___________________(STEP 3:Uploading Snapshot)________________'
    print(step3)
    core.logs.debug('%s' %step3)
    response = core.snapshot.post_snapshot(snapshot)

    print('------------------- [ FINISHED ] -------------------')

    core.print_summary(json_file, response)
