<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KEPO</title>
    <link href="/public/css/output.css" rel="stylesheet">
</head>

<body class="bg-gray-100 text-gray-900">

    <!-- Header -->
    <header class="bg-blue-600 text-white py-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold">KEPO.COM</h1>
            <input type="text" placeholder="Search..." class="p-2 rounded-lg w-1/2">
        </div>
    </header>

    <!-- Form Input -->
    <div id="input" class="container mx-auto my-8">
        <h2 class="text-lg font-bold mb-4">SEARCHING DATA</h2>
        <form id="searchForm" class="space-y-4">
            <div>
                <label class="font-bold">Keyword:</label>
                <input type="text" name="keyword" id="keyword" class="p-2 border border-gray-300 rounded-lg w-full" required>
            </div>
            <div>
                <label class="font-bold">Similarity Method:</label>
                <div class="space-x-4">
                    <label><input type="radio" name="method" value="Minkowski" checked> Minkowski</label>
                    <label><input type="radio" name="method" value="Canberra"> Canberra</label>
                </div>
            </div>
            <button type="submit" id="searchButton" class="px-4 py-2 bg-blue-600 text-white rounded-lg">Search</button>
        </form>
    </div>

    <!-- Form Result -->
    <div id="result" class="hidden">
        <!-- Tabs -->
        <div class="container mx-auto my-4">
            <div class="flex space-x-4 border-b">
                <button class="py-2 px-4 text-blue-600 border-b-2 border-blue-600" onclick="showTab('all')">All</button>
                <button class="py-2 px-4 text-gray-600 hover:text-blue-600" onclick="showTab('instagram')">Instagram</button>
                <button class="py-2 px-4 text-gray-600 hover:text-blue-600" onclick="showTab('x')">X</button>
                <button class="py-2 px-4 text-gray-600 hover:text-blue-600" onclick="showTab('youtube')">YouTube</button>
            </div>
        </div>

        <!-- Results Section -->
        <div class="container mx-auto my-8">
            <!-- All Results -->
            <div id="all" class="results-section grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- All Cards will be injected here -->
            </div>
            <!-- Instagram Results -->
            <div id="instagram" class="results-section grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 hidden">
                <!-- Instagram Cards will be injected here -->
            </div>

            <!-- X Results -->
            <div id="x" class="results-section grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 hidden">
                <!-- X Cards will be injected here -->
            </div>

            <!-- YouTube Results -->
            <div id="youtube" class="results-section grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 hidden">
                <!-- YouTube Cards will be injected here -->
            </div>
        </div>

        <!-- Pagination -->
        <div class="container mx-auto text-center my-4">
            <button class="py-2 px-4 bg-gray-200 rounded-lg mr-2" onclick="prevPage()">Previous</button>
            <span id="currentPage" class="font-bold">1</span>
            <button class="py-2 px-4 bg-gray-200 rounded-lg ml-2" onclick="nextPage()">Next</button>
        </div>

    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-4 mt-8">
        <div class="container mx-auto text-center">
            <p>&copy; 2025 KEPO.COM. All rights reserved.</p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        let data = {
            all: [],
            instagram: [],
            x: [],
            youtube: []
        };
        $(document).ready(function() {
            $('#searchForm').on('submit', function(event) {
                event.preventDefault(); // Mencegah reload halaman

                const keyword = $('#keyword').val();
                const method = $('input[name="method"]:checked').val();

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
                        method: method,
                    },
                    dataType: 'json',
                    success: function(response) {
                        // Reset tombol ke state awal
                        $('#searchButton').text('Search').prop('disabled', false).removeClass('bg-gray-400 text-white');

                        // Sembunyikan form input
                        $('#input').addClass('hidden');

                        // Munculkan form result
                        $('#result').removeClass('hidden');
                        
                        console.log(response);
                        // Proses data dan masukkan ke dalam variabel `data`
                        data = {
                            all: [
                                ...response.instagram,
                                ...response.x,
                                ...response.youtube
                            ],
                            instagram: response.instagram,
                            x: response.x,
                            youtube: response.youtube,
                        };
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
//         // Dummy data
//         const data = {
//             all: Array.from({
//                 length: 20
//             }, (_, i) => {
//                 const sources = ['Youtube', 'Instagram', 'X']; // Array sumber
//                 const randomSource = sources[Math.floor(Math.random() * sources.length)]; // Pilih sumber secara acak

//                 return {
//                     source: randomSource, // Sumber acak
//                     text: `All post ${i + 1}`,
//                     preprocessed: `Preprocessed text ${i + 1}`,
//                     similarity: Math.floor(Math.random() * 100) + 1, // Random similarity
//                 };
//             }),
//             instagram: Array.from({
//                 length: 15
//             }, (_, i) => ({
//                 source: `Instagram`,
//                 text: `Instagram post ${i + 1}`,
//                 preprocessed: `Preprocessed text ${i + 1}     Lorem ipsum dolor sit amet consectetur adipisicing elit. Adipisci corrupti molestias aliquid ut perferendis quisquam mollitia architecto quod atque, ad, nobis nostrum ullam tenetur laborum impedit suscipit expedita eveniet deleniti!
// `,
//                 similarity: Math.floor(Math.random() * 100) + 1,
//             })),
//             x: Array.from({
//                 length: 12
//             }, (_, i) => ({
//                 source: `X`,
//                 text: `X post ${i + 1}`,
//                 preprocessed: `Preprocessed text ${i + 1}`,
//                 similarity: Math.floor(Math.random() * 100) + 1,
//             })),
//             youtube: Array.from({
//                 length: 20
//             }, (_, i) => ({
//                 source: `Youtube`,
//                 text: `YouTube post ${i + 1}`,
//                 preprocessed: `Preprocessed text ${i + 1}`,
//                 similarity: Math.floor(Math.random() * 100) + 1,
//             })),
//         };

        let currentTab = 'all';
        let currentPage = 1;
        const itemsPerPage = 6;

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
            const section = document.getElementById(currentTab);
            section.innerHTML = ''; // Clear existing cards

            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const currentData = [...data[currentTab]].sort((a, b) => b.similarity - a.similarity).slice(start, end);
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
            <p class="text-gray-700">${item.text}</p>
        </div>
        <div class="bg-white rounded-lg p-4 relative border border-gray-300 mt-4 h-40 overflow-y-auto">
            <h2 class="font-bold text-lg">Preprocessed Text:</h2>
            <p class="text-gray-500">${item.preprocessed}</p>
        </div>
        <div class="mt-4">
            <span class="font-bold text-sm">Similarity:</span>
            <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="h-4 rounded-full" style="width: ${item.similarity}%; background-color: ${getColor(item.similarity)};"></div>
            </div>
            <span class="text-sm text-gray-600">${item.similarity}%</span>
        </div>
    `;
                section.appendChild(card);
            });
        }

        // Get dynamic color based on similarity
        function getColor(similarity) {
            if (similarity >= 75) return 'green';
            if (similarity >= 50) return 'yellow';
            return 'red';
        }

        // Switch tab
        function showTab(tab) {
            // // Debug: Periksa apakah elements ditemukan
            // const sections = document.querySelectorAll('.results-section');
            // console.log("Found sections:", sections.length);

            // // Debug: Periksa tiap section
            // sections.forEach(section => {
            //     console.log("Section ID:", section.id);
            //     console.log("Current classes:", section.classList);
            //     section.classList.add('hidden');
            //     console.log("After adding hidden:", section.classList);
            // });
            document.querySelectorAll('.results-section').forEach(section => {
                section.style.display = 'none';
            });
            document.getElementById(tab).style.display = "grid";

            // Update active tab button
            document.querySelectorAll('button').forEach(btn => {
                btn.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
                btn.classList.add('text-gray-600');
            });

            // Highlight active tab button
            document.querySelector(`button[onclick="showTab('${tab}')"]`).classList.add('text-blue-600', 'border-b-2', 'border-blue-600');

            currentTab = tab;
            currentPage = 1;
            updatePagination();
            displayCards();
        }

        // Update pagination
        function updatePagination() {
            document.getElementById('currentPage').textContent = currentPage;
        }

        // Next page
        function nextPage() {
            const maxPage = Math.ceil(data[currentTab].length / itemsPerPage);
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
    </script>

</body>

</html>