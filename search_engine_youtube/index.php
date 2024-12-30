<?php

require_once __DIR__ . '../../vendor/autoload.php';

// Load file .env
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . "/..");
$dotenv->load();

// API Key YouTube
$apiKey = $_ENV['API_KEY'];

// Keyword pencarian
$keyword = "Terima kasih pak Jokowi"; // Ganti dengan keyword yang diinginkan

// URL untuk pencarian video berdasarkan keyword
$searchUrl = "https://www.googleapis.com/youtube/v3/search?key={$apiKey}&q=" . urlencode($keyword) . "&part=snippet&type=video&maxResults=10";

function fetchYouTubeData($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        echo "cURL Error: " . curl_error($ch);
    }
    curl_close($ch);
    return json_decode($response, true);
}

// Ambil video berdasarkan keyword
$searchResults = fetchYouTubeData($searchUrl);

if (!empty($searchResults['items'])) {
    foreach ($searchResults['items'] as $item) {
        $videoId = $item['id']['videoId'];
        $title = $item['snippet']['title'];
        $channelId = $item['snippet']['channelId'];
        $channelTitle = $item['snippet']['channelTitle'];

        echo "Video Title: $title<br>";
        echo "Channel: $channelTitle<br>";

        // Ambil detail video untuk deskripsi
        $videoDetailUrl = "https://www.googleapis.com/youtube/v3/videos?key={$apiKey}&id={$videoId}&part=snippet";
        $videoDetails = fetchYouTubeData($videoDetailUrl);

        if (!empty($videoDetails['items'])) {
            $description = $videoDetails['items'][0]['snippet']['description'];
            echo "Description: $description<br>";
        }

        // Ambil komentar utama
        $commentsUrl = "https://www.googleapis.com/youtube/v3/commentThreads?key={$apiKey}&videoId={$videoId}&part=snippet&maxResults=5";
        $comments = fetchYouTubeData($commentsUrl);

        echo "Comments:<br>";
        if (!empty($comments['items'])) {
            foreach ($comments['items'] as $comment) {
                $commentText = $comment['snippet']['topLevelComment']['snippet']['textDisplay'];
                echo "- $commentText<br>";
            }
        } else {
            echo "No comments found.<br>";
        }

        echo "=============================<br>";
    }
} else {
    echo "No videos found for the keyword '{$keyword}'.<br>";
}
?>
