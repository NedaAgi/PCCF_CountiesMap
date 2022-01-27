function selectedDataType(selector) {
     let selectedValue = selector.options[selector.selectedIndex].value;
     let form1 = document.getElementById('form1');
     let form2 = document.getElementById('form2');
     let form = document.getElementById('form');
     switch (selectedValue) {
        case "":
            form1.setAttribute('style', 'display:none');
            form.setAttribute('style', 'display:none');
            form2.setAttribute('style', 'display:none');
            break;
        case "economic":
            form1.setAttribute('style', 'display:block');
            form.setAttribute('style', 'display:block');
            form2.setAttribute('style', 'display:none');
            break;
        case "psychological":
            form1.setAttribute('style', 'display:none');
            form.setAttribute('style', 'display:block');
            form2.setAttribute('style', 'display:block');
            break;
     }
}

function displayAttributes(data_type) {
    if (data_type == 'economic') {
        let form_name = 'form1'
    }   else {
        let form_name = 'form2'
    }
    let form = document.getElementById(form_name)
    form.setAttribute('style', 'display:block')
}
