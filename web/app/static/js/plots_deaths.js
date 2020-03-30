function showMainChart(country) {
    $.ajax({
        url: '/plot/country/deaths/' + country,
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('graph', JSON.parse(data) );
        }
    });
}

function refreshExponentialGrowthTable(country) {
    $('#exponential').bootstrapTable('refresh', {url: '/exponential/country/deaths/' + country});
}

function updateTable(country) {
    $.ajax({
        url: '/information/country/deaths/' + country,
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        dataType:"json",
        success: function (data) {
            $('#table-percentage-population').text(data['percentage_of_population']);
            $('#last-run-at').text(data['last_run_at']);
            $('#total-country').text(data['total_per_country']);
            $('#cfr').text(data['cfr']);
        }
    });
}
$(document).ready(function() {
    showMainChart("Brazil");
    updateTable('Brazil')
    // move it to a method
    $('.dropdown-item').click(function(e){
        country = $(this).data('country');
        $('#country-title').text('Deaths Statistics for ' + country);
        showMainChart(country);
        refreshExponentialGrowthTable(country);
        updateTable(country);
        e.preventDefault();
    })
});