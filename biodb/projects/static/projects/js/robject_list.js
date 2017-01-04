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

    // SEARCH/FILTER TOOLS
    // searching dropdown content hide/show logic 
    $(".filter-dropdown-toggle").click(function(event){
        var content = $(".filter-dropdown-content");
        
        if (content.is(":visible")){
            content.hide();
        }

        else {
            content.show();
            // possible thanks to tabindex tag attr
            content.focus();
            content.blur(function(){ 
                // blure dont concern button click or inputs inside dropdown menu
                if (!$(".filter-dropdown-toggle:hover").length &&
                    !$(".filter-dropdown-content *:hover").length){
                        content.hide();
                }
                // TODO: make dropdown-content visible afer click on search bar
            });
        }
    });
});