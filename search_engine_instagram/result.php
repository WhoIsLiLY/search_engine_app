<?php
	$keyword = $_POST['keyword'];
	$output = shell_exec("python instagram_crawler.py $keyword");

	echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
	echo "<pre>$output</pre>"; 
?>