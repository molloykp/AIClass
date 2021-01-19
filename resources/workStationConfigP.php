This document outlines how to config a workstatiion
with all the required software for Machine Learning.
This document outlines how to create this environment
on one of the following environments:
<ul>
    <li>Mac/OS</li>
    <li>Ubuntu/Mint 20</li>
    <li>Virtual Box running Ubuntu/Mint 20.  (see
    <a href="virtualBoxInstall.php">instructions for install a VM with Ubuntu/Mint 20</a>)</li>
</ul>

<h3>Limited MS Windows Support</h3>
In theory, Python and the required packages <b>should</b> run in a Windows
environment, however, limited assistance will be available
for Windows installations.
<h3> Configuring a Development Environment </h3>

<div style="padding-left:2em;">

    This document contains the procedure for building a programming/development
    environment for this AI class.


    <h4>Install Python</h4>
    <div style="padding-left:2em;">
        <h4>Install Python on a MAC</h4>
        <div style="padding-left:2em;">
            Just visit <a href="https://python.org">python.org</a> and download the latest version that
            is above 3.7.  Run the .pkg file that you download and Python should be installed. To run
            this version of Python from the command line, simply type in the python followed by the
            version number, for example:
            <pre><code class="language-shell" data-lang="bash" style="white-space: pre-line ">
                    python3.7</code></pre>

        </div>

        This class will utilize Python 3 and recommends at least Python 3.7 (or higher).
        <h4>Virtual Environment (venv) on Ubuntu/Mint</h4>
        <div style="padding-left:2em;">
           Simply use apt-get if you running Ubuntu/Mint 20.

            <pre><code class="language-shell" data-lang="bash" style="white-space: pre-line ">
                    sudo apt-get update
                    sudo apt-get install python3-distutils python3-pip python3-dev python3-venv
                </code></pre>
        </div>
        <h4>Install on Windows</h4>
        <div style="padding-left:2em;">
            Just visit <a href="https://python.org">python.org</a> and download the latest version that
            is above 3.7.  I downloaded the Windows embeddable package (64-bit), unzipped the
            file, and then I could run the python.exe located in that directory.
        </div>

    </div>


    <h4>Setup up a Virtual Python Environment (venv)</h4>
    <div style="padding-left:2em;">
        A virutal python environment allows the installation of packages and
        tools that are only visable in that environment.  It avoids conflicts
        between packages.

        To create a virtual environment, follow these steps:
        <pre><code class="language-shell" data-lang="bash" style="white-space: pre-line ">cd # places you in your home directory
                python3.7 -m venv cs444_venv</code></pre>

        To activate your virtual environment, execute the following command:
        <pre><code class="language-shell" data-lang="bash" style="white-space: pre-line ">
                source $HOME/cs444_venv/bin/activate
            </code></pre>

        After sourcing this file, your prompt should now be prefixed
        with <i><b>(cs444_venv)</b></i>.  In the image, it says cs445 (because
        I borrowed the image from my machine learning class).

        <img src="ubuntu_source_venv_command.png" class="rounded mx-auto" style="display: block;">

        You will probably want this environment setup each time use start
        the shell, which can be accomplished by adding this to your <b>.bashrc</b> file for Ubuntu/Mint
        or your <b>.bash_profile</b> file on Mac.
    </div>



    <h4>Install Python ToolSets</h4>
    <div style="padding-left:2em;">
        The remaining steps install Python software packages utilizing
        pip (a package manager for Python).  For this class, I highly
        recommend creating a virtual python environment (as detailed
        in the prior step).

        The following procedure will work on Mac or Ubuntu and should work on
        Windows from a shell configured to access the correct version of
        Python (running activiate as described above).  You can also install
        these packages using PyCharm (the next section details how to install
        PyCharm).

        First, start a terminal window by click on the black screen icon, located
        in the bottom left corner (for me, it is the 4th small icon from the left).
        Next, make sure you <i>venv</i> environment is active by doing one of the
        following commands (Ubuntu/Mac only):
        <ul>
            <li><b><i>which python</i></b> command   (make sure that path
            is to the python link in your venv)
            </li>
            <li>Notice that your shell prompt has the venv environment
            name prefixd in the front (as shown in the image of the terminal window
            from the prior section)
            </li>
        </ul>

        Next, run the following commands, which will install the
        required packages.

        <pre>
            <code id="pipCommands" class="language-shell" data-lang="bash" style="white-space: pre-line ">
                pip install --upgrade pip
                pip install wheel
                pip install setuptools
                pip install numpy
                pip install matplotlib
                pip install notebook
                pip install pandas
                pip install PyQt5
                pip install seaborn
                pip install sklearn
                pip install nbgrader
                jupyter nbextension install --sys-prefix --py nbgrader
                jupyter nbextension enable --user validate_assignment/main --section=notebook
                jupyter serverextension enable --user nbgrader.server_extensions.validate_assignment
            </code>
        </pre>
        <!-- </div> -->
    </div>

    <h4>Install the PyCharm IDE</h4>
    <div style="padding-left:2em;">
        <a href="https://www.jetbrains.com/pycharm/">PyCharm</a> provides a nice language aware editor, a
        <a href="https://en.wikipedia.org/wiki/Lint_(software)">linter</a> (something that checks
        your syntax as you type), and a nice debugger.  Other IDE's
        that are popular are <a href="https://www.spyder-ide.org/">Spyder</a> (especially
        popular with computational biologists), and <a href="https://code.visualstudio.com/">MS Visual Code</a>.


        This procedure focuses on PyCharm.  To obtain a copy of PyCharm and install it, follow these steps:
        <ol>
            <li> Register for a free version of PyCharm professional.  Visit
                <a href="https://www.jetbrains.com/student/">
                    https://www.jetbrains.com/student/</a>.  Typically it takes less than
                5 minutes for a license to get approved.
            </li>

            <li>After being approved, create your JetBrains account.  You will need this to register your copy of PyCharm.
            </li>
            <li> Download the <b>PROFESSIONAL</b> version of pycharm from
                <a href="https://www.jetbrains.com/pycharm/download">
                    https://www.jetbrains.com/pycharm/download</a>.
                At the welcome screen,  select <i>activate new license with: JetBrains
                    account</i>
            </li>
        </ol>

        When first starting PyCharm, you will need to pick an interpreter.  Make sure to pick
        the virtual environment ($HOME/cs444_venv).  The image below shows where I changed
        the location and selected to use an existing interpreter
        (the image says cs445 since I borrowed it from my machine learning class).

        <img src="ubuntu_pycharm_newproject_dialog.png" class="rounded mx-auto" style="display: block;">


        You can also control where you project
        files will be kept.  I would strongly recommend storing these files where they will
        be routinely backed up.  When I use a VM, I setup a mount point/directory from
        my Mac (which gets backed up).  I would also recommend using
        GIT (since it will provide another layer of safety and utility).
    </div>

</div>
