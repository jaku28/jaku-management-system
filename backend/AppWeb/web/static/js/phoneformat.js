$(document).ready(function () {
  var phoneInputID = "#phone_number";
  var input = document.querySelector(phoneInputID);
  var iti = window.intlTelInput(input, {
    formatOnDisplay: true,
    hiddenInput: "full",
    preferredCountries: ["pe"],
    autoHideDialCode: true,
    nationalMode: false,
    separateDialCode: true,
    utilsScript:
      "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.14/js/utils.js",
  });

  $(phoneInputID).on("countrychange", function (event) {
    var selectedCountryData = iti.getSelectedCountryData();
    let code_number =  iti.getSelectedCountryData().dialCode;
    (newPlaceholder = intlTelInputUtils.getExampleNumber(
      selectedCountryData.iso2,
      true,
      intlTelInputUtils.numberFormat.INTERNATIONAL
    )),
      

    mask = "+"+code_number+" " + newPlaceholder.replace(/[1-9]/g, "0");
    $(this).mask(mask);
  });

  iti.promise.then(function () {
    $(phoneInputID).trigger("countrychange");
    
  });
  // document.getElementById("phone_number").addEventListener("change", (e) =>{
    // let full_number = iti.getNumber();
    // console.log(full_number);
    // let number = document.getElementById("phone_number");
    // number.value = full_number;
    // let code_number =  iti.getSelectedCountryData().dialCode;
    // let full_number = "+"+code_number+" "+number;
    // number = full_number;
    // console.log(number);
  // })
});

