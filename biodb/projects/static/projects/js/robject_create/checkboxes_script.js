define(function(){
    $("input[type=checkbox]").click(function(){
        $("input[type=checkbox]").prop("checked", false);
        $(this).prop("checked", true);
    });
})
