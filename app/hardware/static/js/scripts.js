    $(document).ready(function() {
      $('#rackSelect').change(function() {
        var rackId = $(this).val();
        if (rackId) {
          $.ajax({
            url: '/rack/get_units/' + rackId,
            type: 'GET',
            success: function(response) {
              var units = response.units;
              $('#unitSelect').empty();
              $.each(units, function(index, unit) {
                $('#unitSelect').append('<option value="' + unit.id + '">' + unit.seq  + ' - ' + unit.name + '</option>');
              });
            }
          });
        } else {
          $('#unitSelect').empty();
        }
      });
    });