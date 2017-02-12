$(function(){
    // CREATE DATEPICKER AND SET DATE FORMAT
    $(".date-input").datepicker({ 
        dateFormat: 'dd-mm-yy',
        onClose: function(d,i) {$(".filter-dropdown-content").focus()}   
    });
});