// client login / signup

// once logged in set login invisible and load page
//

function SwitchToLogin() {
    window.location.href = "/client-login";
}

function SwitchToSignup() {
    window.location.href = "/client-signup";
}


async function fetchLogin(username, password) {
    try {
        await fetch("/api/client/login/", {
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
                    console.log("Login successful");
                    localStorage.setItem('username', username);
                    // let storedValue = localStorage.getItem('username');
                    // console.log('storedValue', storedValue);
                    window.location.href = "/client-dashboard";
                    break;
                default:
                    console.log("Login failed");
                    errorMessage.style.display = "block"; // Show error message
                    errorMessage.textContent = "Login failed, try again!";
                }
        });
    } catch (error) {
      console.error("Error fetching location:", error);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded");

    // Add event listener to the form
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        const username = document.getElementById('loginUser').value;
        const password = document.getElementById('loginPass').value;

        await fetchLogin(username, password);
    });
});