#!/usr/bin/python3
""" Fabric script that generates a .tgz archive"""


def do_pack():
    """ Creates the tar file"""

    from fabric.api import run
    from datetime import datetime
    import os
    
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(time)
    if not os.path.exists("versions"):
        os.makedirs("versions")
    try:
        run("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None
