<?php

$cookie = json_encode(array( "showpassword"=>"yes", "bgcolor"=>"#ffffff"));

function xor_encrypt($in) {
    $key = "eDWo";
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

// Decrypting the cookie
$decrypted_cookie = base64_encode(xor_encrypt(json_encode($cookie)));
echo $decrypted_cookie . "\n";

?>
