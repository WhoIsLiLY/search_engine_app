<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KEPO</title>
    <link href="/public/css/output.css" rel="stylesheet">
    <link href="/public/css/custom.css" rel="stylesheet">
</head>

<body class="bg-gray-100 text-gray-900">

    <!-- Header -->
    <header class="bg-blue-600 text-white py-4">
        <div class="container mx-auto flex justify-between items-center">
            <!-- <h1 class="text-2xl font-bold">KEPO.COM</h1> -->
            <div class="logo-container">
                <img src="/public/image/logo_ubaya.png" alt="Ubaya Logo" class="logo-ubaya">
                <img src="/public/image/logo_if.png" alt="IF Logo" class="logo-if">
            </div>
            <div class="button-container">
                <button type="submit" id="homeButton" class="homeButton">Home</button>
                <button type="submit" id="resultButton" class="resultButton">Result</button>
            </div>
        </div>
    </header>

    <!-- Form Input -->
    <div id="input" class="container mx-auto my-8">

        <!-- <form class="flex items-center max-w-sm mx-auto">
            <label for="simple-search" class="sr-only">Search</label>
            <div class="relative w-full">
                <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                    <svg class="w-4 h-4 text-gray-500 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 20">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5v10M3 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm12 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm0 0V6a3 3 0 0 0-3-3H9m1.5-2-2 2 2 2" />
                    </svg>
                </div>
                <input type="text" id="simple-search" class="bg-white-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search branch name..." required />
            </div>
            <button type="submit" class="p-2.5 ms-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                </svg>
                <span class="sr-only">Search</span>
            </button>
        </form> -->


        <form id="searchForm" class="space-y-4">
            <div class="search-container">
                <h1 class="search-tittle">KEPOIN</h1>
                <div class="search-bar">
                    <input type="text" name="keyword" id="keyword" placeholder="SEARCH..." class="search-input">
                    <button type="submit" id="searchButton" class="search-button">
                        <img src="/public/image/search_icon.png" alt="Search">
                    </button>
                </div>
                <div class="flex flex-col justify-center items-center">
                    <div class="flex space-x-6 mr-5 mt-4">
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="platform-youtube-start" value="youtube" class="platform-checkbox-start w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500" checked>
                            <span class="text-lg text-gray-700">YouTube</span>
                        </label>
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="platform-instagram-start" value="instagram" class="platform-checkbox-start w-5 h-5 text-pink-600 border-gray-300 rounded focus:ring-pink-500" checked>
                            <span class="text-lg text-gray-700">Instagram</span>
                        </label>
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="platform-x-start" value="x" class="platform-checkbox-start w-5 h-5 text-black border-gray-300 rounded focus:ring-gray-700" checked>
                            <span class="text-lg text-gray-700 mr-4">X</span>
                        </label>
                    </div>
                </div>
            </div>
        </form>

        <!-- <form id="searchForm" class="space-y-4">
            <div class="flex flex-col justify-center items-center">
                <h2 class="text-lg font-bold mb-4">SEARCHING DATA</h2>
                <input type="text" name="keyword" id="keyword" class="p-2 border border-gray-300 rounded-lg w-full" required>
                <button type="submit" id="searchButton" class="px-4 py-2 bg-blue-600 text-white rounded-lg">Search</button>
            </div>
        </form> -->
    </div>

    <!-- Form Result -->
    <div id="result" class="hidden">
        <div class="flex justify-start items-center pt-4">
            <!-- Checkboxes -->
            <div class="container mx-auto my-4">
                <div class="flex space-x-4 justify-end px-5">
                    <div class="flex items-center ps-4 border border-gray-200 rounded dark:border-gray-700">
                        <label for="bordered-radio-1" class="w-full py-4 ms-2 text-lg font-bold text-gray-900 dark:text-black-300 mr-4">Platform: </label>
                        <div class="flex space-x-6 mr-5">
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" id="platform-youtube" value="youtube" class="platform-checkbox w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500" checked>
                                <span class="text-lg text-gray-700">YouTube</span>
                            </label>
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" id="platform-instagram" value="instagram" class="platform-checkbox w-5 h-5 text-pink-600 border-gray-300 rounded focus:ring-pink-500" checked>
                                <span class="text-lg text-gray-700">Instagram</span>
                            </label>
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" id="platform-x" value="x" class="platform-checkbox w-5 h-5 text-black border-gray-300 rounded focus:ring-gray-700" checked>
                                <span class="text-lg text-gray-700 mr-4">X</span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Radio Buttons -->
            <div class="container mx-auto my-4">
                <div class="flex space-x-4 justify-start px-5">

                    <div class="flex items-center ps-4 border border-gray-200 rounded dark:border-gray-700">
                        <label for="bordered-radio-1" class="w-full py-4 ms-2 text-lg font-bold text-gray-900 dark:text-black-300 mr-4">Similarity: </label>

                        <div class="flex space-x-6 mr-5">
                            <label class="flex items-center space-x-2">
                                <input type="radio" id="similarity-asymetric" name="similarity" value="asymetric" class="w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500" checked>
                                <span class="text-lg text-gray-700">Asymmetric</span>
                            </label>
                            <label class="flex items-center space-x-2">
                                <input type="radio" id="similarity-cosine" name="similarity" value="cosine" class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                                <span class="text-lg text-gray-700">Cosine</span>
                            </label>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- Results Section -->
        <div class="container mx-auto my-8">
            <div id="results" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Filtered Cards will be injected here -->
            </div>
        </div>

        <!-- Results Section -->
        <div id="messageBoxAlert" class="hidden">
            <div class="container mx-auto my-8 flex justify-center items-center h-96">
                <div id="results" class="flex items-center justify-center p-6 border border-gray-300 rounded shadow-md dark:border-gray-700 bg-gray-50">
                    <h1 class="text-lg text-gray-600 text-center">
                        No result available. Please make sure you checked at least 1 of the checkboxes<br>
                        Or make sure your keyword valid
                    </h1>
                </div>
            </div>
        </div>


        <!-- Pagination -->
        <div id="page" class="container mx-auto text-center my-4">
            <button class="py-2 px-4 bg-gray-200 rounded-lg mr-2" onclick="prevPage()">Previous</button>
            <span id="currentPage" class="font-bold">1</span>
            <button class="py-2 px-4 bg-gray-200 rounded-lg ml-2" onclick="nextPage()">Next</button>
        </div>


    </div>

    <!-- Footer -->
    <footer class="text-white py-4 mt-8">
        <div class="container mx-auto text-center">
            <p>&copy; 2025 KEPOIN. All rights reserved.</p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        let data = {
            all: [],
            instagram: [],
            x: [],
            youtube: [],
            // instagram_x: [],
            // instagram_youtube: [],
            // x_youtube: []
        };
        $(document).ready(function() {
            $('#searchForm').on('submit', function(event) {
                event.preventDefault(); // Mencegah reload halaman

                const keyword = $('#keyword').val();
                const platforms = $('.platform-checkbox-start:checked').map((_, el) => el.value).get();

                if (!keyword) {
                    alert('Please enter a keyword!');
                    return;
                }

                // Ubah tombol ke state loading
                $('#searchButton').text('Searching...').prop('disabled', true).addClass('bg-gray-400 text-white');

                // Lakukan AJAX request
                $.ajax({
                    url: 'process.php', // Endpoint untuk memproses pencarian
                    type: 'POST',
                    data: {
                        keyword: keyword,
                        platforms: platforms,
                    },
                    dataType: 'json',
                    success: function(response) {
                        // Reset tombol ke state awal
                        $('#searchButton').text('Search').prop('disabled', false).removeClass('bg-gray-400');

                        // Sembunyikan form input
                        $('#input').addClass('hidden');

                        // Munculkan form result
                        $('#result').removeClass('hidden');

                        console.log(response);
                        // Proses data dan masukkan ke dalam variabel `data`
                        data = {
                            instagram: response.instagram,
                            x: response.x,
                            youtube: response.youtube,
                        };
                        Object.keys(data).forEach(key => {
                            if (data[key] === null) {
                                delete data[key];
                            }
                        });
                        console.log(data);
                        displayCards();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        //console.error('Error:', errorThrown);
                        if (jqXHR.responseText) {
                            console.error(jqXHR.responseText);
                        }
                        // Display error message to the user
                        alert(JSON.parse(jqXHR.responseText).message);
                        // Tangani respons error
                        var errorMessage = jqXHR.status + ': ' + jqXHR.statusText;
                        console.error('Error:', errorMessage);

                        // Jika ingin menampilkan pesan kesalahan yang dikirim oleh server (jika ada)
                        if (jqXHR.responseText) {
                            console.error('Server Error:', jqXHR.responseText);
                        }
                    },
                });
            });
        });
        // // Dummy data
        // const data = {
        //     all: Array.from({
        //         length: 20
        //     }, (_, i) => {
        //         const sources = ['Youtube', 'Instagram', 'X']; // Array sumber
        //         const randomSource = sources[Math.floor(Math.random() * sources.length)]; // Pilih sumber secara acak

        //         return {
        //             source: randomSource, // Sumber acak
        //             text: `All post ${i + 1}`,
        //             preprocessed: `Preprocessed text ${i + 1}`,
        //             similarity: Math.floor(Math.random() * 100) + 1, // Random similarity
        //         };
        //     }),
        //     instagram: Array.from({
        //         length: 15
        //     }, (_, i) => ({
        //         source: `Instagram`,
        //         text: `Instagram post ${i + 1}`,
        //         preprocessed: `Preprocessed text ${i + 1}     Lorem ipsum dolor sit amet consectetur adipisicing elit. Adipisci corrupti molestias aliquid ut perferendis quisquam mollitia architecto quod atque, ad, nobis nostrum ullam tenetur laborum impedit suscipit expedita eveniet deleniti!
        // `,
        //         similarity: Math.floor(Math.random() * 100) + 1,
        //     })),
        //     x: Array.from({
        //         length: 12
        //     }, (_, i) => ({
        //         source: `X`,
        //         text: `X post ${i + 1}`,
        //         preprocessed: `Preprocessed text ${i + 1}`,
        //         similarity: Math.floor(Math.random() * 100) + 1,
        //     })),
        //     youtube: Array.from({
        //         length: 20
        //     }, (_, i) => ({
        //         source: `Youtube`,
        //         text: `YouTube post ${i + 1}`,
        //         preprocessed: `Preprocessed text ${i + 1}`,
        //         similarity: Math.floor(Math.random() * 100) + 1,
        //     })),
        // };

        let currentPage = 1;
        const itemsPerPage = 6;
        let selectedSimilarity = 'cosine';

        // Tambahkan event listener menggunakan jQuery
        $('input[name="similarity"]').on('change', function() {
            selectedSimilarity = $(this).val(); // Update nilai similarity yang dipilih
            displayCards(); // Panggil ulang fungsi displayCards untuk memperbarui tampilan
        });

        // $(document).ready(function() {
        //     // Event handler untuk setiap perubahan pada checkbox platform
        //     $('.platform-checkbox').on('change', function() {
        //         // Cek apakah semua checkbox tidak dicentang
        //         if ($('.platform-checkbox:checked').length === 0) {
        //             // Munculkan form result
        //             $('#messageBoxAlert').removeClass('hidden');
        //         } else {
        //             // Sembunyikan form input
        //             $('#messageBoxAlert').addClass('hidden');
        //         }
        //     });
        // });

        $(document).ready(function() {
            // Re-render cards when a checkbox is toggled
            $('.platform-checkbox').on('change', function() {
                currentPage = 1; // Reset to first page
                displayCards();
            });

            // Initial load
            displayCards();
        });

        function getSourceStyle(source) {
            if (!source) return "bg-gray-300 text-gray-700";
            switch (source.toLowerCase()) {
                case 'youtube':
                    return 'bg-red-500 text-white';
                case 'instagram':
                    return 'bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 text-white';
                case 'x':
                    return 'bg-black text-white';
                default:
                    return 'bg-blue-500 text-white';
            }
        }

        // Display cards based on the current tab and page
        function displayCards() {
            const selectedPlatforms = $('.platform-checkbox:checked').map((_, el) => el.value).get();
            const section = document.getElementById('results');
            section.innerHTML = ''; // Clear existing cards

            // Filter out platforms that are null in the data
            const validSelectedPlatforms = selectedPlatforms.filter(platform =>
                data[platform] !== null && Array.isArray(data[platform])
            );

            // Combine all valid data into one array
            const allData = validSelectedPlatforms.reduce((acc, platform) => {
                if (data[platform]) {
                    // Add source property to each item
                    const itemsWithSource = data[platform].map(item => ({
                        ...item,
                        source: platform
                    }));
                    return [...acc, ...itemsWithSource];
                }
                return acc;
            }, []);

            // Sort combined data
            const filteredData = allData.sort((a, b) => selectedSimilarity === 'cosine' ?
                b.cosine_similarity - a.cosine_similarity :
                b.asymetric_similarity - a.asymetric_similarity);

            if (filteredData.length === 0) {
                $('#messageBoxAlert').removeClass('hidden');
                return;
            } else {
                $('#messageBoxAlert').addClass('hidden');
            }
            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const currentData = filteredData.slice(start, end);
            console.log(currentData);
            currentData.forEach(item => {
                const card = document.createElement('div');
                card.className = 'bg-white shadow-lg rounded-lg p-4 relative';
                card.innerHTML = `
        <div class="relative my-2 pb-3">
            <div class="inline-block px-3 py-1 rounded-full text-sm font-semibold shadow-md ${getSourceStyle(item.source)}">
                ${item.source}
            </div>
        </div>
        <div class="bg-white rounded-lg p-4 relative border border-gray-300 h-40 overflow-y-auto">
            <h2 class="font-bold text-lg">Original Text:</h2>
            <h3 class="font-bold text-lg">Caption:</h3>
            <p class="text-gray-700">${item.text_caption}</p>
            <h3 class="font-bold text-lg">Comments:</h3>
            <p class="text-gray-700">${item.text_comments}</p>
        </div>
        <div class="bg-white rounded-lg p-4 relative border border-gray-300 mt-4 h-40 overflow-y-auto">
            <h2 class="font-bold text-lg">Preprocessed Text:</h2>
            <h3 class="font-bold text-lg">Caption:</h3>
            <p class="text-gray-700">${item.preprocessed_caption}</p>
            <h3 class="font-bold text-lg">Comments:</h3>
            <p class="text-gray-700">${item.preprocessed_comments}</p>
        </div>
        <div class="mt-4">
            <span class="font-bold text-sm">Similarity:</span>
            <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="h-4 rounded-full" style="width: ${parseFloat(selectedSimilarity === 'cosine' ? item.cosine_similarity : item.asymetric_similarity) * 100}%; background-color: ${getColor(parseFloat(selectedSimilarity === 'cosine' ? item.cosine_similarity : item.asymetric_similarity) * 100)};"></div>
            </div>
            <span class="text-sm text-gray-600">${selectedSimilarity === 'cosine' ? item.cosine_similarity : item.asymetric_similarity}</span>
        </div>
    `;
                section.appendChild(card);
            });

            updatePagination(filteredData.length);
        }

        // Get dynamic color based on similarity
        function getColor(similarity) {
            if (similarity >= 75) return 'green';
            if (similarity >= 50) return 'yellow';
            return 'red';
        }

        // // Switch tab
        // function showTab(tab) {
        //     // // Debug: Periksa apakah elements ditemukan
        //     // const sections = document.querySelectorAll('.results-section');
        //     // console.log("Found sections:", sections.length);

        //     // // Debug: Periksa tiap section
        //     // sections.forEach(section => {
        //     //     console.log("Section ID:", section.id);
        //     //     console.log("Current classes:", section.classList);
        //     //     section.classList.add('hidden');
        //     //     console.log("After adding hidden:", section.classList);
        //     // });
        //     document.querySelectorAll('.results-section').forEach(section => {
        //         section.style.display = 'none';
        //     });
        //     document.getElementById(tab).style.display = "grid";

        //     // Update active tab button
        //     document.querySelectorAll('button').forEach(btn => {
        //         btn.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
        //         btn.classList.add('text-gray-600');
        //     });

        //     // Highlight active tab button
        //     document.querySelector(`button[onclick="showTab('${tab}')"]`).classList.add('text-blue-600', 'border-b-2', 'border-blue-600');

        //     currentTab = tab;
        //     currentPage = 1;
        //     updatePagination();
        //     displayCards();
        // }

        // Update pagination
        function updatePagination() {
            document.getElementById('currentPage').textContent = currentPage;
        }

        function nextPage() {
            const selectedPlatforms = $('.platform-checkbox:checked').map((_, el) => el.value).get();

            // Filter out platforms that are null in the data
            const validSelectedPlatforms = selectedPlatforms.filter(platform =>
                data[platform] !== null && Array.isArray(data[platform])
            );

            // Get total items from all valid platforms
            const totalItems = validSelectedPlatforms.reduce((total, platform) => {
                return total + (data[platform] ? data[platform].length : 0);
            }, 0);

            const maxPage = Math.ceil(totalItems / itemsPerPage);

            if (currentPage < maxPage) {
                currentPage++;
                updatePagination();
                displayCards();
            }
        }

        // Previous page
        function prevPage() {
            if (currentPage > 1) {
                currentPage--;
                updatePagination();
                displayCards();
            }
        }

        // Initial load
        displayCards();

        $(document).ready(function() {
            // Re-render cards when a checkbox is toggled
            $('#homeButton').on('click', function() {
                $('#result').addClass('hidden');
                $('#input').removeClass('hidden');
            });
        });
        $(document).ready(function() {
            // Re-render cards when a checkbox is toggled
            $('#resultButton').on('click', function() {
                $('#input').addClass('hidden');
                $('#result').removeClass('hidden');
            });
        });
    </script>

</body>

</html>