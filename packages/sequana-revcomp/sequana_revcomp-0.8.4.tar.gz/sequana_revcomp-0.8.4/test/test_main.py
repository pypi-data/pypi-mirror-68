import easydev
import os
import tempfile
import subprocess
import sys


sequana_path = easydev.get_package_location('sequana_revcomp')
sharedir = os.sep.join([sequana_path , "sequana_pipelines", 'revcomp', 'data'])


# 
def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = "sequana_pipelines_revcomp --input-directory {} "
    cmd += "--working-directory {} --force"
    cmd = cmd.format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.revcomp.main as m
    sys.argv = ["test", "--input-directory", sharedir, "--working-directory",
        directory.name, "--force"]
    m.main()


def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory
        cmd = "sequana_pipelines_revcomp --input-directory {} "
        cmd += "--working-directory {} --force"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())
        stat = subprocess.call("sh revcomp.sh".split(), cwd=wk)


def test_version():
    cmd = "sequana_pipelines_revcomp --version"
    subprocess.call(cmd.split())
