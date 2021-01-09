/*
Used to scroll to prediction box when form is submitted 
*/
$(document).ready(function() {
    if ($(".prediction-box").length){
        $(document).scrollTop( $(".prediction-box").offset().top );
    }
});