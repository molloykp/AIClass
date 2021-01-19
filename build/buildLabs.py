#!/usr/bin/env python3


"""
Compiles jupyter notebooks with nbgrader and move 
student files into place in the www directory so that the
website construction script picks them up.
"""


import os
import shutil
import sys

# command to use for os.system
NBGRADER_CMD = "nbgrader generate_assignment"

# default course paths to build
LAB_LOC = "../labs"
NBGRADER_LOC = ["../nbgrader"]

def runLocalBuild():
    locBuildFile = './localBuild.sh'

    if os.path.isfile(locBuildFile):
        os.system(locBuildFile + ' >' + locBuildFile + '.log' + ' 2>&1')

def nbgrader(nbgrader_dir, assignment_name,lab_dir, nbgrader_path_abs):

    sys.stdout.flush()

    os.chdir(nbgrader_path_abs)

    cmd = NBGRADER_CMD + ' ' + assignment_name + ' --force'
    print('running:', cmd, ' from :',os.getcwd(),end='')
    status = os.system(cmd) #  + " > _nbgrader_1.run 2>&1")
    if status == 0:
        print("...Completed OK")
    else:
        print("completed with ERROR")
        return status

    assignment_dir = os.path.join(nbgrader_path_abs, 'release',assignment_name)
    print('copying files in:', assignment_dir)


    labPath = os.path.join(lab_dir,'www')
    for filename in os.listdir(assignment_dir):
        print('file in release area:', filename)
        srcFile=os.path.join(assignment_dir, filename)
        if (filename.endswith('.ipynb') or filename.endswith('.py')) and os.path.isfile(srcFile):
            targetFile = os.path.join(labPath,filename)
            print('Copying filename', srcFile, ' to labdir:', targetFile)
            shutil.copyfile(srcFile,targetFile)

    print('')


def build(path, name,lab_path_abs, nbgrader_path_abs):
    """Build the given source file."""

    # join last directory into lab path
    path, last_dir = os.path.split(path)
    testdir = os.path.join(lab_path_abs,last_dir)
    
    if not os.path.isdir(testdir):
        return
    
    print('Debug: path:',path)
    print('       last_dir:', last_dir)
    print('       name:', name)

    print('building:',os.path.join(path, last_dir), ' labloc:',testdir)

    # build student version

    if name.endswith('ipynb'):
        status = nbgrader(path,last_dir,testdir,nbgrader_path_abs)
    """
    else: # it is a simple copy
        labPath = os.path.join(lab_dir,'www')
        srcFile=os.path.join(assignment_dir, filename)
        targetFile = os.path.join(labPath,filename)
        print('Copying filename', srcFile, ' to labdir:', targetFile)
        shutil.copyfile(srcFile,targetFile)
    """ 

    #runLocalBuild()

    # delete temp activity

def main(courses, pattern):
    """Find and build all files."""
    # get abs path to labs
    lab_path_abs = os.path.abspath(LAB_LOC)
    print('Settings\n-----------')
    print('Lab path:',lab_path_abs)

    cwd = os.getcwd()
    for root in courses:
        os.chdir(root)
        cwd = os.getcwd()
        print('scanning from:', cwd,'\n')
        nbgrader_path_abs = os.path.abspath(os.getcwd())
        for path, dirs, files in sorted(os.walk('.')):

            for name in files:
                # build tex files
                if (name.endswith(".ipynb") or name.endswith(".py")) and path.startswith('./source'):
                    if pattern == "all" or pattern in name:
                        os.chdir(path)
                        status = build(path, name,lab_path_abs, nbgrader_path_abs)
                        if status:
                            return status
                        os.chdir(cwd)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(NBGRADER_LOC, sys.argv[1])
    else:
        print("Usage: buildLabs.py {all | NAME}")
        print("NAME is any substring of the file(s)")
