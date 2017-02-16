define(function(){
    /**
       Modify any input founded in given container.
    */
    function modifyForm(form, form_number){
        // find all inputs inside form
        var inputs = form.find("input");

        // pass any input to modifyInput
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            modifyInput(input=input, attrs=["id", "name"], form_number=form_number);
        }
    }

    /**
        Modify input's attributes listed in attrs (by replace number in attr string).
    */
    function modifyInput(input, attrs, form_number) {
        
        for(var i = 0; i < attrs.length; i++) {
            // grab attr
            var attr = $(input).attr(attrs[i]);
            // modify number in attr str
            var new_attr = attr.replace(/[0-9]+/, form_number);
            // replace attr
            $(input).attr(attrs[i], new_attr);
        }
    }
    return {
        modifyForm:modifyForm,
        // modifyInput:modifyInput
    }
});