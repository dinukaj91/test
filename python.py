﻿import docker
import os
from time import sleep
import shutil

x = ["pf-b2c-insights-staging-bh"]
y = ["pf-b2c-insights-prenv-bh"]

#x = ["pf-b2c-insights-staging-bh", "pf-b2c-insights-staging-eg"]
#y = ["pf-b2c-insights-prenv-bh", "pf-b2c-insights-staging-eg"]

def my_function(container):
    timeout = 1200
    stop_time = 3
    elapsed_time = 0
    while container.status != 'exited' and elapsed_time < timeout:
        container.reload()
        print(container.status)
        sleep(stop_time)
        elapsed_time += stop_time
        continue

for i, j in zip(x, y):
    client = docker.from_env()
    shutil.rmtree(os.path.join(os.getcwd(), "dump"), ignore_errors=True)
    os.mkdir("dump")
    container = client.containers.run("bchew/dynamodump:latest",
                                      "-m backup --dumpPath /dump --accessKey AKIAZCUZQZIUUH2LACEE --secretKey "
                                      f"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 -r ap-southeast-1 -s {i}",
                                      volumes={os.path.join(os.getcwd(), "dump"): {'bind': '/dump/', 'mode': 'rw'}},
                                      detach=True)

    my_function(container)
    os.chdir("dump")
    os.rename(i, j)
    os.chdir("..")