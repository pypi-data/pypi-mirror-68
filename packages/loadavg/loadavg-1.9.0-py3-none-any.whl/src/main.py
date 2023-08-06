from flask import Flask, jsonify
from sys import argv, exit
from os import getuid, name, system, mkdir, chdir
import psutil
app = Flask(__name__)
logo = r"""
  _                     _                   
 | |  loadaverage.net  | |   /\             
 | |     ___   __ _  __| |  /  \__   ____ _ 
 | |    / _ \ / _` |/ _` | / /\ \ \ / / _` |
 | |___| (_) | (_| | (_| |/ ____ \ V / (_| |
 |______\___/ \__,_|\__,_/_/    \_\_/ \__, |
       v1.0                            __/ |
                                      |___/ 
"""


def is_linux():
    if name == "posix":
        return True
    else:
        return False


if not is_linux():
    print("This program only works on Linux")
    exit(True)

if getuid() != 0:
    print("Run in root !")
    exit(True)

try:
    command = argv[1]
except IndexError:
    system("clear")
    print(logo)
    print("\n\nfor install the loadaverage use this command -> {} install".format(argv[0]))
    print("\nloadavg commands:")
    print("\tloadavg start   -> for start service")
    print("\tloadavg restart -> for restart service")
    print("\tloadavg stop    -> for stop service")
    exit(True)


@app.route('/loadavg')
def loadaverage():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    output = {
        'memory_usage': f"{memory.used // (2**30)}GB/{memory.total // (2**30) + 1}GB",
        'memory_percent': round(memory.percent),
        'cpu_percent': psutil.cpu_percent(),
        'disk_usage': f"{disk.used // (2**30)}GB/{disk.total // (2**30)}GB",
        'disk_percent': round(disk.percent)
    }
    return jsonify(output)


def loadavg():
    if command == "install":
        try:
            mkdir("/etc/.loadavg")
        except FileExistsError:
            pass
        chdir("/etc/.loadavg")
        with open("run_loadavg.sh", mode="w") as load_runner:
            load_runner.write("loadavg run")
            load_runner.close()
        with open("/etc/systemd/system/loadavg.service", mode="w") as service:
            service.write("""
[Unit]
Description=loadavg daemon

[Service]
ExecStart=/bin/bash /etc/.loadavg/run_loadavg.sh
StandardOutput=syslog
StandardError=syslog
syslogIdentifier=loadavg

[Install]
WantedBy=multi-user.target
            """)
            service.close()
            system("systemctl enable loadavg")
            system("systemctl start loadavg")
    elif command == "start":
        system("systemctl start loadavg")
    elif command == "restart":
        system("systemctl restart loadavg")
    elif command == "stop":
        system("systemctl stop loadavg")
    elif command == "run":
        app.run(host='0.0.0.0', port=35629)


if __name__ == "__main__":
    loadavg()
