//Global Variable
var API_BASE_URL='http://127.0.0.1:5000/';

function validate()
{
  var email = document.getElementById('email').value;
  var product_id=document.getElementById('pid').value;
  var threshold = document.getElementById('threshold').value;
  console.log(product_id);
  var mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

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
var url = API_BASE_URL+'prod_details';

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
