<?php
    session_start();
    $mess = "Approved! Use secret to create a link for next step! next Chain step secret is:";
    $part = "lacus,";
    if($_POST['s']){
        if (substr(md5($_POST['ch']), -4) === $_SESSION['rand']){
        ?>
        <script language="javascript"> 
        document.addEventListener("DOMContentLoaded", function(event) {
        var btn = document.getElementById("B");
        btn.hidden = true;   
        });
    </script>
        <?php
    echo "<br>".$mess."<br>";
    echo "<br>".$part."<br>";
    }
    }
    $valid = md5(rand());
    $rand = substr($valid, -4);
    $_SESSION['rand'] = $rand;
    ?>
    <div id="B">
    <br>gimmie a value whose MD5 ends with this 4 chars from captcha:<br> 
    <form action="" method="post">
    <table width="50%">
        <tr>
            <td>Cmon Human!</td>
            <br><img src="captcha.php" alt="Captcha Image"><br>
            <input name="hash" value="<?php echo md5($rand); ?>" type="hidden">
            <td><input type="text" name="ch"></td>
        </tr>
    </table>
        <input type="submit" value="OK" name="s">
    </form>
    </div>
    
