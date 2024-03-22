window.addEventListener('load', function() {
    // Wait 0.5 seconds for the page to load
    setTimeout(function() {
      // Function that updates localStorage based on button text (Simpler code thanks to @sagepourpre (krobs) on Discord)
      function updateStorage(key, newValue) {
        const oldValue = localStorage.getItem(key);
        localStorage.setItem(key, newValue); // Update local storage with new value
    
        // Create a new StorageEvent
        const storageEvent = new StorageEvent('storage', {
            key: key,
            oldValue: oldValue,
            newValue: newValue,
            url: window.location.href,
            storageArea: localStorage,
        });
    
        // Dispatch the event
        window.dispatchEvent(storageEvent);

        const span = document.getElementsByClassName('truncate max-w-[100px] sm:max-w-lg')[0];

        if (newValue === true) {
          span.style.color = 'green';
        }else if (newValue === false) {
          span.style.color = 'red';
        }
    }
      let overrideAutoStreaming = false;

      // get span by classes
      setInterval(() => {
        const span = document.getElementsByClassName('truncate max-w-[100px] sm:max-w-lg')[0];
        const buttonText = span.textContent;

        if (buttonText.includes('Wrapper') && !overrideAutoStreaming) {
          updateStorage("TM_useStreaming", false);
        }else if (!overrideAutoStreaming){
          updateStorage("TM_useStreaming", true);
        }
      }, 100);

      setInterval(() => {
        // check if button exists
        if (document.querySelector('[data-element-id="toggle-streaming-button"]')) {
          return;
        }

        // Add a quick enable/disable button for the streaming feature under data-element-id="current-chat-title"
        const enableAutoStreamingButton = document.createElement('button');
        enableAutoStreamingButton.textContent = 'Auto-Streaming';
        enableAutoStreamingButton.style.marginLeft = '10px';
        enableAutoStreamingButton.style.cursor = 'pointer';
        enableAutoStreamingButton.dataset.elementId = 'toggle-streaming-button';
        enableAutoStreamingButton.style.color = 'green';
        enableAutoStreamingButton.onclick = function() {
          // set the overrideAutoStreaming to opposite of current value
          if (overrideAutoStreaming) {
            overrideAutoStreaming = false;
            enableAutoStreamingButton.style.color = 'green'
          } else {
            overrideAutoStreaming = true;
            enableAutoStreamingButton.style.color = 'red'
          }
        };

        // Add a quick enable/disable button for the streaming feature under data-element-id="current-chat-title"
        const currentChatTitle = document.querySelector('[data-element-id="current-chat-title"]');
        const button = document.createElement('button');
        button.textContent = 'Streaming';
        button.style.marginLeft = '10px';
        button.style.cursor = 'pointer';
        button.dataset.elementId = 'toggle-streaming-button';
        button.onclick = function() {
          const useStreaming = localStorage.getItem('TM_useStreaming') === 'true';
          updateStorage('TM_useStreaming', !useStreaming);
          overrideAutoStreaming = true;
          enableAutoStreamingButton.style.color = 'red';

          if (!useStreaming) {
            button.style.color = 'green';
          } else {
            button.style.color = 'red';
          }
        };

        // Append after first child (as second element) but before the current second element
        const child = currentChatTitle.children[1];
        
        // Create one div to hold both buttons
        child.appendChild(button);
        child.appendChild(enableAutoStreamingButton);

      }, 500)
    }, 500);
  });
  