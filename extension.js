document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('status').textContent = "Extension loaded";
    document.getElementById('content').textContent = "Click on Load Tweets to detect mood of the tweets. For now, load tweets evertime you see new tweets in the tab (Takes 2-3 seconds to load)";
    var button = document.getElementById('permission');
    button.addEventListener('click', async function () {
        await chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
            const response = await chrome.tabs.sendMessage(tabs[0].id, {greeting: "Tweets Requested"});
            console.log(response)
        });
    });
});
