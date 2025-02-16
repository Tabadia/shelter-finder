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

        console.log("Filtering shelters:", filter);
        
        shelters.filter(shelter => 
            filter === 'All' || shelter.type.trim().toLowerCase() === filter.trim().toLowerCase()
        )
        .sort((a, b) => parseFloat(a.time) - parseFloat(b.time))
        .forEach(shelter => {
            console.log("Displaying shelter:", shelter.type);
    

                const shelterBox = document.createElement("div");
                shelterBox.classList.add("shelter-box");
                shelterBox.innerHTML = `
                    <div class="shelter-content">
                        <div class="shelter-info">
                            <input type="hidden" id="shelterID" value="${shelter.ShelterID}">
                            <h3 class="shelter-name">${shelter.name} ${shelter.verif ? '<span class="fa-regular fa-circle-check"></span>' : ''}</h3>
                            <p><strong><i class="fa-solid fa-person-walking-arrow-right"></i>  </i>  Distance:</strong> ${shelter.time} minutes</p>
                            <p><strong><i class="fa-solid fa-people-group"></i>  Capacity:</strong> ${shelter.capacity - shelter.curr_cap}</p>
                            <p><strong><i class="fa-solid fa-location-dot"></i>  Address:</strong> ${shelter.address}</p>
                            <p><strong><i class="fa-solid fa-book"></i>  Description:</strong> ${shelter.description}</p>
                            <p><strong><i class="fa-solid fa-bookmark"></i>  Type:</strong> ${shelter.type}</p> 
                            <div class="shelter-buttons">
                                <button class="more-info" 
                                onclick="showDetails(
                                    '${shelter.name} ${shelter.verif ? '✔' : ''}', 
                                    '${shelter.time}', 
                                    '${shelter.capacity - shelter.curr_cap}', 
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

function submitRSVP(event) {
    event.preventDefault();
    const phoneNumber = document.getElementById("phoneNumber").value;
    const numPeople = document.getElementById("numPeople").value;
    const name = document.getElementById("userName").value;
    popupRSVP.style.display = "none";
    const shelterId = document.querySelector("#shelterID").value; // Assuming you have a hidden input field with the shelter ID
    console.log(shelterId);
    fetch("/reserve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            shelter_id: shelterId,
            phone_number: phoneNumber,
            num_people: parseInt(numPeople),
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
        console.log("People reserved:", data.count); // DATA.COUNT IS THE TOTAL PEOPLE RESERVED RN
        alert('Reservation successful!');
    })
    .catch(error => {
        console.error('Error making reservation:', error);
        alert('Error making reservation. Please try again.');
    });
}

const popup = document.getElementById("popup");

function showDetails(name, distance, people, address, description, resources, type) {
    const popup = document.getElementById("popup");
    const popupTitle = document.getElementById("popupTitle");
    const popupDistance = document.getElementById("popupDistance");
    const popupPeople = document.getElementById("popupPeople");
    const popupAddress = document.getElementById("popupAddress"); 
    const popupDescription = document.getElementById("popupDescription"); 
    const popupResources = document.getElementById("popupResources");
    const popupAISummary = document.getElementById("popupAISummary");
    const popupReserveButton = document.getElementById("popupReserve");
    const popupIcon = document.getElementById("popupIcon"); 

    console.log('inittt', popup, popupIcon);

    popupTitle.textContent = name;
    popupDistance.textContent = `Distance: ${distance} minutes`;
    popupPeople.textContent = `People: ${people}`;
    popupAddress.textContent = `Address: ${address}`;
    popupDescription.textContent = description;
    popupResources.textContent = resources;
    popupAISummary.textContent = "(Coming Soon)";


    type = type.trim().toLowerCase(); // Remove spaces, ensure lowercase

    let iconHTML = "";
    switch (type) {
        case "hospital":
            iconHTML = "<i class=\"fa-solid fa-hospital\"></i>"; 
            break;
        case "school":
            iconHTML = "🏫"; 
            break;
        case "home":
            iconHTML = "🏠"; 
            break;
        case "homeless shelter":
            iconHTML = "🛌"; 
            break;
        default:
            iconHTML = "❓"; 
            console.error(`Unknown shelter type: '${type}'`);
            break;
    }


    if (popupIcon) {
        popupIcon.innerHTML = iconHTML;
    } else {
        console.error("popupIcon element not found!");
    }

    
    if (popup) {
        popup.style.display = "flex";
    }
}

function closePopup() {
    const popup = document.getElementById("popup");
    if (popup) {
        popup.style.display = "none";
    } else {
        console.error("Popup not found!");
    }
}

function closeRSVPPopup() {
    const popupRSVP = document.getElementById("popupRSVP");
    if (popupRSVP) {
        popupRSVP.style.display = "none";
    } else {
        console.error("RSVP popup not found!");
    }
}

