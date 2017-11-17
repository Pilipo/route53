<?php
require __DIR__ . '/vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

$dotenv = new Dotenv\Dotenv(__DIR__);
$dotenv->load();

if (php_sapi_name() !== 'cli') {
    die;
}

if (empty($argv[1])) {
    echo "ERROR: At least one parameter is required.\n";
    die;
}

if (empty($argv[2])) {
    sendmail($argv[1]);
}
else {
    sendmail($argv[1], $argv[2]);    
}


function sendMail($message, $title='') {
    $mail = new PHPMailer(true);

    //Setup
    //$mail->SMTPDebug = 2;                                 // Enable verbose debug output
    $mail->isSMTP();                                      // Set mailer to use SMTP
    $mail->Host = 'smtp.gmail.com';                       // Specify main and backup SMTP servers
    $mail->SMTPAuth = true;                               // Enable SMTP authentication
    $mail->Username = getenv('EMAIL_USER');               // SMTP username
    $mail->Password = getenv('EMAIL_PASS');               // SMTP password
    $mail->SMTPSecure = 'tls';                            // Enable TLS encryption, `ssl` also accepted
    $mail->Port = 587;                                    // TCP port to connect to

    //Recipients
    $mail->setFrom(getenv('EMAIL_USER'), 'server-name');
    $mail->addAddress(getenv('EMAIL_TO'), 'recipient name');     // Add a recipient

    //Content
    $mail->isHTML(true);                                  // Set email format to HTML
    $mail->Subject = 'Message from ' . gethostname();
    if (!empty($title)) {
        $mail->Subject .= ' regarding ' . $title;
    }
    $mail->Body    = '<p>This is more detail:</p>';
    $mail->Body     .= '<p>' . $message . '</p>';
    $mail->AltBody = $message;

    //Send it!
    return $mail->send();
}
?>