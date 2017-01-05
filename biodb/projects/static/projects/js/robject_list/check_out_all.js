// CHECK/CHECK OUT ALL ROBJECTS 
$(function(){
    $(".select-all").click(function(){
        if ($(this).is(":checked")){
            $(".select-robject").prop({"checked":true});
        }
        else {
            $(".select-robject").prop({"checked":false});
        }
    });
});