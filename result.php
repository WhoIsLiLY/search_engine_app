<?php
	// require_once __DIR__ . "/youtube_crawler.php";
	// require_once __DIR__ . "/instagram_crawler.php";

	$output = shell_exec('python youtube_crawler.py');

	echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
	echo "<pre>$output</pre>"; 
?>