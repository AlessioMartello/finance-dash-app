document.onreadystatechange = hideSpinner

function hideSpinner (){
  var state = document.readyState;
  if (state == 'complete') {
      setTimeout(hide
      ,1000);
  }
}

function hide (){
    document.getElementById("spinner-div").classList.add('hidden');
}
