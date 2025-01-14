<?php
$keyword = $_POST["keyword"];
$platforms = $_POST["platforms"];

// Jalankan tiga crawler Python secara terpisah & Decode hasil output masing-masing crawler
$instagram = array_filter($platforms, function($value) {
    return strpos($value, 'instagram') !== false;
});
$x = array_filter($platforms, function($value) {
    return strpos($value, 'x') !== false;
});
$youtube = array_filter($platforms, function($value) {
    return strpos($value, 'youtube') !== false;
});

if(!empty($instagram)){
    $output_instagram = shell_exec("python instagram_crawler.py $keyword");
    $results_instagram = json_decode($output_instagram, true);
}else{
    $results_instagram = null;
}

if(!empty($x)){
    $output_x = shell_exec("python x_crawler.py $keyword");
    $results_x = json_decode($output_x, true);
}else{
    $results_x = null;
}

if(!empty($youtube)){
    $output_youtube = shell_exec("python youtube_crawler.py $keyword");
    $results_youtube = json_decode($output_youtube, true);
}else{
    $results_youtube = null;
}

// print_r($results_instagram);
// print_r($results_youtube);
// print_r($results_x)

// Gabungkan ketiga hasil crawler ke dalam satu array
$final_results = array(
    'instagram' => $results_instagram,
    'x' => $results_x,
    'youtube' => $results_youtube
);

// Mengatur header agar respons dikirim sebagai JSON
header('Content-Type: application/json');

// Kirimkan hasil dalam format JSON
echo json_encode($final_results);
?>