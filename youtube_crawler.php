<?php
require_once __DIR__ . '/vendor/autoload.php';
include_once('simple_html_dom.php');

use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;
use Phpml\FeatureExtraction\TfIdfTransformer;

// YOUTUBE ===========================================================================================
$keyword = urlencode($_POST['keyword']);
$html = file_get_html("https://www.youtube.com/results?search_query=" . $keyword);
echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
$i = 0;
$data_crawling = array();
$sample_data = array();
foreach ($html->find('a#video-title') as $video) {
    if ($i >= 10) break;
    else {
        // $videoTitle = $video->innertext;
        // $videoLink = 'https://www.youtube.com' . $video->href;
        // $sendTitle = str_replace(" ", "#", $videoTitle);
        // $stopTitle = shell_exec("python preprocessing.py $sendTitle");

        // array_push($data_crawling, array($videoTitle, $videoLink, $stopTitle, 'similarity' => 0.0));
        // array_push($sample_data, $stopTitle);

        echo "data ke " . $i . "<br>";
        // echo "Title: " . $videoTitle . "<br>";
        // echo "Link: " . $videoLink . "<br>";
    }
    $i++;
}
// array_push($sample_data, $_POST['keyword']);

// echo "<pre>";
// print_r($sample_data);
// echo "</pre>";
// $tf = new TokenCountVectorizer(new WhitespaceTokenizer());
// $tf->fit($sample_data);
// $tf->transform($sample_data);
// // echo "<pre>";
// // print_r($sample_data);
// // echo "</pre>";				
// $tfidf = new TfIdfTransformer($sample_data);
// $tfidf->transform($sample_data);
// echo "<pre>";
// print_r($sample_data);
// echo "</pre>";
// $total = count($sample_data);


// // similarity calculation

// // send displayed data
// $columns = array_column($data_crawling, 'similarity');
// array_multisort($columns, SORT_ASC, $data_crawling);
// echo "<b>Search Results</b><br><br>";
// echo "<table border='1'>";
// echo "<tr>";
// echo "<th align='center'>Title</th>";
// echo "<th align='center'>Link</th>";
// echo "<th align='center'>Preprocessing Result</th>";
// echo "<th align='center'>Similarity</th>";
// echo "</tr>";
// foreach ($data_crawling as $row) {
// 	echo "<tr>";
// 	echo "<td>" . $row[0] . "</td>";
// 	echo "<td>" . $row[1] . "</td>";
// 	echo "<td>" . $row[2] . "</td>";
// 	echo "<td>" . $row["similarity"] . "</td>";
// 	echo "</tr>";
// }
// echo '</table>';
