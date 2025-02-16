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
    const queuePopup = document.getElementById("queuePopup");
    const queueList = document.getElementById("queueList");
    const checkedInList = document.getElementById("checkedInList");

    queuePopup.style.display = "block"; 

    const queueData = await fetchQueue(shelterID);

    const queue = queueData[0];
    const checkedIn = queueData[1];

    queueList.innerHTML = "";  
    checkedInList.innerHTML = "";  

    // Populate Queue List
    queue.forEach(person => {
        const listItem = document.createElement("li");
        listItem.classList.add("queue-item");
        listItem.innerHTML = `
            <span><strong>${person.name}</strong> (${person.phone_number})</span>
            <button onclick="checkIn('${person.phone_number}', '${shelterID}')">Check In</button>
        `;
        queueList.appendChild(listItem);
    });

    // Populate Checked-In List
    checkedIn.forEach(person => {
        const listItem = document.createElement("li");
        listItem.classList.add("queue-item");
        listItem.innerHTML = `<span><strong>${person.name}</strong> (${person.phone_number})</span>
        <button onclick="removeCheckIn('${person.phone_number}', '${shelterID}')">Remove</button>
        `;
        
        checkedInList.appendChild(listItem);
    });

    queuePopup.style.display = "block";
}

function closeQueuePopup() {
    document.getElementById("queuePopup").style.display = "none";
}

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM loaded");
    const username = localStorage.getItem("username");
    let shelters = await fetchMyShelters(username); 
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
                                ${shelter.verif ? '<span class=\"fa-regular fa-circle-check verified\"></span>' : ''}
                            </div>
                            <div class="stats">
                                <span class="capacity">
                                    <i class="fa-solid fa-people-group"></i>
                                    <span>${shelter.capacity - shelter.curr_cap}</span>
                                </span>
                                <span class="address">
                                    <i class="fa-solid fa-location-dot"></i>
                                    <span>${shelter.address}</span>
                                </span>
                            </div>
                            <div class="shelter-buttons">
                                <button class="queue" onclick="queuePopup('${shelter.ShelterID}')">View Queue</button>
                                <button class="remove" onclick="removeShelter('${shelter.ShelterID}')">Remove</button>
                            </div>
                        </div>
                        <div class="shelter-image">
                            <img src="../static/images/${shelter.image}" alt="">
                        </div>
                    </div>
                `;
                shelterContainer.appendChild(shelterBox);
            });
        if (shelterContainer.innerHTML === "") {
            shelterContainer.innerHTML = "<p style='color: gray; font-size: 18px;'>No sheltrs available.</p>";
        }
        console.log(shelterContainer);
    }
    displayShelters();
});
function closeQueuePopup() {
    document.getElementById("queuePopup").style.display = "none";
}


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
        const response = await fetch(`/shelters/${shelterID}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const shelter = await response.json();
        console.log("shelter:", shelter);

        const queue = shelter.queue.filter(person => !person.check_in);
        const checkedIn = shelter.queue.filter(person => person.check_in);
        
        let queueList = document.getElementById("queueList");
        let checkedInList = document.getElementById("checkedInList");

        queueList.innerHTML = ""; 
        checkedInList.innerHTML = "";

        queue.forEach(person => {
            const listItem = document.createElement("li");
            listItem.classList.add("queue-item");
            listItem.innerHTML = `
                <span><strong>${person.name}</strong> (${person.phone_number})</span>
                <button onclick="checkIn('${person.phone_number}', '${shelterID}')">Check In</button>
            `;
            queueList.appendChild(listItem);
        });

        checkedIn.forEach(person => {
            const listItem = document.createElement("li");
            listItem.classList.add("queue-item");
            listItem.innerHTML = `
                <span><strong>${person.name}</strong> (${person.phone_number})</span>
                <button onclick="removeCheckIn('${person.phone_number}', '${shelterID}')">Remove</button>
            `;
            checkedInList.appendChild(listItem);
        });

        return [queue, checkedIn];
    } catch (error) {
      console.error("Error fetching location:", error);
    }
}

async function checkIn(number, shelterID) {
    try {
        const response = await fetch(`/check-in/${shelterID}/${number}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone: number })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        console.log(`Checked in: ${number}`);
        fetchQueue(shelterID); 

    } catch (error) {
        console.error("Error checking in:", error);
    }
}


async function removeShelter(shelterID) {
    try {
        const response = await fetch(`/shelters/${shelterID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Shelter deleted:', data);
        window.location.reload();
    } catch (error) {
        console.error('Error deleting shelter:', error);
    }
}

async function removeCheckIn(number, shelterID) {
    try {
        const response = await fetch(`/check-in/${shelterID}/${number}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone: number })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        console.log(`Removed check-in: ${number}`);
        fetchQueue(shelterID); 

    } catch (error) {
        console.error("Error removing check-in:", error);
    }
}