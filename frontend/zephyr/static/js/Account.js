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
  var xhr = new XMLHttpRequest();
  url = "http://localhost:5000/Account/" + username
  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    method: 'setselectedticker',
    body: {
      selectedticker: ticker
    }
  }));

//   url = "http://localhost:5000/Account/" + username
//   xhr.open("POST", url, true);
//   xhr.setRequestHeader('Content-Type', 'application/json');
//   xhr.send(JSON.stringify({
//     method: 'getsupportedtickers',
//     body: {
//
//     }
//   }));
//   if (xhr.readyState == 4)
//     if (xhr.status == 200)
//       var json_data = JSON.parse(request.response);
//
// json_data.forEach((element) => {
//   var container = document.getElementById(element)
//   container.className = 'col-sm'
//   })
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
