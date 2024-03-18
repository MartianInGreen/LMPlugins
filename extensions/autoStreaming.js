window.addEventListener('load', function() {
    // Wait 0.5 seconds for the page to load
    setTimeout(function() {
      // Function that updates localStorage based on button text
      function updateLocalStorageBasedOnText(content) {
        const containsWrapper = content.includes('Wrapper');
        const currentUseStreaming = localStorage.getItem('TM_useStreaming');
  
        if (containsWrapper && currentUseStreaming === 'true') {
          console.log('containsWrapper', containsWrapper);
          const settingsButton = document.querySelector('[data-element-id="settings-button"]');
          settingsButton.click();
  
          setTimeout(function() {
            // find the right button
            containerClass = document.getElementsByClassName('absolute right-0 w-60 top-10 z-10 mt-2 origin-top-left rounded-md bg-[color:var(--popup-color)] shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none p-2 transform opacity-100 scale-100')[0];
  
            // go through each child button to find the one with the "Preferences" text
            for (let i = 0; i < containerClass.children.length; i++) {
              if (containerClass.children[i].textContent === 'Preferences') {
                containerClass.children[i].click();
                break;
              }
            }
  
            setTimeout(function() {
              const streamingButton = document.querySelector('[data-element-id="plugins-switch-enabled"]');
              streamingButton.click();
  
              // Click the escape key
              window.dispatchEvent(
                new KeyboardEvent("keydown", {
                  altKey: false,
                  code: "Escape",
                  ctrlKey: false,
                  isComposing: false,
                  key: "Escape",
                  location: 0,
                  metaKey: false,
                  repeat: false,
                  shiftKey: false,
                  which: 27,
                  charCode: 0,
                  keyCode: 27,
                })
              );
            }, 500);
          }, 500);
          
        } else if (!containsWrapper && currentUseStreaming === 'false') {
          console.log('containsWrapper', containsWrapper);
          const settingsButton = document.querySelector('[data-element-id="settings-button"]');
          settingsButton.click();
  
          setTimeout(function() {
            // find the right button
            containerClass = document.getElementsByClassName('absolute right-0 w-60 top-10 z-10 mt-2 origin-top-left rounded-md bg-[color:var(--popup-color)] shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none p-2 transform opacity-100 scale-100')[0];
  
            // go through each child button to find the one with the "Preferences" text
            for (let i = 0; i < containerClass.children.length; i++) {
              if (containerClass.children[i].textContent === 'Preferences') {
                containerClass.children[i].click();
                break;
              }
            }
  
            setTimeout(function() {
              const streamingButton = document.querySelector('[data-element-id="plugins-switch-disabled"]');
              streamingButton.click();
  
              // Click the escape key
              window.dispatchEvent(
                new KeyboardEvent("keydown", {
                  altKey: false,
                  code: "Escape",
                  ctrlKey: false,
                  isComposing: false,
                  key: "Escape",
                  location: 0,
                  metaKey: false,
                  repeat: false,
                  shiftKey: false,
                  which: 27,
                  charCode: 0,
                  keyCode: 27,
                })
              );
  
            }, 500);
          }, 500);
          
        }
      }
  
      // get span by classes
      setInterval(() => {
        const span = document.getElementsByClassName('truncate max-w-[100px] sm:max-w-lg')[0];
        const buttonText = span.textContent;

        updateLocalStorageBasedOnText(buttonText);
        observer.disconnect();

        // Creating a MutationObserver to observe changes in the button
        const observer = new MutationObserver((mutations) => {
          mutations.forEach((mutation) => {
            if (mutation.type === 'childList' || mutation.type === 'characterData') {
              const newTextContent = mutation.target.textContent;
              updateLocalStorageBasedOnText(newTextContent);
            }
          });
        });

        // Configuration of the observer:
        const config = { childList: true, characterData: true, subtree: true };

        // Pass in the target node, as well as the observer options
        observer.observe(span, config);
      }, 2000);
    }, 500);
  });
  