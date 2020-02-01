<?php
session_start();
create_image();

function create_image()
{
    // Generating Random Code
    $md5_hash = md5(rand(0,999));
    $captcha = $_SESSION['rand'];

    $width = 200;
    $height = 50;

    $image = ImageCreate($width,$height);

    // Colours
    $white = imagecolorallocate($image, 255, 255, 255);
    $black = imagecolorallocate($image, 0, 0, 0);
    $green = imagecolorallocate($image, 0, 255, 0);
    $brown = imagecolorallocate($image, 139, 69, 19);
    $orange = imagecolorallocate($image, 255, 69, 0);
    $grey = imagecolorallocate($image, 204, 204, 204);

    // Making Background
    imagefill($image, 0, 0, $black);

    // Carving Text into the image
    $font= "/code/font.ttf";
    imagettftext($image, 25, 10, 45, 45, $brown, $font, $captcha);

    // Informing Browser there is a jpeg image file is coming
    header("Content-Type: image/jpeg");

    //Converting Image into JPEG
    imagejpeg($image);
    // Clearing Cache
    imagedestroy($image);
}
