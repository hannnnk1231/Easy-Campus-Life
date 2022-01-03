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

var back_btn = document.getElementById("back");

back_btn.onclick = function() {
  window.location.href = "http://easy-campus-react-front-host.s3-website-us-east-1.amazonaws.com/Easy-Campus-Life/index.html?username="+username;
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
  apigClient.eventGet({"username":username},{},{}).then(function(result) {
    console.log("Got info for: ", username, "info", result.data)
    showEvents(result.data)
  }).catch(function (result) {
    console.log(result);
  });
}


function showEvents(res) {
  var d_r = document.getElementsByClassName("event_r")[0];
  var d_all = document.getElementsByClassName("event_all")[0];
  script_r = `<div class="event_container">
            <div class="event_header">
              <h1>${res.recommend.name}</h1>
              <button class="event_register_btn" name="${res.recommend.id}">Register</button>
            </div>
            <div class="event_content">
              <img src="${res.recommend.img}">
              <div class="event_text">
                <p>${res.recommend.content}</p>
              </div>
              <div class="event_detail">
                <h2>Host</h2>
                <p>${res.recommend.host}</p>
                <h2>Date</h2>
                <p>${res.recommend.date}</p>
                <h2>Time</h2>
                <p>${res.recommend.time}</p>
                <h2>Location</h2>
                <p >${res.recommend.location}</p>
                <h2>Contact</h2>
                <p>${res.recommend.contact}</p>
                <h2>Cost</h2>
                <p>${res.recommend.cost}</p>
              </div>
            </div>
          </div>
  `
  d_r.insertAdjacentHTML('beforeend', script_r);
  for (var i = 0; i < res.all.length; i++) {
    script = `<div class="event_container">
            <div class="event_header">
              <h1>${res.all[i].name}</h1>
              <button class="event_register_btn" name="${res.all[i].id}">Register</button>
            </div>
            <div class="event_content">
              <img src="${res.all[i].img}">
              <div class="event_text">
                <p>${res.all[i].content}</p>
              </div>
              <div class="event_detail">
                <h2>Host</h2>
                <p>${res.all[i].host}</p>
                <h2>Date</h2>
                <p>${res.all[i].date}</p>
                <h2>Time</h2>
                <p>${res.all[i].time}</p>
                <h2>Location</h2>
                <p >${res.all[i].location}</p>
                <h2>Contact</h2>
                <p>${res.all[i].contact}</p>
                <h2>Cost</h2>
                <p>${res.all[i].cost}</p>
              </div>
            </div>
          </div>
    `
    d_all.insertAdjacentHTML('beforeend', script);
  }

  btn = document.getElementsByClassName("event_register_btn");
  for (var i = 0; i < btn.length; i++){
    btn[i].onclick = function(e) {
      msg = {
        "e_id": this.name,
        "username": username,
      }
      apigClient.registerEventPost({},msg,{}).then((response) => {
        console.log(response)
        alert(response.data.body);
      })
      .catch((error) => {
        console.log('an error occurred', error);
      });
    }  
  }
}

// Modal
var modal = document.getElementById("myModal");
var add_event = document.getElementById("create_event_btn");
var span = document.getElementsByClassName("close")[0];
var modal_btn = document.getElementById("modal_btn");

add_event.onclick = function() {
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
  var e_name = document.getElementById("e_name");
  var e_img = document.getElementById("e_img");
  var e_content = document.getElementById("e_content");
  var e_host = document.getElementById("e_host");
  var e_date = document.getElementById("e_date");
  var e_time = document.getElementById("e_time");
  var e_location = document.getElementById("e_location");
  var e_contact = document.getElementById("e_contact");
  var e_cost = document.getElementById("e_cost");

  msg = {
    "e_name": e_name.value,
    "e_img": e_img.value,
    "e_content": e_content.value,
    "e_host": e_host.value,
    "e_date": e_date.value,
    "e_time": e_time.value,
    "e_location": e_location.value,
    "e_contact": e_contact.value,
    "e_cost": e_cost.value
  }

  apigClient.eventPost({},msg,{}).then((response) => {
        console.log(response);
        alert("Successfully create event");
        location.reload();
      })
      .catch((error) => {
        console.log('an error occurred', error);
      });

  e_name.value = "";
  e_img.value = "";
  e_content.value = "";
  e_host.value = "";
  e_date.value = "";
  e_time.value = "";
  e_location.value = "";
  e_contact.value = "";
  e_cost.value = "";

}