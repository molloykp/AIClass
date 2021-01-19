<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>

    <?php
    include "/data/www/molloykp/CommonVariables.php";
    include $commonHeader;
    ?>
    <meta name="description" content="JMU CS444 AI">
    <title>CS 444 - AI - Spr 2021</title>
</head>

<body>

<?php include  $pageBodyHeaderBootS; ?>
<div class="container-fluid">
    <div class="row flex-xl-nowrap">
        <?php include "../cs444_sidebar.php"; ?>

        <main class="col-12 col-md-10 col-xl-10 py-md-3 pl-md-5 bd-content" role="main">


            <div class="jumbotron">
                <div class="row">
                    <div class="col-md-12 align-middle text-center">
                        <h2>CS 444 Artificial Intelligence</h2>
                        <h2>Spring 2021</h2>
                    </div>
                </div>
            </div> <!-- jumbotron -->

            <h3> Installing an Ubuntu/Mint Virtual Machine with VirtualBox  </h3>

            A virtual machine image is maintained by JMU's Unix User Group (UUG).
            This set of instructions starts with that image and suggests
            a few customizations for CS 444.


            <h4>Install Virtual Box and the Virtual Machine Image </h4>
            <div style="padding-left:2em;">
                <ol>
                    <li> Download and install the VirtualBox software for your platform
                        from <a href="https://www.virtualbox.org">https://www.virtualbox.org</a>
                    </li>

                    <li> Download the virtual machine image from the JMU's (UUG) site:
                        <a href="https://w3.cs.jmu.edu/uug/">https://w3.cs.jmu.edu/uug/</a>.
                        The file you want is normally named <i>image-XXYYa.ova</i>, where XX is the semester that the image was created (<i>sp</i>} for Spring, <i>fa</i> for Fall)  and YY is the 2 digit year.  This file is rather large (1.8 GB).
                    </li>
                    <li> Start VirtualBox </li>
                    <li>Select <i>File</i>, then <i>Import Appliance...</i>, then select
                        the file you downloaded (<i>image-XXYYa.ova</i> ) and click on
                        <b>import</b> to create the machine
                    </li>

                    <li> Start the machine by double clicking on the name (JMU Linux Mint XXYY) on the left side of your VirtualBox window </li>
                </ol>

                You will then need  to proceed through the Linux OS configuration screens.
                <ol>
                    <li>Select <i>English</i> and then continue
                    </li>
                    <li>Take the default keyboard (English (US) and press <i>Continue</i>
                    </li>
                    <li> Take <i>New York</i> as the default timezone, and press <i>Continue</i>
                    </li>
                    <li>Select your name (use <b>your e-id</b>.  For example,
                        I used <b>molloykp</b>).  This will auto populate the next 3 fields.
                    </li>
                    <li> Select a password and then press  <i>Continue</i>
                    </li>
                </ol>


                The system will then execute a few configuration scripts (this
                took about 2 minutes on my laptop). At the conclusion
                of this process, I will able to login to the virtual machine
                using my username and password.


                <!--
                \begin{figure}[h]
                \includegraphics[scale=0.2]{ScreenShotDevicesSelection.png}
                \caption{Selecting the device menu from the VirtualBox app.}
                \label{fig:deviceMenu}
                \end{figure}
                -->
            </div>


            <h4>Install Guest Additions and Configurations</h4>
            <div style="padding-left:2em;">

                To allow your VM to run more smoothly, install the <i>Guest Additions</i>.
                <ol>
                    <li>Start your VM and log in
                    </li>

                    <li>Click on the <b>devices </b> menu in your OS (not within the VM,
                        see Figure fig:deviceMenu and
                        select <b> Insert Guest Additions CD image...</b>
                    </li>

                    <li>The system will then prompt you to run the image, click <b> Run</b>.
                        Enter your VM password when prompted.
                    </li>

                    <li>When completed, you will get a <i>Press Return to close this window...</i>,
                        so press return.
                    </li>

                    <li> Restart your VM.
                    </li>
                </ol>

                Some releases of VirtualBox seem to set the display scaling to 200\%.
                To check this setting, go to the <i>VirtualVM</i> menu, <i>Preferences</i>,
                then click on the <i>Display</i> icon.
                Check the <i>scale factor</i> setting and adjust to your preference.  I
                set mine to 100%.
            </div>

            <h4>Configuring CPU and Memory</h4>
            <div style="padding-left:2em;">

                Training machine learning models can be a computationally expensive task.
                Fortunately, a lot of tools kits utilize approaches that employ
                parallel computation utilizing multiple CPU cores and graphic proceessing units (GPUs).
                Visualizing ML models can also be expensive.

                You can increase the amount of CPU core's and video memory available to your
                virtual machine.
                <ul>

                    <li>On the VirtualBox home screen, select your virtual machine
                        and then click the yellow gear button for settings.</li>
                    <li>The click the system button and select processor (as
                    shown in the image below). Increase the CPUs/cores.</li>
                    <li>Click on display, and increase video memory to its
                    maximum settings (128 MB) and make sure that
                    <i>Enable 3D acceleration</i> is checked.  An example
                    of this configuration is shown below (right).  </li>
                </ul>

                <div class="row">
                    <div class="col-sm-6">
                        <img src="VirtualBoxCPUConfig.png" width="500" alt="CPU Config">
                    </div>
                    <div class="col-sm-6">
                        <img src="VirtualBoxVideoMemoryConfig.png" width="500" alt="Video Memory Config">
                    </div>
                </div>
            </div>
        </main>
    </div>  <!-- content -->
</div> <!-- wrapper -->

</body>

</html>
