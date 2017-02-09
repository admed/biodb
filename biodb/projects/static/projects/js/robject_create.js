$(function(){
// SCRIPT
    $(".delete-button").click(function(){
        $(this).parents(".name-form-content").detach()
    })

    var name_form = $(".name-form").first().clone(true);
    name_form.find("input[type=text]").val("");
    name_form.find("input[type=checkbox]").prop("checked", false);

    $(".add-button").click(function(){
        // get number of forms in formset 
        var form_number = $("#id_name-TOTAL_FORMS").val();
        // increment form_number        
        form_number = parseInt(form_number,10) + 1 + "";
        // set incremented form_number 
        $("#id_name-TOTAL_FORMS").val(form_number);
        // clone name_form
        form = name_form.clone(true);
        // $(".formset").append(name_form.clone(true));
        modifyForm(form = form, form_number = form_number-1);
        // append modified form to formset
        $(".formset").append(form);
    })

// MODULE

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
});