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
    }
  
      // get span by classes
      setInterval(() => {
        const span = document.getElementsByClassName('truncate max-w-[100px] sm:max-w-lg')[0];
        const buttonText = span.textContent;

        if (buttonText.includes('Wrapper')) {
          updateStorage("TM_useStreaming", false);
        }else{
          updateStorage("TM_useStreaming", true);
        }
      }, 100);
    }, 500);
  });
  