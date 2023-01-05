chrome.runtime.onMessage.addListener(
    async function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
    const t = document.getElementsByClassName("css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu")
    // const t = tweets.getElementsByClassName("css-1dbjc4n")
    tweets = []
    for(i=0;i<t.length;i++){
        const res = t[i].getElementsByClassName("css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0")
        const r = res[0].getElementsByClassName("css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")

        const h = t[i].getElementsByClassName("css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l")
        const m = h[0].getElementsByClassName("css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t")
        const l = m[0].getElementsByClassName("css-1dbjc4n r-18u37iz r-1q142lx")
        temp = []
        for(j=0;j<r.length;j++){
            temp.push(r[j].innerHTML)
        }
        tweets.push({"tweet_text": temp.join(" ")})
    }

    await fetch('http://127.0.0.1:5000/api/language-detection', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        },
    body: JSON.stringify(tweets)
    })
      .then(response => response.json())
      .then(response => {
        fetch('http://127.0.0.1:5000/api/sentiment-score', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(response)
        }).then(response => response.json())
        .then((response) => {
            console.log(response)
            updateDOM(t,response)
        })
      }
      )
    if (request.greeting === "hello")
        sendResponse({farewell: "goodbye"});
    }
  );


  function updateDOM(t,res){
    // console.log(t)
    for(k=0;k<t.length;k++){
        console.log(res[k]["detected_mood"])
        const h = t[k].getElementsByClassName("css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l")
        const m = h[0].getElementsByClassName("css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t")
        const l = m[0].getElementsByClassName("css-1dbjc4n r-18u37iz r-1q142lx")
        // console.log(l[0])
        if(res[k]["detected_mood"]=="POSITIVE"){
            const addEmoji = "<div class=\"css-1dbjc4n r-18u37iz r-1q142lx\"><span class=\"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0\">·</span><span class=\"css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0\"> Detected Mood: 😊</span> </div>"
            m[0].innerHTML = m[0].innerHTML + addEmoji
        }
        else if(res[k]["detected_mood"]=="NEUTRAL"){
            const addEmoji = "<div class=\"css-1dbjc4n r-18u37iz r-1q142lx\"><span class=\"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0\">·</span><span class=\"css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0\"> Detected Mood: 😐</span> </div>"
            m[0].innerHTML = m[0].innerHTML + addEmoji
        }else if(res[k]["detected_mood"]=="NEGATIVE"){
            const addEmoji = "<div class=\"css-1dbjc4n r-18u37iz r-1q142lx\"><span class=\"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0\">·</span><span class=\"css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0\"> Detected Mood: 🙁</span> </div>"
            m[0].innerHTML = m[0].innerHTML + addEmoji
        } else{
            const addEmoji = "<div class=\"css-1dbjc4n r-18u37iz r-1q142lx\"><span class=\"css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0\"></span> </div>" 
            m[0].innerHTML = m[0].innerHTML + addEmoji
        }
        
    }
  }