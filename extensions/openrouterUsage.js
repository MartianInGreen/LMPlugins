// Set your OPEN_ROUTER_API_KEY Cookie to your OpenRouter API Key
// Set your OPEN_ROUTER_OFFSET Cookie to 0 or a positive float if you want to offset the usage by a certain amount

function getCookie(name) {
    const cookieArr = document.cookie.split(";");

    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        
        /* Removing whitespace at the beginning
        * of the cookie name and compare it with
        * the given string */
        if (cookiePair[0].trim() === name) {
        // Decode the cookie value to handle special characters
        return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if cookie is not found
    return null;
}

// Get the OpenRouter API Key from the Cookie
const openRouterApiKey = getCookie('OPEN_ROUTER_API_KEY');
const openRouterOffset = getCookie('OPEN_ROUTER_OFFSET');

console.log(openRouterApiKey)
console.log(openRouterOffset)

let firstRun = false;

function updateUsage(){
    result = fetch('https://openrouter.ai/api/v1/auth/key', {
        method: 'GET',
        headers: {
            Authorization: 'Bearer ' + openRouterApiKey
        }
        });
    result.then((response) => {
        response.json().then((data) => {
            const usage = data.data.usage;
            // Limit usageOffset to 2 decimals
            const usageOffset = parseFloat((usage - parseFloat(openRouterOffset)).toFixed(2));

            const usageDisplay = document.querySelector('[data-element-id="usage-display"]');
            usageDisplay.textContent = `Usage: ${usageOffset}`;

            console.log(usage)
            console.log(usageOffset)

            });
        });
}

// Get the usage data from the OpenRouter API
window.addEventListener('load', function() {
    setInterval(() => {
        // check if button exists
        if (document.querySelector('[data-element-id="usage-display"]')) {
            return;
        }

        // Add a quick enable/disable button for the streaming feature under data-element-id="current-chat-title"
        const usageDisplay = document.createElement('span');
        usageDisplay.textContent = 'Usage: 0';
        usageDisplay.style.marginLeft = '10px';
        usageDisplay.style.cursor = 'pointer';
        usageDisplay.dataset.elementId = 'usage-display';

        const currentChatTitle = document.querySelector('[data-element-id="current-chat-title"]');
        const child = currentChatTitle.children[1];

        // Create one div to hold the usage display
        child.appendChild(usageDisplay);

        if (!firstRun){
            updateUsage()
            firstRun = false;
        }

    }, 500);

    setInterval(() => {
            updateUsage();
        }, 30000);
    });
