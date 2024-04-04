//
// GET LIST OF UNITS FROM A RACK
//
$(document).ready(function () {
    $('#rack').change(function () {
        var rackId = $(this).val();
        if (rackId) {
            $.ajax({
                url: '/rack/get_units/' + rackId,
                type: 'GET',
                success: function (response) {
                    var units = response.units;
                    $('#unit').empty();
                    $.each(units, function (index, unit) {
                        var unitText = unit.seq + (unit.name ? ' - ' + unit.name : '');
                        $('#unit').append('<option value="' + unit.id + '">' + unitText + '</option>');
                    });
                }
            });
        } else {
            $('#unit').empty();
        }
    });
});