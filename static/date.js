// Since this a future predictor, you need to pick a date in the future
// Also used if the browser doesn't support the type "date" html

$(document).ready(function() {
    var today = new Date(); 
    var day = today.getDate() + 1; 
    var month = today.getMonth() + 1; 
    var year = today.getFullYear(); 

    if (month < 10) {
        month = '0' + month; 
    }

    $('#date').attr("min",`${year}-${month}-${day}`);

    if ( $('#date')[0].type != 'date' ) {
        $("#date").datepicker({ dateFormat: 'yy-mm-dd', minDate: new Date(year, month, day),});
    }
});