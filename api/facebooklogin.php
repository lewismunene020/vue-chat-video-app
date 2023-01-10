<?php
// Include the autoloader provided by Facebook SDK
require_once __DIR__ . '/facebook-sdk/autoload.php';

// Start a session
session_start();

// Create a new Facebook app instance
$fb = new Facebook\Facebook([
  'app_id' => '{your-app-id}',
  'app_secret' => '{your-app-secret}',
  'default_graph_version' => 'v5.0',
]);

// Create a login helper instance
$helper = $fb->getRedirectLoginHelper();

// Get the access token
try {
  $accessToken = $helper->getAccessToken();
} catch(Facebook\Exceptions\FacebookResponseException $e) {
  // When Graph returns an error
  echo 'Graph returned an error: ' . $e->getMessage();
  exit;
} catch(Facebook\Exceptions\FacebookSDKException $e) {
  // When validation fails or other local issues
  echo 'Facebook SDK returned an error: ' . $e->getMessage();
  exit;
}

if (!isset($accessToken)) {
    // Redirect the user to the login URL
    $loginUrl = $helper->getLoginUrl("http://{your-website-url}/login/facebook");
    header("Location: " . $loginUrl);
    exit;
}

// Get the user's profile information
$response = $fb->get('/me?fields=id,name,email', $accessToken);
$user = $response->getGraphUser();

// Send the user's information to Stream Video
$data = array(
    'id' => $user['id'],
    'name' => $user['name'],
    'email' => $user['email']
);
$options = array(
    'http' => array(
        'method'  => 'POST',
        'content' => json_encode( $data ),
        'header'=>  "Content-Type: application/json\r\n" .
                    "Accept: application/json\r\n"
    )
);

$stream_video_url = "http://{stream-video-url}/users";
$context  = stream_context_create( $options );
$result = file_get_contents( $stream_video_url, false, $context );
$response = json_decode( $result );

// Store the user's ID in the session
$_SESSION['user_id'] = $user['id'];

// Redirect the user to the home page
header("Location: http://{your-website-url}");
exit;

