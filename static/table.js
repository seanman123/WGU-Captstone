/*
Used to add a class/css to the table returned from Python 
*/

$(document).ready(function() {
    var $dataTable = $('.data-table');

    $dataTable.addClass('table');
    $dataTable.find('th').css('text-align', 'left');

});