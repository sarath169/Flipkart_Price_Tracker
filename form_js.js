//Global Variable
var API_BASE_URL='http://127.0.0.1:5000/';

function validate()
{
  var email = document.getElementById('email').value;
  var product_id=document.getElementById('pid').value;
  var threshold = document.getElementById('threshold').value;
  var mobile = document.getElementById('mobile').value;
  var email_checkbox = document.getElementById('email_checkbox').value;
  console.log(product_id);
  var mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  if (email_checkbox == 0){
  if(email == ""){
      document.getElementById('alert-email').innerHTML =" The email field can't be empty";
      document.getElementById('alert-email').style.color="red";
      return false;
    }
    if (email.match(mailformat)) {
        document.getElementById('alert-email').style.color="green";
        document.getElementById('alert-email').innerHTML ="Valid Email";
      }
      else
      {
        document.getElementById('alert-email').innerHTML =" Please enter a valid email";
        document.getElementById('alert-email').style.color="red";
        return false;
      }
    }
      if(product_id == ""){
          document.getElementById('alert-pid').innerHTML =" The product_id can't be empty";
          document.getElementById('alert-pid').style.color="red";

          return false;
        }
      else{
        document.getElementById('alert-pid').innerHTML =" Valid entry";
        document.getElementById('alert-pid').style.color="green";
      }
        if(threshold == ""){
            document.getElementById('alert-threshold').innerHTML =" The threshold can't be empty";
            document.getElementById('alert-threshold').style.color="red";
            return false;
          }
        else{
          document.getElementById('alert-threshold').innerHTML =" Valid entry";
          document.getElementById('alert-threshold').style.color="green";
        }
}
function reset_errors(){
  document.getElementById('alert-threshold').innerHTML="";
  document.getElementById('alert-email').innerHTML="";
  var dropdown = $('#pid');
  dropdown.prop('selectedIndex', 0);
  document.getElementById('alert-pid').innerHTML ="";
}
function populate(){
  var dropdown = $('#pid');
  dropdown.empty();
dropdown.append('<option selected=true disabled>Choose Product</option>');
dropdown.prop('selectedIndex', 0);
var url = `${API_BASE_URL}prod_details`;

var request = new XMLHttpRequest();
request.open('GET', url, true);
request.onload = function() {
  if (request.status === 200) {
    var data = JSON.parse(request.responseText);
    $.each(data, function (key, entry) {
      dropdown.append($('<option></option>').attr('value', entry[0]).text(entry[1]));
    });
  }
  else {
    console.log('Reached the server, but it returned an error');
  }
};
request.onerror = function() {
  console.error('An error occurred fetching the JSON from ' + url);
};
request.send();
}
function fillprice(){
  var pid=document.getElementById('pid').value;
  var interval = document.getElementById('interval').value;
  var url = `${API_BASE_URL}price_details/${pid}/${interval}`;
  console.log(url);
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.onload = function() {
    if (request.status === 200) {
      var data = JSON.parse(request.responseText);
      console.log(data);
      document.getElementById('latest_price').innerHTML ="Latest Price is "+data[0][0];
      document.getElementById('highest_price').innerHTML ="Highest Price is "+data[0][1];
      document.getElementById('lowest_price').innerHTML ="Lowest Price is "+data[0][2];
    }
    else {
      console.log('Reached the server, but it returned an error');
    }
};
request.onerror = function() {
  console.error('An error occurred fetching the JSON from ' + url);
};
request.send();
}
function email_alert(){
  var email_checkbox = document.getElementById('email_checkbox').value;
  console.log(email_checkbox);
  document.getElementById("mobile").style.display = "none";
  document.getElementById("email").style.display="block";

}
function mobile_alert(){
  var mobile_checkbox = document.getElementById('mobile_checkbox').value;
  console.log(mobile_checkbox);
  document.getElementById("mobile").style.display = "block";
  document.getElementById("email").style.display="none";
}
function both_alert(){
  var both = document.getElementById('both').value;
  console.log(both);
  document.getElementById("mobile").style.display = "block";
  document.getElementById("email").style.display="block";
}
function renderChart() {
    var ctx = document.getElementById("myChart").getContext('2d');
    var pid=document.getElementById('pid').value;
    var interval = document.getElementById('interval').value;
    var url = `${API_BASE_URL}plot_price/${pid}/${interval}`;
    console.log(url);
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
      if (request.status === 200) {
        var price_data = JSON.parse(request.responseText);
        var i=0;
        var data=[],labels=[];
        for (i=0;i<price_data.length;i++){
          data.join(price_data[i][0]);
          labels.join(price_data[i][1]);
        }
        // var myChart = new Chart(ctx, {
        //     type: '',
        //     data: {
        //         labels: labels,
        //         datasets: [{
        //             label: 'This week',
        //             data: data,
        //         }]
        //     },
        // });
//         var chart = new Chart(document.getElementById("myChart"), {
//     type: 'line',
//     data: data,
//     options: {
//         scales: {
//             xAxes: [{
//                 type: 'time',
//                 time: {
//                     unit: 'month'
//                 }
//             }]
//         }
//     }
// });
var x = new Chart(document.getElementById("myChart"), {
   type: 'scatter',
   data: {
      datasets: [{
         label: "Test",
         data: [{
            x: 0,
            y: 5
         }, {
            x: 5,
            y: 10
         }, {
            x: 8,
            y: 5
         }, {
            x: 15,
            y: 0
         }],
      }]
   },
   options: {
      responsive: true
   }
});
      }
      else {
        console.log('Reached the server, but it returned an error');
      }
  };
  request.onerror = function() {
    console.error('An error occurred fetching the JSON from ' + url);
  };
  request.send();

}
