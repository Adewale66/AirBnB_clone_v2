#!/usr/bin/python3
# Distributes an archive to your web servers, using the function do_deploy


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    from fabric.api import env, put, run
    from os.path import exists
    env.hosts = ["100.25.118.136", "54.160.105.221"]

    if exists(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/" +
            archive_path[9:-4] + "/")
        run("tar -xzf /tmp/" + archive_path[9:] +
            " -C /data/web_static/releases/" +
            archive_path[9:-4] + "/")
        run("rm /tmp/" + archive_path[9:])
        run("mv /data/web_static/releases/" +
            archive_path[9:-4] + "/web_static/* /data/web_static/releases/" +
            archive_path[9:-4] + "/")
        run("rm -rf /data/web_static/releases/" +
            archive_path[9:-4] + "/web_static")
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/" +
            archive_path[9:-4] + "/ /data/web_static/current")
        return True
    except Exception:
        return False
