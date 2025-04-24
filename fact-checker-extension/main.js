const loading = document.getElementById('loading')
const quoteElement = document.getElementById('resultElement')
const authorElement = document.getElementById('reasonElement')

const getQuotes = async (url) => {
    if(!url.includes('x.com')) {
      loading.innerHTML = `This is not twitter/x ` + url
      return;
    }  
    const ytId = url.replace('https://www.youtube.com/watch?v=', '');
    // Option 1: Using regex
    const match = url.match(/status\/(\d+)/);
    const tweetId = match ? match[1] : null;
    if (!tweetId) {
        loading.innerHTML = `This is not a tweet ` + url
        return;
    }

    loading.style.display = 'block'
    try {
        const res = await fetch(`http://127.0.0.1:5000/get-facts/${tweetId}`)
        const data = await res.json()
        loading.style.display = 'none'
        quoteElement.innerHTML = data.result ? data.result : 'no quotes found'
    } catch (error) {
        quoteElement.innerHTML = `oops... no qotes to show`
    }

}


// see the note below on how to choose currentWindow or lastFocusedWindow
chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
  let url = tabs[0].url;
  getQuotes(url)
  // use `url` here inside the callback because it's asynchronous!
});