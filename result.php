<?php
	// require_once __DIR__ . "/youtube_crawler.php";
	// require_once __DIR__ . "/instagram_crawler.php";

	$keyword = $_POST['keyword'];
	$output = shell_exec("python youtube_crawler.py $keyword");

	echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
	echo "<pre>$output</pre>"; 
?>