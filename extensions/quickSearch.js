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
                const span = document.getElementsByClassName('truncate max-w-[100px] sm:max-w-lg')[0];
                span.click();

                const modelListContainer = document.getElementsByClassName('absolute left-4 right-4 sm:right-auto sm:left-0 z-10 mt-2 sm:w-[380px] origin-top-right divide-y divide-gray-100 dark:divide-gray-700 rounded-md bg-white dark:bg-zinc-900 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none p-2 transform opacity-100 scale-100')[0];
                
                setTimeout(function() {
                    // Look through all children (and children of children...) and find "Anthropic: Claude 3 Haiku (self-moderated)"
                    const modelList = document.getElementsByClassName('truncate max-w-[180px]');
                    for (let i = 0; i < modelList.length; i++) {
                        const model = modelList[i];
                        if (model.innerText.includes('Anthropic: Claude 3 Haiku (self-moderated)')) {
                            model.click();
                        }
                    }

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

                    console.log('Setting search input value to: ', searchInput.value);
                }, 250);
            }, 500);
        }
    }, 500);
});