<?php

$cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=";

$cookie_decoded = base64_decode($cookie);

echo $cookie_decoded;

echo "\n\n";



$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");


$plain = json_encode($defaultdata);


echo $plain;
echo "\n\n";



function xorOperation($a, $b) {
    // Perform XOR operation and return the result
    // Iterate through each character
    $outText = '';
    for($i=0;$i<strlen($a);$i++) {
        $outText .= $a[$i] ^ $b[$i % strlen($b)];
        }
    
    return $outText;
}



$result = xorOperation($plain, $cookie_decoded);

echo $result;
echo "\n\n";



$key = "eDWo";
$keyrepeated = "eDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoe";




$hackeddata = array("showpassword"=>"yes", "bgcolor"=>"#ffffff");


$hackedjson = json_encode($hackeddata);


$hackedencrypted = base64_encode(xorOperation($hackedjson, $key));


echo $hackedencrypted;


?>
