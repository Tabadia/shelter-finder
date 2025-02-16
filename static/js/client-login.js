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
        const data = await fetch("/api/client/login", {
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
            // if(response.
            // if (!response.ok) {
            //     throw new Error(`HTTP error! Status: ${response.status}`);
            // }
            return response.json();
        })
        const popup = document.getElementById("popup");
        console.log('popup', popup);

        switch (data[0]) {
            case "0":
                console.log("Login successful");
                window.location.href = "/client-dashboard";
                break;
            case "1":
                console.log("Login failed");
                popup.innerHTML = "Login failed, try again";
                break;
            default:
                console.log("User not found");
                popup.innerHTML = "User not found. Please sign up, or someone else has created an account with this username";
        }

        
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