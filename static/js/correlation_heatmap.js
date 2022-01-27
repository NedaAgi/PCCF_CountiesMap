function selectedDataTypes(selector, economic_attributes, psychological_attributes) {

    var i;
    var attributes1 = [];
    var attributes2 = [];
    let selectedValue = selector.options[selector.selectedIndex].value;
    let form = document.getElementById('form');
    switch (selectedValue) {
        case "":
            form.setAttribute('style', 'display:none');
            break;
        case "economic":case "psychological": case "economic_psychological":
            form.setAttribute('style', 'display:block');
            switch (selectedValue){
                case "economic":
                    attributes1 = economic_attributes;
                    attributes2 = economic_attributes;
                    break;
                case "psychological":
                    attributes1 = psychological_attributes;
                    attributes2 = psychological_attributes;
                    break;
                case "economic_psychological":
                    attributes1 = economic_attributes;
                    attributes2 = psychological_attributes;
                    break;
            }
            break;
    }

    let attribute1_list = document.getElementById('attribute1_list');
    let attribute2_list = document.getElementById('attribute2_list');

    attribute1_list.innerHTML = "";
    attribute2_list.innerHTML = "";

    for (i = 0, length_i = attributes1.length; i < length_i; i += 1){
        str_attr1 = attributes1[i].split(",")[0] + "_1";
        attribute1_list.innerHTML += `<input type="checkbox" id=${str_attr1} name=${str_attr1} value=${attributes1[i]}>
                    <label for=${str_attr1}>${attributes1[i]}</label><br>
                    <hr>`
    }

    for (i = 0, length_i = attributes2.length; i < length_i; i += 1){
        str_attr2 = attributes2[i].split(",")[0] + "_2";
        attribute2_list.innerHTML += `<input type="checkbox" id=${str_attr2} name=${str_attr2} value=${attributes2[i]}>
                    <label for=${str_attr2}>${attributes2[i]}</label><br>
                    <hr>`
    }

    attribute1_list.innerHTML += `</div>`;
    attribute2_list.innerHTML += `</div>`;

}