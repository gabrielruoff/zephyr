var form = document.getElementById("transactionform");
function handleForm(event) { event.preventDefault(); }
form.addEventListener('submit', handleForm);

var apiurl = "http://localhost:5000/pos/";

window.requestAnimationFrame =
           window.requestAnimationFrame ||
           window.mozRequestAnimationFrame ||
           window.webkitRequestAnimationFrame ||
           window.msRequestAnimationFrame;

var selectedticker = '';
var priceusd = '';
var txuid = '';
var value = '';

function dopretransaction(rxuid) {
  requestAnimationFrame(_showpromptforcard);

  txuid = get_uid_from_card(apiurl + rxuid);
  console.log(txuid);

  selectedticker = getselectedticker(apiurl + txuid);
  priceusd = getpriceusd(selectedticker);
  value = document.querySelector("#transactionValue").value;
  _showconfirmationprompt(value, priceusd, selectedticker);
}

function get_uid_from_card(url) {
  return api_request(url, 'uidfromcard', {}, false)['uid'];

};

function getselectedticker(url) {
  return api_request(url, 'getselectedticker', {}, false)['ticker'];
};

function dotransaction(txuid, rxuid) {
  value = document.getElementById("transactionValue").value;
  var body = {
    rxuid: rxuid,
    value: value,
  };
  return api_request(txuid, 'dotransaction', body);
};

function getpriceusd(selectedticker) {
  url = 'http://localhost:5000/data'
  var body = {
    assets: [selectedticker],
  };
  return api_request(url, 'getpriceusd', body, false)['prices'][selectedticker];
};

function _showpromptforcard() {
  form.classList.add('visually-hidden');
  promptforcard = document.querySelector("#promptforcard");
  promptforcard.classList.remove('visually-hidden');
};

function _showconfirmationprompt(value, priceusd, selectedticker) {
  console.log(value);
  console.log(priceusd);
  console.log(selectedticker);
  confirmationprompt = document.querySelector("#confirmationprompt");
  confirmationprompt.innerHTML = "<strong style='font-size: 25px'>Confirm transaction: $" + value + '</strong><br>(' + (value / priceusd).toString() + ' ' + selectedticker + ')';
  confirmationprompt.style.fontsize = '24px';
  confirmationprompt.style.fontweight = 'bold';
  confirmationprompt.classList.remove('visually-hidden');
};

  function api_request(url, method, body, async) {
  var json_data = {};
  var xhr = new XMLHttpRequest();
    if(async) {
          xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
          if (xhr.status == 200) {
            json_data = JSON.parse(xhr.responseText);
            console.log(json_data['data'])
            return json_data
          };
        };
      };
       xhr.open("POST", url, true);
          xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify({
        method: method,
        body: body
      }));
    } else {
      xhr.open("POST", url, false);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify({
        method: method,
        body: body
      }));
      return JSON.parse(xhr.responseText)['data'];
    }
}