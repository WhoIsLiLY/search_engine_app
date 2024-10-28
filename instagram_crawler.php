<?php
require_once __DIR__ . '/vendor/autoload.php';
include_once('simple_html_dom.php');

use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;
use Phpml\FeatureExtraction\TfIdfTransformer;

// INSTAGRAM ===========================================================================================
$html = file_get_html("https://www.instagram.com/results?search_query=".$_POST['keyword']);

echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
$i = 0;
$data_crawling = array();
$sample_data = array();
foreach ($html->find('ytd-video-renderer[class="style-scope ytd-item-section-renderer"]') as $video) {
	if ($i > 9) break;
	else {
		$newsTitle = $news->find('h4[class="wSpec-title"]', 0)->innertext;
		$newsLink = $news->find('a', 0)->href;
		$sendTitle = str_replace(" ", "#", $newsTitle);
		$stopTitle = shell_exec("python preprocessing.py $sendTitle");

		array_push($data_crawling, array($newsTitle, $newsLink, $stopTitle, 'similarity' => 0.0));
		array_push($sample_data, $stopTitle);
	}
	$i++;
}
array_push($sample_data, $_POST['keyword']);

echo "<pre>";
print_r($sample_data);
echo "</pre>";
$tf = new TokenCountVectorizer(new WhitespaceTokenizer());
$tf->fit($sample_data);
$tf->transform($sample_data);
// echo "<pre>";
// print_r($sample_data);
// echo "</pre>";				
$tfidf = new TfIdfTransformer($sample_data);
$tfidf->transform($sample_data);
echo "<pre>";
print_r($sample_data);
echo "</pre>";
$total = count($sample_data);


// similarity calculation

// send displayed data
$columns = array_column($data_crawling, 'similarity');
array_multisort($columns, SORT_ASC, $data_crawling);
echo "<b>Search Results</b><br><br>";
echo "<table border='1'>";
echo "<tr>";
echo "<th align='center'>Title</th>";
echo "<th align='center'>Link</th>";
echo "<th align='center'>Preprocessing Result</th>";
echo "<th align='center'>Similarity</th>";
echo "</tr>";
foreach ($data_crawling as $row) {
	echo "<tr>";
	echo "<td>" . $row[0] . "</td>";
	echo "<td>" . $row[1] . "</td>";
	echo "<td>" . $row[2] . "</td>";
	echo "<td>" . $row["similarity"] . "</td>";
	echo "</tr>";
}
echo '</table>';
