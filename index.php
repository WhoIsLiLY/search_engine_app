<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #e0e6ed;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }

        .container {
            background-color: #2c3e50;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 40px;
            width: 600px;
            max-width: 90%;
            border: 2px solid #b4c9e1;
        }

        .container h2 {
            font-size: 24px;
            color: #ecf0f1;
            margin-bottom: 20px;
            text-align: center;
        }

        .form-group label {
            font-weight: bold;
            color: #bdc3c7;
        }

        .form-group input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #b4c9e1;
            border-radius: 5px;
            font-size: 14px;
            background-color: #34495e;
            color: #ecf0f1;
        }

        .options {
            display: flex;
            flex-direction: column;
            gap: 15px;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            color: #bdc3c7;
        }

        .submit-btn {
            width: 100%;
            padding: 10px;
            border: none;
            background-color: #a2d2ff;
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .submit-btn:hover {
            background-color: #80b5e9;
        }
        .result-item {
            margin-top: 60px;
        }

        .result-item h4 {
            font-size: 16px;
            color: #ecf0f1;
            margin: 0;
        }

        .result-item p {
            color: #bdc3c7;
            
        }
        .pagination{
            margin-top: 40px;
            display: flex;
            justify-content: center;
        }

        .pagination a {
            margin: 0 5px;
            color: #a2d2ff;
            text-decoration: none;
            transition: color 0.3s;
        }

        .pagination a:hover {
            color: #ecf0f1;
            
        }

    </style>
</head>
<body>

<div class="container">
    <h2>SEARCHING DATA</h2>
    <form action="result.php" method="POST">
        <div class="form-group">
            <label for="keyword">Keyword:</label>
            <input type="text" id="keyword" name="keyword" placeholder="Enter keyword" required>
        </div>
        
        <div class="options">
            <div class="source-options">
                <label><b>Source:</b></label>
                <input type="checkbox" name="source[]" value="X"> X
                <input type="checkbox" name="source[]" value="Instagram"> Instagram
                <input type="checkbox" name="source[]" value="Youtube"> Youtube
            </div>
            
            <div class="similarity-options">
                <label><b>Similarity Method:</b></label>
                <input type="radio" name="method" value="Method 1" checked> Method 1
                <input type="radio" name="method" value="Method 2"> Method 2
            </div>
        </div>
        
        <input type="submit" name="crawl" value="Search" class="submit-btn">
    </form>

    
    <div class="results">
        <div class="result-item">
            <h4>Source: X</h4>
            <p><b>Original text:</b> ....</p>
            <p><b>Preprocessing Result:</b> ....</p>
            <p><b>Similarity:</b> ....</p>
        </div>
        <div class="result-item">
            <h4>Source: Instagram</h4>
            <p><b>Original text:</b> ....</p>
            <p><b>Preprocessing Result:</b> ....</p>
            <p><b>Similarity:</b> ....</p>
        </div>
        <div class="result-item">
            <h4>Source: Youtube</h4>
            <p><b>Original text:</b> ....</p>
            <p><b>Preprocessing Result:</b> ....</p>
            <p><b>Similarity:</b> ....</p>
        </div>

        
        <div class="pagination">
            <a href="#">1</a> | <a href="#">2</a> | <a href="#">3</a> | ... | <a href="#">5</a> Next
        </div>
    </div>
</div>


</body>
</html>
