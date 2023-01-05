document.addEventListener('DOMContentLoaded', function() {
    // document.getElementById('status').textContent = "Extension loaded";
    var button = document.getElementById('permission');
    button.addEventListener('click', async function () {
        await chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {

            const response = await chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"});
            console.log(response)
        });
    });
});
