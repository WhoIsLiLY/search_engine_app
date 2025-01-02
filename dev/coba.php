<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KEPO</title>
    <link href="/public/css/output.css" rel="stylesheet">
</head>
<body>
<div class="relative mb-4">
            <div class="inline-block px-3 py-1 rounded-full text-sm font-semibold shadow-md bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 text-white">
                instagram
            </div>
        </div>
        <h2 class="font-bold text-lg">Original Text:</h2>
        <p class="text-gray-700">${item.text}</p>
        <h2 class="font-bold text-lg mt-2">Preprocessed Text:</h2>
        <p class="text-gray-500">${item.preprocessed}</p>
        <div class="mt-4">
            <span class="font-bold text-sm">Similarity:</span>
            <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="h-4 rounded-full" style="width: ${item.similarity}%; background-color: ${getColor(item.similarity)};"></div>
            </div>
            <span class="text-sm text-gray-600">${item.similarity}%</span>
        </div>
</body>
</html>