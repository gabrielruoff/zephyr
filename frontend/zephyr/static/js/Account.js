/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  var datasets = [];
  console.log(data)
  var colors = ['#7eafec', '#f39564', '#b278f8'];
  var i = 0;
for(const [key, value] of Object.entries(data)) {
      datasets.push({
        label: key.toUpperCase(),
        data: value,
        lineTension: 0,
        // backgroundColor: [
        //         colors[i]
        //     ],
        borderColor: colors[i],
        borderWidth: 4,
        pointBackgroundColor: colors[i],
          pointStyle: 'rect',
      })
  i++;
        };


  // Graphs
    Chart.Legend.prototype.afterFit = function() {
    this.height = this.height + 20;
    this.padding = this.padding + 100;
};
    Chart.defaults.global.legend.labels.usePointStyle = true;
  var ctx = document.getElementById('balanceChart')
  // eslint-disable-next-line no-unused-vars
  var balanceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
        plugins: {
        },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
        title: {
            display: true,
            text: 'Wallets Over Time (%)'
        },
      legend: {
          display: true,
          position: 'top',
          align: 'start',
          maxwidth: 200,
            labels: {
                fontColor: '#333',
                font: {
                        size: 100,
                    style: 'bold',
                    },
            }
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
  var apiurl = "https://ccr-testbench:5000/Account/";
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