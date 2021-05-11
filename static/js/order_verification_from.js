var verify_box = document.getElementById("checkbox1");
var delivered = document.getElementById("checkbox2");
var payment_done = document.getElementById("checkbox3");

function myFunction() {

  verify_box.removeAttribute('disabled','disabled');
  delivered.removeAttribute('disabled','disabled');
  payment_done.removeAttribute('disabled','disabled');

  if (verify_box.checked == true && delivered.checked == true && payment_done.checked == true) {
      verify_box.setAttribute('disabled','disabled');
      delivered.setAttribute('disabled','disabled');
      payment_done.setAttribute('disabled','disabled');

      console.log('case1')


    
  }


  else if (verify_box.checked == true && delivered.checked == true && payment_done.checked == false) {
      verify_box.setAttribute('disabled','disabled');
      delivered.setAttribute('disabled','disabled');
      console.log('case2')

    
  }

  else if (verify_box.checked == false && delivered.checked == false && payment_done.checked == false){
    delivered.setAttribute('disabled','disabled');
    payment_done.setAttribute('disabled','disabled');
    console.log('case3')

    // verification is first step
    
  } 
  else if (verify_box.checked == true && delivered.checked == false && payment_done.checked == false) {
      verify_box.setAttribute('disabled','disabled');
      payment_done.setAttribute('disabled','disabled');
      console.log('case4')


    
  }



    


};

[verify_box,delivered,payment_done].forEach(item => item.addEventListener('change',
  (event)=>{

    myFunction()
    



  }));
myFunction();
$('#my_form').submit(function(){
    $("#my_form :disabled").removeAttr('disabled');
});














