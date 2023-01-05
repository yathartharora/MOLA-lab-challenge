chrome.runtime.onMessage.addListener(
    // console.log(tweets)
    function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
    console.log(request)
    const t = document.getElementsByClassName("css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu")
    // const t = tweets.getElementsByClassName("css-1dbjc4n")
    for(i=0;i<t.length;i++){
        // console.log(t[i])
        const res = t[i].getElementsByClassName("css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0")
        const r = res[0].getElementsByClassName("css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
        for(j=0;j<r.length;j++){
            console.log(r[j].innerHTML)
        }
    }
      if (request.greeting === "hello")
        sendResponse({farewell: "goodbye"});
    }
  );