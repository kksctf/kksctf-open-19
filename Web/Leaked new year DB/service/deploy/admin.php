<?php
$allowedip = '127.0.0.1';
if (!($_SERVER['REMOTE_ADDR'] == $allowedip || strpos($_SERVER["REMOTE_ADDR"], "192.168") !== false)) {
    echo "here is restricted area, only for internal web users";
    echo $_SERVER['REMOTE_ADDR'];
    exit();
} else {


    $sqlite = new SQLite3('/db/test.db');
    $sqlite->enableExceptions(true);
    $otp = '43185748513597135109358413758436513856153178a5136713651357650815983470293480';
    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        if (isset($_GET['username'], $_GET['password'], $_GET['otp'])) {

            $a = $_GET['username'];
            $b = $_GET['password'];
            $c = $_GET['otp'];
            if (strcmp($c, $otp) == 0) {
                $result = $sqlite->query("SELECT * FROM Users WHERE login = '$a' AND password = '$b'");
                $row = $result->fetchArray();
                $count = count($row);
                if ($count === 1) {
                    echo "no such a user";
                    die();
                } else {
                    echo "exists";
                    die();
                }
            } else {
                echo "bad OTP";
                die();
            }
        }
    }
}
?>



<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>ADMIN AREA</title>

</head>

<body>

    <a><?php // 
    ?></a>



    <form action="" method="get">
        <label>UserName :</label><input type="text" name="username" /><br /><br />
        <label>Password :</label><input type="password" name="password" /><br /><br />
        <label>otp :</label><input type="otp" name="otp" /><br /><br />
        <input type="submit" value=" Submit " /><br />
    </form>
</body>

</html>
