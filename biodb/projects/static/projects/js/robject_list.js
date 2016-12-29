$(function(){

    // CHECK/CHECK OUT ALL ROBJECTS 
    $(".select-all").click(function(){
        if ($(this).is(":checked")){
            $(".select-robject").prop({"checked":true});
        }
        else {
            $(".select-robject").prop({"checked":false});
        }
    });
});