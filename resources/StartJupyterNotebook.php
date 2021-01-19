<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
    <?php
    include "/data/www/molloykp/CommonVariables.php";
    include $commonHeader;
    ?>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta name="description" content="JMU CS445 Machine Learning">
    <title>CS 445 - Machine Learning</title>
</head>


<body>


<?php include  $pageBodyHeaderBootS; ?>

<div class="container-fluid">
    <div class="row flex-xl-nowrap">
        <main class="col-12 col-md-10 col-xl-10 py-md-3 pl-md-5 bd-content" role="main">


            <div class="jumbotron">
                <div class="container">
                    <div class="row">
                        <div class="col-md align-middle text-center">
                            <h2>CS 445 -- Machine Learning</h2>
                        </div>
                    </div>
                </div>
            </div>

            <h3>Using Jupyter Notebooks</h3>
            <p>
                This class will utilize
                <a href="https://jupyter.org/">Jupyter notebooks</a> for
                many of our labs.  These notebooks utilize a web-based
                interactive environment where the learning material (text,
                images, etc) can be combined with Python code and data.
            </p>

            <p>
                This semester, some notebooks have been <i>enhanced</i>
                to use <a href="https://nbgrader.readthedocs.io/en/stable/">nbgrader</a>.
                This add-on provide many features, but the main one utilized in this
                setting is the <i>autograder</i>.  This is not really used to provide a grade,
                but rather, to provide a way that you can verify your results while
                perform the lab (i.e., are my answers correct, did I complete all the
                problems in the notebook).
            </p>

            <h3>Starting Jupyter Notebooks</h3>
            Follow these steps to utilize jupyter notebooks:
            <ol>
                <li>Place all lab files in a directory (recommend a separate directory
                    for each lab</li>
                <li>Open a command prompt/terminal and <b>cd</b> into this directory</li>

                <li>Make sure your python environment is set (have you sourced the
                activate script to setup the <i><b>venv</b></i>
                You can check this on Unix/Mac based systems usin (it should be using
                    the python in your <i>venv</i>).
                by typing <pre><code>which python</code></pre>
                </li>

                <li>To start the notebook, enter the
                    folllowing command and press enter.<pre><code>jupyter notebook</code></pre>.
                    <img src="jupyterNotebookStartSeq.png" width="800"></li>

                <li>A web browser should start and present the contents
                of the where <i>jupyter</i> was started.</li>

                <li>Click on the lab file that ends with <i>.ipynb</i>, it should open
                and present a screen similar to the following image.
                <img src="jupyterNotebookWithNBGrader2.png" width="800">
                </li>
                <li>You should now be ready to use the notebook.  Notice the
                <b>validate</b> button (cirled in red in the above image).  This is
                the <i>nbgrader</i> package.  You should click this button when you
                have completed a section of the notebook to help check your
                work.  Note that validate may report errors for sections that you
                have not completed</li>
                <li>To turn in your notebook, simply save your <i>.ipynb</i> file and
                upload it to Canvas.  Most labs will be group activities, so,
                please note your lab partner in the text submission area in Canvas (and
                use both first and last names).  </li>
            </ol>

            <h3>Jupyter Notebook Tutorials</h3>
            There are a lot of features packed into Jupyter notebooks.  Here are a few
            additional tutorials that I have glanced through and found helpful.
            <ul>
                <li><a href="https://medium.com/velotio-perspectives/the-ultimate-beginners-guide-to-jupyter-notebooks-6b00846ed2af">
                        Guide to Jupyter Notebooks</a></li>
                <li><a href="https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook">
                    Jupyter Tutorial</a>  This one is a little verbose but illustrates
                a lot of features, such as profiling code.</li>
            </ul>
        </main>
    </div>  <!-- content -->
</div> <!-- wrapper -->


</body>

</html>


