window.onload = function search() {
  var apigClient = apigClientFactory.newClient();
  var params = {
    "workspace": "Cloud Computing",
    "channel": "test"
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
  
}