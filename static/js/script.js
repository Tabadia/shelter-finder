document.addEventListener("DOMContentLoaded", function() {
    const shelters = [
        { type: "Hospital", distance: "2 miles", people: 50, address: "123 Main St", description: "Full medical services available.", resources: "Doctors, Beds, Medicine" },
        { type: "School", distance: "5 miles", people: 30, address: "456 Oak St", description: "Temporary shelter with basic amenities.", resources: "Food, Water, Sleeping Bags" },
        { type: "Home", distance: "3 miles", people: 20, address: "789 Pine St", description: "Available for small families.", resources: "Private Rooms, Kitchen" },
        { type: "Homeless Shelter", distance: "4 miles", people: 15, address: "101 Elm St", description: "Open for those in urgent need.", resources: "Meals, Showers, Counseling" }
    ];

    const shelterContainer = document.getElementById("shelterContainer");
    const popup = document.getElementById("popup");
    const popupTitle = document.getElementById("popupTitle");
    const popupDescription = document.getElementById("popupDescription");
    const popupResources = document.getElementById("popupResources");
    const popupAISummary = document.getElementById("popupAISummary");

    function displayShelters(filter) {
        shelterContainer.innerHTML = "";
        shelters.filter(shelter => filter === 'All' || shelter.type === filter)
            .forEach(shelter => {
                const shelterBox = document.createElement("div");
                shelterBox.classList.add("shelter-box");
                shelterBox.innerHTML = `
                    <div class="shelter-content">
                        <div class="shelter-info">
                            <h3>${shelter.type}</h3>
                            <p><strong>Distance:</strong> ${shelter.distance}</p>
                            <p><strong>People:</strong> ${shelter.people}</p>
                            <p><strong>Address:</strong> ${shelter.address}</p>
                            <p><strong>Description:</strong> ${shelter.description}</p>
                            <button class="more-info" onclick="showDetails('${shelter.type}', '${shelter.description}', '${shelter.resources}')">More Info</button>
                            <button class="rsvp">RSVP</button>
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
        popup.style.display = "flex";
    }

    window.closePopup = function() {
        popup.style.display = "none";
    }
});
