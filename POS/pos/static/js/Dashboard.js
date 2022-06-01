var form = document.getElementById("transactionform");
function handleForm(event) { event.preventDefault(); }
form.addEventListener('submit', handleForm);

var apiurl_local = "http://localhost:5000/pos/";
var apiurl_remote_account = "https://ccr-testbench:5000/Account/";
var apiurl_remote_transactions = "https://ccr-testbench:5000/Transactions/";

var txuid = "";
var value = "";
var priceusd = "";

window.requestAnimationFrame =
           window.requestAnimationFrame ||
           window.mozRequestAnimationFrame ||
           window.webkitRequestAnimationFrame ||
           window.msRequestAnimationFrame;


function dopretransaction() {
  requestAnimationFrame(_showpromptforcard);
  listen_for_card_read();

}

function listen_for_card_read(stop=false) {
  if(!stop) {
    var listeninterval = window.setInterval(function () {
      txuid = retrievereaderdata();
      // console.log(txuid);
      if(parseInt(txuid) != 0) {
        // console.log('retrieving data');
        clearInterval(listeninterval);
        _hidepromptforcard();
        _showconfirmationprompt(txuid);
      }
    }, 400);
  } else {
    clearInterval(listeninterval)
  }
}

function _showconfirmationprompt(txuid) {
  value = parseFloat(document.querySelector("#transactionValue").value);
  let selectedticker = getselectedticker(txuid);
  priceusd = getpriceusd(selectedticker);
  confirmationprompt = document.querySelector("#confirmationprompt");
  confirmationprompt.innerHTML = "<strong class=\"mt-5\" style=\"font-size: 30px\">" +
      "Confirm Transaction:" +
      "</strong>" +
      "<span>" +
      "<p class=\"mt-4\" style=\"font-size: 30px\">" +
      "$" + value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ", paying with " +
      "<img src=\"/static/img/"+ selectedticker + "-logo.png\" alt=\"{{ imgname }}\" style=\"width: 100px; height: auto; margin: auto\">" +
      "</p>" +
      "</span>" +
      "<br>" +
      "<p class=\"mt-3\" style=\"font-size: 17px; font-style: italic;\">" +
      "(" + (value / priceusd).toString() + ' <strong>' + selectedticker.toUpperCase() + '</strong>)' +
      '</p>' +
      "<button type=\"button\" id=\"yesbutton\" class='btn btn-success m-3' style='width: 100px; height: auto' onClick=\"dotransaction()\">" +
      "Yes</button>" +
      "<div id=\"yesspinner\" class='spinner-border text-secondary visually-hidden m-3' role=\"status\">" +
      "<span class=\"sr-only mb-5\"></span>" +
      "</div>" +
      "<button type=\"button\" id='nobutton' class='btn btn-danger m-3' style='width: 100px; height: auto' onClick=\"reset_page()\">" +
      "No" +
      "</button>";

  confirmationprompt.style.fontsize = '24px';
  confirmationprompt.style.fontweight = 'bold';
  confirmationprompt.classList.remove('visually-hidden');
};

function _hideconfirmationprompt() {
  confirmationprompt = document.querySelector("#confirmationprompt");
  confirmationprompt.classList.add('visually-hidden');
};

function reset_page() {
  window.location.reload();
}

function getselectedticker(txuid) {
  let url = apiurl_remote_account + txuid;
  let body = {
    'userid': txuid,
  }
  return api_request(url, 'getselectedticker', body, false)['selectedticker'];
};

function dotransaction() {
  var showspinner = window.setTimeout(_showconfirmationwaitspinner,1);
  let url = apiurl_remote_transactions + txuid
  let body = {
    txuserid: txuid,
    rx: rxuid,
    value: (value / priceusd)
  };
  let tx_id = api_request(url, 'dotransaction', body)['tx_id'];
  _hideconfirmationprompt();
_showfarewellconfirmation(tx_id);
};

function getpriceusd(selectedticker) {
  let url = 'http://localhost:5000/data'
  let body = {
    assets: [selectedticker],
  };
  return api_request(url, 'getpriceusd', body, false)['prices'][selectedticker];
};

function retrievereaderdata() {
  let url = apiurl_local + '0';
  let data = api_request(url, 'retrievereaderdata', {}, false)['read'];
  return data;
};

function _showpromptforcard() {
  form.classList.add('visually-hidden');
  let promptforcard = document.querySelector("#promptforcard");
  promptforcard.classList.remove('visually-hidden');
};

function _showconfirmationwaitspinner() {
    let yesbutton = document.querySelector("#yesbutton");
  let nobutton = document.querySelector("#nobutton");
let yesspinner = document.querySelector("#yesspinner");
  yesbutton.classList.add('visually-hidden');
  nobutton.classList.add('visually-hidden');
  yesspinner.classList.remove('visually-hidden');
};

function _hidepromptforcard() {
  let promptforcard = document.querySelector("#promptforcard");
  promptforcard.classList.add('visually-hidden');
};

function _showfarewellconfirmation(txid) {
  let farewellconfirmation = document.querySelector("#farewellconfirmation");
  let farewellconftxid = document.querySelector("#farewellconftxid");
  farewellconftxid.textContent = "receipt #" + txid;
  farewellconfirmation.classList.remove('visually-hidden');
};

  function api_request(url, method, body, async) {
  var xhr = new XMLHttpRequest();
    if(async) {
          xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
          if (xhr.status == 200) {
            let json_data = JSON.parse(xhr.responseText);
            // console.log(json_data['data'])
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
      let json_data = JSON.parse(xhr.responseText);
      // console.log(json_data['data']);
      return json_data['data'];
    }
}