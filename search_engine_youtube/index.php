<?php
echo '<h2>SEARCHING DATA</h2>';
echo '<form action="result.php" method="POST">';
echo '<b>Keyword:</b> <input type="text" name="keyword" required><br><br>';
echo '<b>Similarity Method:</b> ';
echo '<input type="radio" name="method" value="Minkowski" checked/> Minkowski ';
echo '<input type="radio" name="method" value="Canberra"/> Canberra<br><br>';
echo '<input type="submit" name="crawl" value="Search">';
echo '</form>';
?>
