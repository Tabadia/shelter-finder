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

function updateShelters(shelters) {   
    
    const shelterContainer = document.getElementById("shelterContainer");
    const popup = document.getElementById("popup");
    const popupTitle = document.getElementById("popupTitle");
    const popupDescription = document.getElementById("popupDescription");
    const popupResources = document.getElementById("popupResources");
    const popupAISummary = document.getElementById("popupAISummary");
    const popupRSVP = document.getElementById("popupRSVP");
    const popupClose = document.querySelector(".close");

    function displayShelters(filter) {
        shelterContainer.innerHTML = "";
        shelters = Object.values(shelters);
        console.log(shelters);
        shelters.filter(shelter => filter === 'All' || shelter.type === filter)
            .sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance))
            .forEach(shelter => {
                shelter = shelter[0];
                console.log(shelter.type);
                const shelterBox = document.createElement("div");
                shelterBox.classList.add("shelter-box");
                shelterBox.innerHTML = `
                    <div class="shelter-content">
                        <div class="shelter-info">
                            <h3>${shelter.name}</h3>
                            <p><strong>Distance:</strong> ${shelter.distance}</p>
                            <p><strong>People:</strong> ${shelter.people}</p>
                            <p><strong>Address:</strong> ${shelter.address}</p>
                            <p><strong>Description:</strong> ${shelter.description}</p>
                            ${shelter.verif ? '<span class="verified-badge">Verified</span>' : ''}
                            <button class="more-info" onclick="showDetails('${shelter.type}', '${shelter.description}', '${shelter.resources}')">More Info</button>
                            <button class="rsvp">RSVP</button>
                        </div>
                        <div class="shelter-image">
                        <img src="../static/images/${shelter.image}" alt="${shelter.type}">
                        </div>
                    </div>
                `;
                shelterContainer.appendChild(shelterBox);
            });
    }

    window.filterShelters = displayShelters;
    displayShelters('All');

    window.showDetails = function(title, description, resources) {
        popupTitle.innerText = title;
        popupDescription.innerText = description;
        popupResources.innerText = resources;
        popupAISummary.innerText = "(Coming Soon)";
        popupRSVP.setAttribute("onclick", `rsvpShelter('${title}', '${address}')`);
        popup.style.display = "flex";
        popupClose.style.opacity = "1";
        popupClose.style.transition = "opacity 0.5s ease-in-out";
        popupClose.style.display = "block";
    }
    window.rsvpShelter = function(type, address) {
        alert(`You have successfully RSVP'd to ${type} at ${address}.`);
    }
    window.closePopup = function() {
        popup.style.display = "none";
    }
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




