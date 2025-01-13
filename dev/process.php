<?php
$keyword = "ppn 12";

// Jalankan tiga crawler Python secara terpisah
$output_instagram = shell_exec("python instagram_crawler.py $keyword");
// $output_x = shell_exec("python x_crawler.py $keyword");
// $output_youtube = shell_exec("python youtube_crawler.py $keyword");

// Decode hasil output masing-masing crawler
$results_instagram = json_decode($output_instagram, true);
// $results_x = json_decode($output_x, true);
// $results_youtube = json_decode($output_youtube, true);
print_r($results_instagram);
// print_r($results_youtube);

// // Gabungkan ketiga hasil crawler ke dalam satu array
// $final_results = array(
//     'instagram' => $results_instagram,
//     'x' => $results_x,
//     'youtube' => $results_youtube
// );

// // Mengatur header agar respons dikirim sebagai JSON
// header('Content-Type: application/json');

// // Kirimkan hasil dalam format JSON
// echo json_encode($final_results);
?>