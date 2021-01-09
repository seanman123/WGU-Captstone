// Used if the browser doesn't support the type "date" html

$(document).ready(function() {
    if ( $('#date')[0].type != 'date' ) {
        $("#date").datepicker({ dateFormat: 'yy-mm-dd', minDate: new Date(2020, 12, 1),});
    }
});