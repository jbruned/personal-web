<?php

$http_code = $_SERVER['REDIRECT_STATUS'];
$HTTP_CODES = [
	100 => 'Continue',
	101 => 'Switching Protocols',
	200 => 'OK',
	201 => 'Created',
	202 => 'Accepted',
	203 => 'Non-Authoritative Information',
	204 => 'No Content',
	205 => 'Reset Content',
	206 => 'Partial Content',
	300 => 'Multiple Choices',
	301 => 'Moved Permanently',
	302 => 'Found',
	303 => 'See Other',
	304 => 'Not Modified',
	305 => 'Use Proxy',
	307 => 'Temporary Redirect',
	400 => 'Bad Request',
	401 => 'Unauthorized',
	402 => 'Payment Required',
	403 => 'Forbidden',
	404 => 'Not Found',
	405 => 'Method Not Allowed',
	406 => 'Not Acceptable',
	407 => 'Proxy Authentication Required',
	408 => 'Request Time-out',
	409 => 'Conflict',
	410 => 'Gone',
	411 => 'Length Required',
	412 => 'Precondition Failed',
	413 => 'Request Entity Too Large',
	414 => 'Request-URI Too Large',
	415 => 'Unsupported Media Type',
	416 => 'Requested Range Not Satisfiable',
	417 => 'Expectation Failed',
	418 => "I'm a Teapot",
	500 => 'Internal Server Error',
	501 => 'Not Implemented',
	502 => 'Bad Gateway',
	503 => 'Service Unavailable',
	504 => 'Gateway Time-out',
	505 => 'HTTP Version Not Supported',
];

$error_code = empty($http_code) or !array_key_exists($http_code, $HTTP_CODES) ? '' : ' ' . $http_code;
$http_msg = $HTTP_CODES[$http_code] ?? 'Unexpected error';
$error_msg = empty($http_code) ? 'n unexpected' : ' <i>' . $HTTP_CODES[$http_code] . '</i> HTTP';

header($_SERVER['SERVER_PROTOCOL'] . ' ' . $HTTP_CODES[$http_code]);

?><html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title><?= $http_msg ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
</head>

<body class="bg-light">
    <main class="container position-absolute top-50 start-50 translate-middle text-center p-2 pb-5" style="max-width: 444px">
        <h1 class="d-inline"><i class="bi bi-exclamation-triangle-fill me-3"></i>Error<?= $error_code ?></h1>
        <p class="lead">Oops! Something went wrong</p>
        <p>While fetching the requested URL, a<?= $error_msg ?> error occurred. Sorry!</p>
    </main>
    <p class="position-absolute w-100 bottom-0 text-center text-muted pb-2">
        <a href="https://jorgebruned.com" class="text-muted">Jorge Bruned</a>
    </p>
</body>

</html>
