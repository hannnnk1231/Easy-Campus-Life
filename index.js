var send = document.getElementById("send");
var text = document.getElementById("text");
var workspace_title = document.getElementsByClassName('workspace_title');
var feed_title = document.getElementsByClassName('feed_title');
var channel_area = document.getElementsByClassName('sidebar__categories')[0];
var username = "iu2";
var profilename = "Dlwlrma"
var profileimg = `profileimg/${username}.jpg`;
var apigClient = apigClientFactory.newClient();

// Modal
var modal = document.getElementById("myModal");
var add_workspace = document.getElementsByClassName("plus")[0];
var span = document.getElementsByClassName("close")[0];
var modal_btn = document.getElementById("modal_btn");

add_workspace.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

modal_btn.onclick = function (e) {
  var w_name = document.getElementById("w_name");
  var w_id = document.getElementById("w_id");
  if ((w_id.value != "") & (w_name.value != "")){
    alert("Please choose from creating OR joining a workspace");
  } else if (w_name.value != ""){
    console.log("create workspace: ", w_name.value)
    msg = {
      "event": "create",
      "workspaceName": w_name.value,
      "username": username
    }
    apigClient.createWorkspacePost({},msg,{}).then((response) => {
          console.log(response);
          msg['w_id'] = response.data['body'];
          showWorkspaces([msg]);
          location.reload();
        })
        .catch((error) => {
          console.log('an error occurred', error);
        });
  } else if (w_id.value != ""){
    console.log('join workspace: ', w_id.value)
    msg = {
      "event": "join",
      "w_id": w_id.value,
      "username": username
    }
    apigClient.createWorkspacePost({},msg,{}).then((response) => {
          console.log(response);
          res = response.data['body']
          if (res != "success"){
            alert(res);
          } else {
            alert("Successfully join workspace");
            location.reload();
          }
        })
        .catch((error) => {
          console.log('an error occurred', error);
        });
  }

  w_name.value = "";
  w_id.value = "";
}

// Channel
var channels = document.getElementsByClassName("channel_name")

for (var i = 0; i < channels.length; i++){
  channels[i].onclick = function(e) {
    window.localStorage.setItem('channel', this.name);
    location.reload();
  }  
}

// Send Feed
send.onclick = function (e) {
  if (text.value != ""){
      msg = {
      "w_id": window.localStorage.getItem('w_id') || 0,
      "channel": window.localStorage.getItem('channel') || '',
      "username": username,
      "content": text.value,
      "time": new Date(),
    }
    apigClient.sendPost({},msg,{}).then((response) => {
          console.log(response);
          msg['profilename'] = profilename;
          msg['profileimg'] = profileimg;
          showFeeds([msg]);
        })
        .catch((error) => {
          console.log('an error occurred', error);
        });
    text.value = "";
  }
}

window.onload = function load() {
  w_title = window.localStorage.getItem('workspace') || ''
  w_id = window.localStorage.getItem('w_id') || -1
  f_title = window.localStorage.getItem('channel') || ''

  apigClient.getUserWorkspacesGet({"username":username},{},{}).then(function(result) {
    console.log('success OK');
    console.log(result)
    showWorkspaces(result.data);
    if (result.data.length>0){
      if (w_title=='') {
        w_title = result.data[result.data.length-1]['workspaceName']
        w_id = result.data[result.data.length-1]['w_id']
        f_title = "test"
        window.localStorage.setItem('workspace', w_title);
        window.localStorage.setItem('w_id', w_id)
        window.localStorage.setItem('channel', f_title);
      }
      workspace_title[0].insertAdjacentHTML('beforeend', `<span>${w_title}</span><p>id: # ${w_id}</p>`);
      feed_title[0].insertAdjacentHTML('afterbegin', `<h1>${f_title}</h1>`);
      var params = {
        "w_id": window.localStorage.getItem('w_id'),
        "channel": window.localStorage.getItem('channel')
      };
      apigClient.searchGet(params,{},{})
        .then(function (result) {
          console.log('success OK');
          showFeeds(result.data);
        }).catch(function (result) {
          console.log(result);
        });
      } else {
        channel_area.style.display = "none";
      }
  }).catch(function (result) {
    console.log(result);
    channel_area.style.display = "none";
  });
    
}

function showFeeds(res) {
  var d = document.getElementsByClassName("feeds__container")[0];
  for (var i = 0; i < res.length; i++) {
    console.log(res[i]);
    script = `<div class="feed">
            <div class="feeds-user-avatar">
              <img src="${res[i]['profileimg']}" alt="User 1" width="40" />
            </div>
            <div class="feed-content">
              <div class="feed-user-info">
                <h3>${res[i]['profilename']}<span class="time-stamp"> ${res[i]['time']}</span></h3>
              </div>
              <div>
                <span class="feed-text" style="white-space: pre-line">${res[i]['content']}</span>
              </div>
            </div>
          </div>
    `
    d.insertAdjacentHTML('beforeend', script);
  }
   d.scrollTop = d.scrollHeight;
}

function showWorkspaces(res) {
  var d = document.getElementsByClassName("sidebar")[0];
  for (var i = 0; i < res.length; i++) {
    console.log(res[i]);
    script = `<button type="button" class="box" name="${res[i]['workspaceName']}" id="${res[i]['w_id']}">${res[i]['workspaceName'][0]}</button>`
    d.insertAdjacentHTML('afterbegin', script);
  }
  d.scrollTop = d.scrollHeight;
  box = document.getElementsByClassName("box");
  for (var i = 0; i < box.length; i++){
    box[i].onclick = function(e) {
      window.localStorage.setItem('workspace', this.name);
      window.localStorage.setItem('w_id', this.id)
      window.localStorage.setItem('channel', "test");
      location.reload();
    }  
  }
}