let main_id;
function editeval(id,eval_type,eval_room,eval_information){
    document.getElementById("eval_type").value = eval_type;
    document.getElementById("eval_room").value = eval_room;
    document.getElementById("eval_information").value = eval_information;
    document.getElementById("eval_sub").value = id;
}

function validate_change_passwords() {
    password1 = document.getElementById("pass1").value;
    password2 = document.getElementById("pass2").value;
    old_password = document.getElementById("old_pass").value;
    if (password1 != password2) {
        passcheckerror.innerHTML = "Both the passwords are diferent";
        return false;
    } else {
        var val = passwordchecker(password1);
        var old_val = passwordchecker(old_password);
        if (!old_val) {
            passcheckerror.innerHTML =
                "Old Password is not having 8 characters with digits, letters and special characters";
            return false;
        }
        else if (!val) {
            passcheckerror.innerHTML =
                "New Password must have atleast 8 characters with digits, letters and special characters";
            return false;
        }
        return true;
    }
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
  