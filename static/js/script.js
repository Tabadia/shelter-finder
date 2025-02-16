    // ZZfetchUserLocation();


// document.addEventListener("DOMContentLoaded", function () {
//     console.log('DOM loaded');
//     async function fetchUserLocation() {
//         console.log('Fetching user location');
//         console.log(navigator.geolocation);
//         // if (navigator.geolocation) {
//         //     navigator.geolocation.getCurrentPosition(async function(position) {
//         //         const lat = parseFloat(position.coords.latitude);
//         //         const lon = parseFloat(position.coords.longitude);
//         //         console.log('User location:', lat, lon);
//         //         try {
//         //             const url = `http://localhost:8000/location/${lat},${lon}`; // Replace with your actual API URL
//         //             const response = await fetch(url);
                    
//         //             if (!response.ok) {
//         //                 throw new Error(`HTTP error! status: ${response.status}`);
//         //             }
                    
//         //             const data = await response.json();
//         //             console.log('User location data:', data);
//         //             // You can now use the data as needed
//         //         } catch (error) {
//         //             console.error('Error fetching user location data:', error);
//         //         }
//         //     }, function(error) {
//         //         console.error('Error getting user location:', error);
//         //     });
//         // }
//         // else {
//         //     console.log('Geolocation is not supported by this browser.');
//         // }
//     }

//     fetchUserLocation();
// });

function formatTime(minutes) {
    const days = Math.floor(minutes / 1440);
    const hours = Math.floor((minutes % 1440) / 60);
    const mins = minutes % 60;
    let timeString = '';
    if (days > 0) {
        timeString += `${days} days `;
    }
    if (hours > 0) {
        timeString += `${hours} hours `;
    }
    if (mins > 0) {
        timeString += `${mins} minutes`;
    }
    return timeString.trim();
}

function updateShelters(shelters) {   
    const shelterContainer = document.getElementById("shelterContainer");

    function displayShelters(filter) {
        shelterContainer.innerHTML = "";
        shelters = Object.values(shelters);
        console.log(shelters);
        
        shelters.filter(shelter => filter === 'All' || shelter.type === filter)
            .sort((a, b) => parseFloat(a.time) - parseFloat(b.time))
            .forEach(shelter => {
                console.log(shelter);
                console.log(shelter.type);

                const shelterBox = document.createElement("div");
                shelterBox.classList.add("shelter-box");
                shelterBox.innerHTML = `
                    <div class="shelter-content">
                        <div class="shelter-info">
                            <input type="hidden" id="shelterID" value="${shelter.ShelterID}">
                            <h3 class="shelter-name">${shelter.name}</h3>
                            <p><strong>Distance:</strong> ${shelter.time} minutes</p>
                            <p><strong>People:</strong> ${shelter.people}</p>
                            <p><strong>Address:</strong> ${shelter.address}</p>
                            <p><strong>Description:</strong> ${shelter.description}</p>
                            <p><strong>Type:</strong> ${shelter.type}</p>
                            ${shelter.verif ? '<span class="verified-badge">✔</span>' : ''}
                            <div class="shelter-buttons">
                                <button class="more-info" 
                                    onclick="showDetails('${shelter.name}', '${shelter.time}', '${shelter.people}', '${shelter.address}', '${shelter.description}', '${shelter.resources}')">
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

    window.filterShelters = displayShelters;
    displayShelters('All');
};


async function fetchLocation(lat, lon) {
    try {
        const response = await fetch(`/location/${lat},${lon}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("shelters:", data);
        updateShelters(data);  
        return data;
    } catch (error) {
        console.error("Error fetching location:", error);
        alert("Error fetching location. Please enable location services.");
    }
  }

// Example: Get user's location and fetch the address
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded");
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            console.log("Getting location...");
            const { latitude, longitude } = position.coords;
            console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
            const shelters = await fetchLocation(latitude, longitude);
            console.log(shelters);
        },
        (error) => {
            console.error("Error getting location:", error.message);
        }
    );
});

function switchToClient() {
    window.location.href = "/client-login"; // Adjust the path based on your actual client-side URL
}

const popupRSVP = document.getElementById("popupRSVP");

function rsvpPopup() {
    popupRSVP.style.display = "block";
}

function submitRSVP() {
    const phoneNumber = document.getElementById("phoneNumber").value;
    const numPeople = document.getElementById("numPeople").value;
    const name = document.getElementById("userName").value;
    popupRSVP.style.display = "none";
    const shelterId = document.querySelector("#shelterID").value; // Assuming you have a hidden input field with the shelter ID
    fetch(`/reserve/${shelterId},${phoneNumber},${numPeople},${name}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            shelter_id: shelterId,
            phone_number: phoneNumber,
            num_people: numPeople,
            name: name
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Reservation successful:', data);
        alert('Reservation successful!');
    })
    .catch(error => {
        console.error('Error making reservation:', error);
        alert('Error making reservation. Please try again.');
    });
    // post request
}

function closeRSVPPopup() {
    popupRSVP.style.display = "none";
}

const popup = document.getElementById("popup");

function showDetails(name, distance, people, address, description, resources) {
    const popupTitle = document.getElementById("popupTitle");
    const popupDistance = document.getElementById("popupDistance");
    const popupPeople = document.getElementById("popupPeople");
    const popupAddress = document.getElementById("popupAddress");
    const popupDescription = document.getElementById("popupDescription");
    const popupResources = document.getElementById("popupResources");
    const popupAISummary = document.getElementById("popupAISummary");
    const popupReserveButton = document.getElementById("popupReserve"); 

    popupTitle.textContent = name;
    popupDistance.textContent = `Distance: ${distance} minutes`;
    popupPeople.textContent = `People: ${people}`;
    popupAddress.textContent = `Address: ${address}`;
    popupDescription.textContent = description;
    popupResources.textContent = resources;
    popupAISummary.textContent = "(Still to implement)";

    popupReserveButton.setAttribute("onclick", `rsvpShelter('${name}', '${address}')`);
    document.getElementById("popup").style.display = "flex";

    // Set the icon based on shelter type
    let iconHTML = "";
    if (type === "Hospital") {
        iconHTML = "🏥"; // Hospital Icon
    } else if (type === "School") {
        iconHTML = "🏫"; // School Icon
    } else if (type === "Home") {
        iconHTML = "🏠"; // Home Icon
    } else if (type === "Homeless Shelter") {
        iconHTML = "🛌"; // Shelter Icon
    } else {
        iconHTML = "❓"; // Default/Fallback Icon
    }
    popupIcon.innerHTML = iconHTML; // Insert the icon

    // Show the popup
    document.getElementById("popup").style.display = "flex";
    popup.style.display = "flex";
};
    
function closePopup() {
    popup.style.display = "none";
}

