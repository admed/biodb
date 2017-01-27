$(function(){
    console.log("add_remove_buttons.js loaded")
    $("#add_button").click(function(){
        $("#add_input").prop('checked', true);
    })
    $("#remove_button").click(function(){
        $("#remove_input").prop('checked', true);
    })
});

