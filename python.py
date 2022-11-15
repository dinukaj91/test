import docker
import os
from time import sleep
import shutil

src_dbs = ["pf-b2c-insights-staging-bh", "pf-b2c-insights-staging-eg"]
dest_dbs = ["pf-b2c-insights-prenv-bh", "pf-b2c-insights-prenv-eg"]

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
