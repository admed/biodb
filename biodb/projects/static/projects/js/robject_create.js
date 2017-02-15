$(function(){
// SCRIPT
    $(".delete-button").click(function(){
        // if only one .name-form dont delete  
        if($(".name-form").length > 1){
            $(this).parents(".name-form").remove()
        }
    })

    var name_form = $(".name-form").last().clone(true);
    name_form.find(".errorlist").remove();
    name_form.find("input[type=text]").val("");
    name_form.find("input[type=checkbox]").prop("checked", false);

    // create counter to store present largest form id 
    var id_counter = name_form.find("input[type=text]").attr("name").match(/\d+/)[0];
    id_counter = parseInt(id_counter,10);

    $(".add-button").click(function(){
        // increment id_counter 
        id_counter ++;
        // get id str        
        id = parseInt(id_counter,10) + "";
        // clone stored form
        form = name_form.clone(true);
        // modify form
        modifyForm(form = form, form_number = id);
        // append modified form to formset
        $(".name-forms").append(form);
    })

});