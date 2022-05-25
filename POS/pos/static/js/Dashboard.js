
var apiurl = "http://localhost:5000/pos/";


function dopretransaction(uid, selectedticker) {
  promptforcard = document.querySelector("#promptforcard")
  promptforcard.classList.remove('visually-hidden')
  uid = get_uid_from_card(uid, selectedticker)
  confirmationprompt = document.querySelector("#confirmationfprompt")
}

function get_uid_from_card(uid, ticker) {
  return api_request(uid, 'uidfromcard', {});

}

function dotransaction(txuid, rxuid) {
  value = document.getElementById("transactionValue").value;
  var body = {
    rxuid: rxuid,
    value: value,
  }
  return api_request(txuid, 'dotransaction', body)
}

  function api_request(uid, method, body) {
  var xhr = new XMLHttpRequest();
  url = apiurl + uid
  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    method: method,
    body: body
    }));
}