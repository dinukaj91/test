import docker
import os
from time import sleep
import shutil

#############################
######### WARNING ###########
#############################
# The values of the indexes of the src_db list should match the value of the same indexes of the dest dbs list
# i.e. src_dbs[0] = pf-b2c-insights-staging-ae should have the equivalent countries prenv db on the same index in dest_dbs[0] = pf-b2c-insights-prenv-ae
src_dbs = ["pf-b2c-insights-staging-ae", "pf-b2c-insights-staging-bh", "pf-b2c-insights-staging-eg", "pf-b2c-insights-staging-qa", "pf-b2c-insights-staging-sa"]
dest_dbs = ["pf-b2c-insights-prenv-ae", "pf-b2c-insights-prenv-bh", "pf-b2c-insights-prenv-eg", "pf-b2c-insights-prenv-qa", "pf-b2c-insights-prenv-sa"]

def container_state(container):
    timeout = 1200
    stop_time = 3
    elapsed_time = 0
    while container.status != 'exited' and elapsed_time < timeout:
        container.reload()
        print(container.status)
        sleep(stop_time)
        elapsed_time += stop_time
        continue

os.mkdir("dump")
for src_db, dest_db in zip(src_dbs, dest_dbs):
    client = docker.from_env()
    print("Dumping " + src_db + ".......")
    container = client.containers.run("bchew/dynamodump:latest",
                                      "-m backup --dumpPath /dump "
                                      f" -r ap-southeast-1 -s {src_db}",
                                      volumes={os.path.join(os.getcwd(), "dump"): {'bind': '/dump/', 'mode': 'rw'}},
                                      detach=True)

    container_state(container)
    os.chdir("dump")
    os.rename(src_db, dest_db)
    os.chdir("..")
    print("Restoring " + src_db + " dump to " + dest_db + ".....")
    container = client.containers.run("bchew/dynamodump:latest",
                                      "-m restore --dumpPath /dump "
                                      f"-r ap-southeast-1 -s {dest_db} --noConfirm",
                                      volumes={os.path.join(os.getcwd(), "dump"): {'bind': '/dump/', 'mode': 'rw'}},
                                      detach=True)
    container_state(container)
