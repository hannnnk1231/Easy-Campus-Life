var send = document.getElementById("send");
var text = document.getElementById("text");
var workspace_title = document.getElementsByClassName('workspace_title')
var username = "Dlwlrma"
var userimg = "iu2.jpeg"
var apigClient = apigClientFactory.newClient();

var box = document.getElementsByClassName("box");

for (var i = 0; i < box.length; i++){
  box[i].onclick = function(e) {
    window.localStorage.setItem('workspace', this.name);
    window.localStorage.setItem('channel', "test");
    location.reload();
  }  
}


send.onclick = function (e) {
  if (text.value !== ""){
      msg = {
      "workspace": window.localStorage.getItem('workspace') || 'Cloud Computing',
      "channel": window.localStorage.getItem('channel') || 'test',
      "username": username,
      "userimg": userimg,
      "content": text.value,
      "time": new Date(),
    }
    apigClient.sendPost({},msg,{}).then((response) => {
          console.log(response);
          showFeeds([msg]);
        })
        .catch((error) => {
          console.log('an error occurred', error);
        });
    text.value = "";
  }
}

window.onload = function load() {
  title = window.localStorage.getItem('workspace') || 'Cloud Computing'
  workspace_title[0].insertAdjacentHTML('beforeend', `<span>${title}</span>`);
  var params = {
    "workspace": window.localStorage.getItem('workspace') || 'Cloud Computing',
    "channel": window.localStorage.getItem('channel') || 'test'
  };
  apigClient.searchGet(params,{},{})
    .then(function (result) {
      console.log('success OK');
      showFeeds(result.data);
    }).catch(function (result) {
      console.log(result);
    });
}

function showFeeds(res) {
  var d = document.getElementsByClassName("feeds__container");
  for (var i = 0; i < res.length; i++) {
    console.log(res[i]);
    script = `<div class="feed">
            <div class="feeds-user-avatar">
              <img src="${res[i]['userimg']}" alt="User 1" width="40" />
            </div>
            <div class="feed-content">
              <div class="feed-user-info">
                <h3>${res[i]['username']}<span class="time-stamp"> ${res[i]['time']}</span></h3>
              </div>
              <div>
                <span class="feed-text" style="white-space: pre-line">${res[i]['content']}</span>
              </div>
            </div>
          </div>
    `
    d[0].insertAdjacentHTML('beforeend', script);
  }
   d[0].scrollTop = d[0].scrollHeight;
}