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

async function queuePopup(shelterID) {
    // const queuePopup = document.getElementById("queuePopup");
    // const queueContent = document.getElementById("queueContent");
    // const queueClose = document.getElementById("queueClose");
    // queuePopup.style.display = "block";
    // queueClose.onclick = function() {
    //     queuePopup.style.display = "none";
    // }
    await fetchQueue(shelterID);
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
                const shelterBox = document.createElement("div");
                shelterBox.classList.add("shelter-box");
                shelterBox.innerHTML = `
                    <div class="shelter-content">
                        <div class="shelter-info">
                            <input type="hidden" id="shelterID" value="${shelter.ShelterID}">
                            <div class="name">${getFontAwesomeIcon(shelter.type)} 
                                ${shelter.name}
                                ${shelter.verif ? '<span class="fa-regular fa-circle-check verified"></span>' : ''}
                            </div>
                            <div class="stats">
                                <span class="capacity">
                                    <i class="fa-solid fa-people-group"></i>
                                    <span>${shelter.capacity - shelter.curr_cap}</span>
                                </span>
                                <span class="time">
                                    <i class="fa-solid fa-stopwatch"></i>
                                    <span>${shelter.time}min</span>
                                </span>
                                <span class="address">
                                    <i class="fa-solid fa-location-dot"></i>
                                    <span>${shelter.address}</span>
                                </span>
                            </div>
                            <p class="description">${shelter.desc}</p>
                            <div class="shelter-buttons">
                                <button class="queue" onclick="queuePopup('${shelter.ShelterID}')">
                                View Queue
                                </button>
                            </div>
                        </div>
                        <div class="shelter-image">
                            <img src="../static/images/${shelter.image}" alt="">
                        </div>
                    </div>
                `;
                shelterContainer.appendChild(shelterBox);
            });
        console.log(shelterContainer);
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

function getFontAwesomeIcon(type) {
    type = type.trim().toLowerCase();

    switch (type) {
        case "hospital":
            return "<i class=\"fa-solid fa-hospital\"></i>";
        case "school":
            return "<i class=\"fa-solid fa-school\"></i>";
        case "home":
            return "<i class=\"fa-solid fa-house\"></i>";
        case "homeless shelter":
            return "<i class=\"fa-solid fa-bed\"></i>";
        default:
            return "<i class=\"fa-solid fa-question\"></i>";
    }
}

async function fetchQueue(shelterID) {
    try {
        const response = await fetch(`/shelters/queue/${shelterID}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let ret = await response.json();
        let queue = ret[0];
        let checked_in = ret[1];
        console.log("queue:", queue);
        console.log("checked_in:", checked_in);
        return data;
    } catch (error) {
      console.error("Error fetching location:", error);
    }
}