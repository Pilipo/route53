<?php
require 'vendor/autoload.php';
use Mailgun\Mailgun;

$dotenv = new Dotenv\Dotenv(__DIR__);
$dotenv->load();

// $mg = new Mailgun(getenv('MAILGUNKEY'));
$mg = Mailgun::create(getenv('MAILGUNKEY'));
$domain = getenv('DOMAIN');

if (php_sapi_name() !== 'cli') {
  die;
}

if (empty($argv[1])) {
  echo "ERROR: At least one parameter is required.\n";
  die;
}

$mg->messages()->send($domain, [
  'from'=>getenv('EMAIL_FROM'),
  'to'=>getenv('EMAIL_TO'),
  'subject'=>"Route53 Updated " . (empty($argv[2]) ? "" : $argv[2]),
  'text'=>$argv[1]
]);
?>
