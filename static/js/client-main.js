<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add New Shelter</title>
    <style>
        label {
            display: block;
            margin-bottom: 10px;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
        }
        button[type="submit"] {
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

<h1>Add New Shelter</h1>

<form id="addShelterForm">
    <label for="name">Shelter Name:</label>
    <input type="text" id="name" name="name" required>

    <label for="address">Address:</label>
    <input type="text" id="address" name="address" required>

    <label for="capacity">Capacity:</label>
    <input type="number" id="capacity" name="capacity" required>

    <label for="description">Description:</label>
    <textarea id="description" name="description"></textarea>

    <button type="submit">Add Shelter</button>
</form>

<script>
    document.getElementById('addShelterForm').addEventListener('submit', function(event) {
        event.preventDefault();
        // Here you would send the form data to your backend to create a new shelter
        const formData = new FormData(this);
        fetch('/shelters/', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Shelter added:', data);
            window.location.href = 'index.html'; // Redirect back to shelter list
        })
        .catch(error => console.error('Error adding shelter:', error));
    });
</script>

</body>
</html>
