// Updated local storage: TM_useUserProfiles, TM_useStateUpdateHistory, TM_useChatList, TM_useDeletedChatIDs, TM_useFolderList, 
// ... TM_useDeletedFolderIDs, TM_usePromptSettings, TM_useDeletedPromptIDs, TM_useDeletedCharacterIDs, TM_useHiddenModelIDs, 
// .. TM_useCustomModels, TM_useDefaultModel, TM_useModelIDsOrder
// Update IndexDB: TM_useUserCharacters, TM_useInstalledPlugins

function utf8_to_b64(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
}

// Get all values into a json object
var syncObj = {};

// Get all values from local storage
var keys = Object.keys(localStorage);
for (var i=0; i<keys.length; i++) {
    if (keys[i].startsWith("TM_")) {
        syncObj[keys[i]] = localStorage.getItem(keys[i]);
    }
}

var db = indexedDB.open("keyval-store");
db.onsuccess = function(event) {
    var db = event.target.result;
    var transaction = db.transaction("keyval", "readonly");
    var store = transaction.objectStore("keyval");

    var getAllKeys = store.getAllKeys();
    getAllKeys.onsuccess = function(event) {
        var keys = event.target.result;
        for (var i=0; i<keys.length; i++) {
            if (keys[i].startsWith("TM_")) {
                (function(key) {
                    var get = store.get(key);
                    get.onsuccess = function(event) {
                        syncObj[key] = event.target.result;
                    }
                })(keys[i]);
            }
        }
    }
}

// Send the object to the github repo

// Get token from cookies (GITHUB_TOKEN)
const token = document.cookie.split("; ").find(row => row.startsWith("GITHUB_TOKEN")).split("=")[1];
const owner = document.cookie.split("; ").find(row => row.startsWith("GITHUB_OWNER")).split("=")[1];
const repo = document.cookie.split("; ").find(row => row.startsWith("GITHUB_REPO")).split("=")[1];

// First, get the file to retrieve its sha
fetch(`https://api.github.com/repos/${owner}/${repo}/contents/typingmind.json`, {
    headers: {
        'Authorization': `Bearer ${token}`,
    },
})
.then(res => res.json())
.then(data => {
    // Then, update the file with its sha
    fetch(`https://api.github.com/repos/${owner}/${repo}/contents/typingmind.json`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: 'Update typingmind.json',
            content: utf8_to_b64(JSON.stringify(syncObj)),
            sha: data.sha // Include the sha in the request body
        })
    })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));
})
.catch(err => console.error(err));