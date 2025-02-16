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


document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM loaded");
    // let shelters = await fetchMyShelters('joe'); TODO: update w/ the current user
    console.log(shelters);
    
    let shelterContainer = document.getElementById("shelterContainer");

    function displayShelters(filter) {
        shelterContainer.innerHTML = "";
        shelters = Object.values(shelters);
        console.log(shelters);
        shelters
        // .filter(shelter => filter === 'All' || shelter.type === filter)
            // .sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance))
            .forEach(shelter => {
                // shelter = shelter[0];
                // console.log(shelter.type);
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
                            <button class="more-info" 
                            onclick="showDetails('${shelter.name}', '${shelter.distance}', '${shelter.people}', '${shelter.address}', '${shelter.description}', '${shelter.resources}')">
                            More Info
                            </button>
                            <button class="rsvp" onclick="rsvpPopup()">Reserve</button>
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
});