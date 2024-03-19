window.addEventListener('load', function() {
    setTimeout(function() {
        // Get window url
        const url = new URL(window.location.href)

        // if window url is .../?search=encoded_query get the query 

        if (url.searchParams.has('search')) {
            const query = url.searchParams.get('search');
            
            // Convert the query to a string
            const decodedQuery = decodeURIComponent(query); //.toString();
            console.log('Searching for: ', decodedQuery)

            // Go trough all data-element-id="single-character-container" and for all children data-element-id="character-title" check if the innerText includes the name "Searcher"
            // If it does, click the parent element
            
            const characterContainers = document.querySelectorAll('[data-element-id="single-character-container"]');
            characterContainers.forEach(characterContainer => {
                const characterTitle = characterContainer.querySelector('[data-element-id="character-title"]');
                if (characterTitle.innerText.includes('Quick Searcher')) {
                    characterContainer.click();
                }
            });

            setTimeout(function() {
                // Get the search input
                const searchInput = document.querySelector('[data-element-id="chat-input-textbox"]'); // is a textarea

                // Press the "/" key to focus the search input
                window.dispatchEvent(
                    new KeyboardEvent("keydown", {
                        altKey: false,
                        code: "Slash",
                        ctrlKey: false,
                        isComposing: false,
                        key: "/",
                        location: 0,
                        metaKey: false,
                        repeat: false,
                        shiftKey: false,
                        which: 191,
                        charCode: 0,
                        keyCode: 191,
                    })
                );
                
                searchInput.textContent = decodedQuery;
                searchInput.dispatchEvent(new Event('input', { bubbles: true }));
                searchInput.dispatchEvent(new Event('change', { bubbles: true }));

                setTimeout(function(){
                    // Get the search button
                    const sendButton = document.querySelector('[data-element-id="send-button"]');

                    // Click the search button
                    sendButton.click();
                }, 250);

                console.log('Setting search input value to: ', searchInput.value)
            }, 3500); // YOU SHOULD PROBABLY CHANGE THIS! (Set to something like 500) I only have it this high so my other extensions have time to turn on streaming :) 
        }
    }, 500);
});