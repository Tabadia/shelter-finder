async function fetchMyShelters(owner_username) {
    try {
        const response = await fetch(`/shelters/owner/${owner_username}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
            console.log("shelters:", data);
        return data;
    } catch (error) {
      console.error("Error fetching location:", error);
    }
}

function addShelter() {
    form = document.getElementById("addShelterForm");
    form.style.display = "block";
    btn = document.getElementById("addShelterButton");
    btn.style.display = "none";
}

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM loaded");
    const username = localStorage.getItem("username");
    let shelters = await fetchMyShelters(username); //TODO: update w/ the current user
    console.log(shelters);
    
    let shelterContainer = document.getElementById("shelterContainer");

    function displayShelters() {
        shelterContainer.innerHTML = "";
        shelters = Object.values(shelters);
        console.log(shelters);
        shelters
            .forEach(shelter => {
                console.log(shelter);
                const shelterBox = document.createElement("div");
                shelterBox.classList.add("shelter-box");
                shelterBox.innerHTML = `
                    <div class="shelter-content">
                        <div class="shelter-info">
                            <input type="hidden" id="shelterID" value="${shelter.ShelterID}">
                            <h3 class="shelter-name">${shelter.name} ${shelter.verif ? '<span class="verified-badge">✔</span>' : ''}</h3>
                            <p><strong>Distance:</strong> ${shelter.time} minutes</p>
                            <p><strong>People:</strong> ${shelter.people}</p>
                            <p><strong>Address:</strong> ${shelter.address}</p>
                            <p><strong>Description:</strong> ${shelter.description}</p>
                            <p><strong>Type:</strong> ${shelter.type}</p> 
                            <div class="shelter-buttons">
                                <button class="more-info" 
                                onclick="showDetails(
                                    '${shelter.name}', 
                                    '${shelter.time}', 
                                    '${shelter.people}', 
                                    '${shelter.address}', 
                                    '${shelter.description}', 
                                    '${shelter.resources}', 
                                    '${shelter.type}'
                                )">
                                More Info
                                </button>
                                <button class="rsvp" onclick="rsvpPopup()">Reserve</button>
                            </div>
                        </div>
                        <div class="shelter-image">
                            <img src="../static/images/${shelter.image}" alt="">
                        </div>
                    </div>
                `;
                shelterContainer.appendChild(shelterBox);
            });
    }
    displayShelters();
});


document.getElementById('addShelterForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Here you would send the form data to your backend to create a new shelter
    const formData = new FormData(this);
    const username = localStorage.getItem('username');
    formData.append('owner_username', username);
    console.log('Form data:', JSON.stringify(Object.fromEntries(formData)));
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
        window.location.reload(); 
    })
    .catch(error => console.error('Error adding shelter:', error));
});
