import docker
import os
from time import sleep

#src_dst_db_map = {'pf-b2c-insights-staging-ae': 'pf-b2c-insights-prenv-ae', 'pf-b2c-insights-staging-bh': 'pf-b2c-insights-prenv-bh', 'pf-b2c-insights-staging-eg': 'pf-b2c-insights-prenv-eg', 'pf-b2c-insights-staging-qa': 'pf-b2c-insights-prenv-qa', 'pf-b2c-insights-staging-sa': 'pf-b2c-insights-prenv-sa'}

src_dst_db_map = {'pf-b2c-insights-staging-bh': 'pf-b2c-insights-prenv-bh', 'pf-b2c-insights-staging-eg': 'pf-b2c-insights-prenv-eg'}

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
        
def dump_restore_dynamodb(client, db_name):
    container = client.containers.run("bchew/dynamodump:latest",
                                  "-m backup --dumpPath /dump "
                                  f" -r ap-southeast-1 -s {db_name} --noConfirm",
                                  volumes={os.path.join(os.getcwd(), "dump"): {'bind': '/dump/', 'mode': 'rw'}},
                                  detach=True)
    return container

os.mkdir("dump")
for src_db in src_dst_db_map:
    print(src_db, '->', src_dst_db_map[src_db])
    client = docker.from_env()
    print("Dumping " + src_db + ".......")
    status = dump_restore_dynamodb(client, src_db)
    container_state(status)

