// client login / signup

// once logged in set login invisible and load page
//

function SwitchToLogin() {
    window.location.href = "/client-login";
}

function SwitchToSignup() {
    window.location.href = "/client-signup";
}


async function fetchSignup(username, password) {
    try {
        await fetch("/api/client/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username, 
                password: password,
            })
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log('data', data, data['status']);
            const popup = document.getElementById("popup");
            
            switch (data['status']) {
                case "0":
                    console.log("Login created");
                    localStorage.setItem('username', username);
                    window.location.href = "/client-dashboard";
                    break;
                default:
                    console.log("Login failed");
                    errorMessage = document.querySelector('#errorMessage');
                    errorMessage.style.display = "block"; 
                    errorMessage.textContent = "Account already exists!";
                }
        });
    } catch (error) {
      console.error("Error fetching location:", error);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded");
    document.getElementById('signupForm').addEventListener('submit', async function(event) {
        event.preventDefault(); 

        const username = document.getElementById('signupUser').value;
        const password = document.getElementById('signupPass').value;

        await fetchSignup(username, password);
    });
});