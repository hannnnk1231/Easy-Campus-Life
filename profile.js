var apigClient = apigClientFactory.newClient();

// Get username
function GetURLParameter(sParam){
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split('&');
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParameterName = sURLVariables[i].split('=');
    if (sParameterName[0] == sParam) {
        return sParameterName[1];
    }
  }
}

var username = GetURLParameter('username');
var originUsername = GetURLParameter('originuser');

var back_btn = document.getElementById("back");

back_btn.onclick = function() {
  window.location.href = "http://easy-campus-react-front-host.s3-website-us-east-1.amazonaws.com/Easy-Campus-Life/index.html?username="+originUsername;
}

var event_icon = document.getElementById("event_icon");
event_icon.onclick = function() {
  window.location.href = "http://easy-campus-react-front-host.s3-website-us-east-1.amazonaws.com/Easy-Campus-Life/event.html?username="+username;
}

var account_icon = document.getElementById("account_icon") 
account_icon.onclick = function(){
  window.location.href = "http://easy-campus-react-front-host.s3-website-us-east-1.amazonaws.com/readProfile";
}

window.onload = function load() {
  apigClient.getUserWorkspacesGet({"username":username, "event": "info"},{},{}).then(function(result) {
    console.log("Got info for: ", username, "info", result.data)
    showUser(result.data)
  }).catch(function (result) {
    console.log(result);
  });
}


function showUser(res) {
  var d = document.getElementsByClassName("card-container")[0];
  script = `<h1>Profile</h1>
        <div class="profile-pic-div">
          <img src="https://easycampusreactv20f8fa0a551e84b23b27048be4f0649145029-dev.s3.amazonaws.com/public/${res['username']}.jpg" id="photo">
        </div>
        <h2>${res['displayName']}</h2>
        <h2>Education</h2>
        <p>${res['education']}</p>
        <h2>Experience</h2>
        <p>${res['experience']}</p>
        <h2>Activities</h2>
        <p>${res['activities']}</p>
      </div>
  `
  console.log(script)
  d.insertAdjacentHTML('beforeend', script);
}