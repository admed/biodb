$(function(){
    // uncheck both inputs, just in case
    $("#add_input").prop('checked', false);
    $("#remove_input").prop('checked', false);

    // check inputs after click
    $("#add_button").click(function(){
        $("#add_input").prop('checked', true);
    })
    $("#remove_button").click(function(){
        $("#remove_input").prop('checked', true);
    })
});

