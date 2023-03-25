const username = document.getElementById('first_name');
const username2 = document.getElementById('last_name');
const email = document.getElementById("signUp_email");
const password = document.getElementById('signUp_password');
const signInEmail = document.getElementById('signIn_email');
const signInPassword = document.getElementById('signIn_password');
const companyPhone = document.getElementById('company_phone');
const companyName = document.getElementById('company_name');
const companyAddress = document.getElementById('company_address');
const branchPhone = document.getElementById('branch_update_phone');
const branchName = document.getElementById('branch_update_name');
const branchAddress = document.getElementById('branch_update_address');
const branchTitle = document.getElementById('branch_update_title');
const profilePhone = document.getElementById('profile_phone');
const additionalSignupEmail = document.getElementById('additional_signUp_email');
const additionalSignupFirstname = document.getElementById('additional_first_name');
const additionalSignupLastname = document.getElementById('additional_last_name');
const additionalSignupPassword = document.getElementById('additional_signUp_password');
const additionalSignupPhone = document.getElementById('additional_phone');
const resetPassword = document.getElementById('reset_new_password');
const new_company_name = document.getElementById('create_company_name');


// const itemPrice = document.getElementById('item_price');


function isvalidEmail(email) {
    let pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    return pattern.test(email);
}


const phonesInputs = [companyPhone, branchPhone, profilePhone, additionalSignupPhone, document.getElementById('new_item_price'), document.getElementById('new_combo_price')];

phonesInputs.forEach(element => {
    try {
        element.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9.]/g, "");
        });
    } catch (e) {

    }

});

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerHTML = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = element => {
    const inputControl = element.parentElement;

    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};


function isValidPassword(password) {
    const pattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&\-_])[A-Za-z\d@$!%*#?&\-_]{8,}$/;
    return pattern.test(password);
}


const sigInvalidateInputs = () => {

    const SignInValue = signInEmail.value.trim();
    const SignInPassValue = signInPassword.value.trim();

    if (SignInValue === '') {
        setError(signInEmail, 'Email is required');
        return false;
    } else if (!isValidEmail(SignInValue)) {
        setError(signInEmail, 'Provide a valid email address');
        return false;
    } else {
        setSuccess(signInEmail);
    }


    if (SignInPassValue === '') {
        setError(signInPassword, 'Password is required');
        return false;
    } else {
        setSuccess(signInPassword);
        return true;
    }
}


const sign_up_validation = () => {
    const usernameValue = username.value.trim();
    const usernameValue2 = username2.value.trim();
    const emailValue = email.value.trim();
    // const phoneValue = phone.value.trim();
    const passwordValue = password.value.trim();

    if (usernameValue === '') {
        setError(username, 'First name is required');
        return false;
    } else {
        setSuccess(username);
    }

    if (usernameValue2 === '') {
        setError(username2, 'Last Name is required');
        return false;
    } else {
        setSuccess(username2);
    }

    if (emailValue === '') {
        setError(email, 'Email is required');
        return false;
    } else if (!isvalidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
        return false;
    } else {
        setSuccess(email);
    }

    // if (phoneValue === '') {
    //     setError(phone, 'This field cannot be empty');
    //     return false;
    // } else if (phoneValue.length !== 11) {
    //     setError(phone, 'Should contain 11 number');
    //     return false;
    //
    // } else {
    //     setSuccess(phone);
    // }

    // else if (usernameValue.indexOf(" ") !== -1) {
    //     setError(username2, 'Last Name cannot contain spaces');
    //     return false;
    // }

    if (passwordValue === '') {
        setError(password, 'Password is required');
        return false;
    } else if (!isValidPassword(passwordValue)) {
        setError(password, 'Password should contain 8 characters with one uppercase , lowercase and character');
        return false;
    } else {
        setSuccess(password);
        return true;
    }
};


const companyValidation = () => {
    const companyPhoneValue = companyPhone.value.trim();
    const companyNameValue = companyName.value.trim();
    const companyAddressValue = companyAddress.value.trim();

    if (companyNameValue === '') {
        setError(companyName, 'Company name is required');
        return false;
    } else {
        setSuccess(companyName);
    }

    if (companyPhoneValue.length !== 11) {
        setError(companyPhone, 'Should contain 11 number');
        return false;

    } else if (companyPhoneValue === '') {
        setError(companyName, 'Field cannot be empty');
        return false;
    } else {
        setSuccess(companyPhone);
    }

    if (companyAddressValue === '') {
        setError(companyAddress, 'Company address cannot be empty');
        return false;
    } else {
        setSuccess(companyAddress);
        return true;
    }

}


const branchValidation = () => {

    const branchNameValue = branchName.value.trim();
    const branchAddressValue = branchAddress.value.trim();
    const branchTitleValue = branchTitle.value.trim();
    const branchPhoneValue = branchPhone.value.trim();

    if (branchNameValue === '') {
        setError(branchName, 'Field cannot be empty');
        return false;
    } else {
        setSuccess(branchName);
    }

    if (branchAddressValue === '') {
        setError(branchAddress, 'field cannot be empty');
        return false;
    } else {
        setSuccess(branchAddress);
    }

    if (branchTitleValue === '') {
        setError(branchTitle, 'field cannot be empty');
        return false;
    } else {
        setSuccess(branchTitle);
    }

    if (branchPhoneValue === '') {
        setError(branchPhone, 'field cannot be empty');
        return false;
    } else if (branchPhoneValue.length !== 11) {
        setError(branchPhone, 'Should contain 11 number');
        return false;
    } else {
        setSuccess(branchPhone);
        return true;
    }
}

const profileValidate = () => {
    const profilePhoneValue = profilePhone.value.trim();

    if (profilePhoneValue === '') {
        setError(profilePhone, 'field cannot be empty');
        return false;
    } else if (profilePhoneValue.length !== 11) {
        setError(profilePhone, 'Should contain 11 number');
        return false;
    } else {
        setSuccess(profilePhone);
        return true;
    }

}

const additionalSignupValidate = () => {
    const additionalEmailValue = additionalSignupEmail.value.trim();
    const additionalFirstnameValue = additionalSignupFirstname.value.trim();
    const additionalLastnameValue = additionalSignupLastname.value.trim();
    const additionalPasswordValue = additionalSignupPassword.value.trim();
    const additionalPhoneValue = additionalSignupPhone.value.trim();


    if (additionalEmailValue === '') {
        setError(additionalSignupEmail, 'Email is required');
        return false;
    } else if (!isvalidEmail(additionalEmailValue)) {
        setError(additionalSignupEmail, 'Provide a valid email address');
        return false;
    } else {
        setSuccess(additionalSignupEmail);
    }

    if (additionalFirstnameValue === '') {
        setError(additionalSignupFirstname, 'First name is required');
        return false;
    } else {
        setSuccess(additionalSignupFirstname);
    }

    if (additionalLastnameValue === '') {
        setError(additionalSignupLastname, 'Last Name is required');
        return false;
    } else if (additionalLastnameValue.indexOf(" ") !== -1) {
        setError(additionalSignupLastname, 'Last Name cannot contain spaces');
        return false;
    } else {
        setSuccess(additionalSignupLastname);
    }

    if (additionalPasswordValue === '') {
        setError(additionalSignupPassword, 'Password is required');
        return false;
    } else if (!isValidPassword(additionalPasswordValue)) {
        setError(additionalSignupPassword, 'Password should contain 8 characters with one uppercase , lowercase and character');
        return false;
    } else {
        setSuccess(additionalSignupPassword);
    }

    if (additionalPhoneValue === '') {
        setError(additionalSignupPhone, 'field cannot be empty');
        return false;
    } else if (additionalPhoneValue.length !== 11) {
        setError(additionalSignupPhone, 'Should contain 11 number');
        return false;
    } else {
        setSuccess(additionalSignupPhone);

        return true;
    }


}

const resetPassValidation = () => {

    const resetPassValue = resetPassword.value.trim();

    if (resetPassValue === '') {
        setError(resetPassword, 'Password is required');
        return false;
    } else if (!isValidPassword(resetPassValue)) {
        setError(resetPassword, 'Password should contain 8 characters with one uppercase , lowercase and character');
        return false;
    } else {
        setSuccess(resetPassword);
        return true;
    }
}
const create_company = () => {
    const company_name_value = new_company_name.value;
    if (company_name_value === '') {
        setError(new_company_name, 'Company name is required');
        return false;
    } else {
        setSuccess(new_company_name);
        return true;
    }
}
