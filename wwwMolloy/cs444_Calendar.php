<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>

    <?php
    include "/data/www/molloykp/CommonVariables.php";
    include $commonHeader;
    ?>
    <meta name="description" content="JMU CS444 AI">
    <title>CS 444 - AI Sp2021</title>
</head>


<body>

<?php include  $pageBodyHeaderBootS; ?>
<div class="container-fluid">
    <div class="row flex-xl-nowrap">
        <?php include "cs444_sidebar.php"; ?>

        <main class="col-12 col-md-10 col-xl-10 py-md-3 pl-md-5 bd-content" role="main">


            <div class="jumbotron">
                <div class="row">
                    <div class="col-md-12 align-middle text-center">
                        <h2>CS 444 Artificial Intelligence</h2>
                        <h2>Spring 2021</h2>
                    </div>
                </div>
            </div> <!-- jumbotron -->

            <p>
                The general learning flow for this class is:
            <ul>
                <li> Attend class where we will interleave
                    lectures and labs.  This is where
                    we will introduce new concepts and
                    methods.
                </li>

                <li>Read the assigned reading <strong> AFTER </strong>
                    class/lecture.  These readings will reinforce the topics
                    from class.  Reading material marked with a "(S)" is supplemental
                    and is encourgaged, but will not be covered on the quizzes.
                </li>

                <li> Weekly quizzes will test you on the prior 2 days of lecture.
                </li>
            </ul>
            </p>
            <script type="text/javascript"
                    src="/molloykp/plugins/js/misc.js">
            </script>

            <script>
                var semesterStartDate= new Date(2021,00,18);
                dt = new Date()
                month = dt.getMonth();
                day = dt.getDate();
                year = dt.getFullYear();
                dt2 = new Date(year, month, day);
                wkd = diff_weeks(dt2,semesterStartDate) + 1
                if (semesterStartDate > dt) wkd = 1;

                document.write("<a href=\"#WeekRow_"+wkd+"_a\">Current Week</a>");

            </script>


            <table class="table  table-hover" border="0" cellpadding="0"
                   cellspacing="0" summary="6 column">

                <col style="width:04%">
                <col style="width:08%">
                <col style="width:26%">
                <col style="width:18%">
                <col style="width:25%">
                <col style="width:17%">
                <thead>
                <tr>
                    <td style="text-align: right"><strong>Week</strong></td>
                    <td style="text-align: left;"><strong>Date</strong></td>
                    <td><strong>Topic</strong></td>
                    <td style="text-align: left;"><strong>Readings</strong></td>
                    <td><strong>Assignment/Lab</strong></td>
                    <td style="text-align: left;"><strong>Due</strong></td>
                </tr>
                </thead>

                <tbody>

                
                <?php
                   include "cs444_Calendar_Data.php";
                ?>

                </tbody>
            </table>

            <script>
                // semesterStartDate declared in script block above

                dt = new Date();
                month = dt.getMonth();
                day = dt.getDate();
                year = dt.getFullYear();
                // dt2 has time truncated.
                dt2 = new Date(year, month, day);
                wkd = diff_weeks_r(semesterStartDate, dt2)
                if (wkd < 1) wkd = 1;

                var weekNo = $("td[id^='WeekNumber']").get();
                for (i = 0; i < weekNo.length; i++){
                    weekNo[i].innerHTML = i+1;
                }

                var weeks = $("tr[id^='WeekRow']").get();

                for (x = 0; x < weeks.length; x++) {
                    var weekNumA = weeks[x].id.split("_");
                    weekNum = parseInt(weekNumA[1],10);
                    if (weekNum >  wkd) {
                        weeks[x].style.opacity = "0.6";
                    }
                }
                addDatesForCalendar("WeekRow",semesterStartDate);
            </script>



        </main>
    </div>
</div>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>

<script>window.jQuery || document.write('<script src="/docs/4.3/assets/js/vendor/jquery-slim.min.js"><\/script>')</script>


</body>
</html>

