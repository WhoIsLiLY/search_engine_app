<?php
$keyword = $_POST['keyword'];
$output = shell_exec("python x_crawler.py $keyword");

echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
echo "<h1>RAW</h1>";
echo "<pre>$output</pre>";

$results = json_decode($output, true);
echo "<br><br><h1>Array Mode</h1>";
echo "<pre>";
print_r($results);
echo "</pre>";
// Cek apakah decoding berhasil
if ($results === null && json_last_error() !== JSON_ERROR_NONE) {
	echo "<b>Error decoding JSON:</b> " . json_last_error_msg();
	exit;
}

echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";

if (!empty($results)) {
	echo "<h3>Results:</h3>";
	foreach ($results as $result) {
		echo "<pre>";
		echo "Original Text: " . htmlspecialchars($result['Original Text'], ENT_QUOTES, 'UTF-8') . "\n";
		echo "Preprocessed Text: " . htmlspecialchars($result['Preprocessed Text'], ENT_QUOTES, 'UTF-8') . "\n";
		echo "Similarity: " . htmlspecialchars($result['Similarity'], ENT_QUOTES, 'UTF-8') . "\n";
		echo "</pre>";
		echo "<hr>";
	}
} else {
	echo "No results found or an error occurred.";
}
