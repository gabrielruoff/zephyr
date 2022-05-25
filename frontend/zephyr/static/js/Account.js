/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById('balanceChart')
  // eslint-disable-next-line no-unused-vars
  var balanceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()

function set_selected_ticker(username, ticker) {
  api_request(username, 'setselectedticker', {selectedticker: ticker})
  // var xhr = new XMLHttpRequest();
  // url = "http://localhost:5000/Account/" + username
  // xhr.open("POST", url, true);
  // xhr.setRequestHeader('Content-Type', 'application/json');
  // xhr.send(JSON.stringify({
  //   method: 'setselectedticker',
  //   body: {
  //     selectedticker: ticker
  //   }
  // }));

  var old_container = document.querySelector("#" + oldticker)
  var old_button = document.querySelector("#" + oldticker + "button")
  old_container.classList.remove('border')
  old_button.classList.remove("btn-primary")
  old_button.classList.add("btn-secondary")
  old_button.textContent = "Spend"

  var selected_container = document.querySelector("#" + ticker)
  var selected_button = document.querySelector("#" + ticker + "button")
  selected_container.classList.add('border')
  selected_container.classList.add('border-info')
  selected_button.classList.remove("btn-secondary")
  selected_button.classList.add("btn-primary")
  selected_button.textContent = "Spending"
  // selected_button.onclick = set_selected_ticker(username, ticker)

  oldticker = ticker
}

  function api_request(uid, method, body) {
  var xhr = new XMLHttpRequest();
  apiurl + uid
  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    method: method,
    body: body
    }));
}