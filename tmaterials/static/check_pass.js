function validate_passwords() {
  password1 = document.getElementById("pass1").value;
  password2 = document.getElementById("pass2").value;
  if (password1 != password2) {
    passcheckerror.innerHTML = "Both the passwords are diferent";
    return false;
  } else {
    var val = passwordchecker(password1);
    if (!val) {
      passcheckerror.innerHTML =
        "Password must have atleast 8 characters with digits, letters and special characters";
      return false;
    }
    return true;
  }
}

function validate_passwaord_letters() {
  password1 = document.getElementById("pass1").value;
    var val = passwordchecker(password1);
    if (!val) {
      passcheckerror.innerHTML =
        "Password must have atleast 8 characters with digits, letters and special characters";
      return false;
    }
    return true;
}

function passwordchecker(str) {
  if (
    (str.match(/[a-z]/g) || str.match(/[A-Z]/g)) &&
    str.match(/[0-9]/g) &&
    str.match(/[^a-zA-Z\d]/g) &&
    str.length >= 8
  )
    return true;
  return false;
}
