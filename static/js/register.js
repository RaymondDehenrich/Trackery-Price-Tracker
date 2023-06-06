function validateRegister(){
    let email = document.forms["register-input"]["register-email"].value;
    let username = document.forms["register-input"]["register-username"].value;
    let password = document.forms["register-input"]["register-password"].value;
    let confirmpassword = document.forms["register-input"]["register-confirmpassword"].value;
    let terms = document.forms["register-input"]["terms"].checked;
    let privacy = document.forms["register-input"]["privacy"].checked;
    if (username == "" || email == "" || password =="" || confirmpassword =="") {
        alert("Please fill in all fields");
        return false;
      }
    if (!terms || !privacy){
        alert("Please accept Terms and Privacy Policy");
        return false;
    }
    if(email.endsWith("@gmail.com")==false){
        alert("Invalid Email Address");
        return false;
    }
    if(password.length<5){
        alert("Password is too short\n");
        return false;
    }
    if(password!=confirmpassword){
        alert("Password and confirm password is not the same");
        return false;
    }
}
