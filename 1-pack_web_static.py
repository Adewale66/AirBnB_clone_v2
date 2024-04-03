#!/usr/bin/python3
""" Fabric script that generates a .tgz archive"""


def do_pack():
    """ Creates the tar file"""

    from fabric.api import run
    from datetime import datetime
    run("mkdir -p versions")
    d = str(datetime.now())\
        .replace("-", "").replace(":", "").replace(" ", "").split(".")[0]
    filename = "web_static_{date}.tgz".format(date=d)
    result = run("tar -cvzf versions/{file} web_static".format(file=filename))
    if result.failed:
        return None
    return filename
