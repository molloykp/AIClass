<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>

  <?php
    include "/data/www/molloykp/CommonVariables.php";
    include $commonHeader;
  ?>
  <meta name="description" content="JMU CS445 Machine Learning">
  <title>CS 444 - Artificial Intelligence</title>
</head>


<body>

<?php include  $pageBodyHeaderBootS; ?>
<style>
    h2, h3, h4, h5, h6, , .h2, .h3, .h4, .h5, .h6 {
                              padding-top: 1 rem;
                              margin-bottom: 1rem;
                          }
</style>

<div class="container-fluid">
  <div class="row flex-xl-nowrap">
   <!-- <?php include "cs444_sidebar.php"; ?> -->
    
    <main class="col-12 col-md-10 col-xl-10 py-md-3 pl-md-5 bd-content" role="main">

        <div class="jumbotron">
            <div class="row">
                <div class="col-md-12 align-middle text-center">
                        <h2>CS 444 Artificial Intelligence</h2>
                </div>
            </div>
        </div> <!-- jumbotron -->


	 <?php 
        $paNumber = (int)$_GET["paNumber"];
        if ($weekParm >= 0 and $weekParm <=20) {
		    $formattedPA = sprintf("%02d",$paNumber);
            include "PA_" . $formattedPA . "/PA_". $formattedPA . ".html";
        }
      ?>

    </main>
  </div>  <!-- content -->
</div> <!-- wrapper -->

</body>

</html>
