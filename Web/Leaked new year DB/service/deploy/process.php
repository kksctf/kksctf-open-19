<?php
libxml_disable_entity_loader (false);
stream_wrapper_unregister (file);
stream_wrapper_unregister (ftp);
stream_wrapper_unregister (data);
stream_wrapper_unregister (zlib);
stream_wrapper_unregister (glob);
stream_wrapper_unregister (phar);
stream_wrapper_unregister (ssh2);
stream_wrapper_unregister (rar);
stream_wrapper_unregister (ogg);
stream_wrapper_unregister (expect);
$xmlfile = file_get_contents('php://input');
if (preg_match('/<email><\/email>/', $xmlfile)){
    echo "we have not blank email:)";
} else {
    $dom = new DOMDocument();
    $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
    $info = simplexml_import_dom($dom);
    $email = $info->email;
    echo "entry for $email is found";
}
?>
