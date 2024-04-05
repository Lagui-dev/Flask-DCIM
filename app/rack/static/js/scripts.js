//
// UPDATE UNIT NAME in RACK/VIEW
//
$( document ).ready(function(){
	// $('.update_form').click(function(){
	$('.edit_name_unit').submit(function(e) {
		e.preventDefault();
		var formData = $(this);
		console.log(formData);

            // Sélectionner l'icône dans le formulaire soumis
            var arrowIcon = $(this).find('.bi-arrow-clockwise');
            var checkIcon = $(this).find('.bi-check');

            // Cacher l'icône de flèche et afficher l'icône de vérification
            arrowIcon.addClass('d-none');
            checkIcon.removeClass('d-none');

            // Désactiver le bouton
            $(this).find('button[type="submit"]').prop('disabled', true);
			$(this).find('button[type="submit"]').prop('title', 'Saved');

		$.ajax({
			url: '/rack/edit_unit',
			data: $(this).serialize(),
			type: 'POST',
			success: function (response) {
				console.log(response);
			},
			error: function (error) {
				console.log(error);
			}
		});
	});
});
//
//  REFRESH UNIT LIST WHEN FILTERING UNIT FILLED/NOT FILLED
//
// $(document).ready(function() {
//     $('#filter-filled').change(function(rack_id) {
//         var isFilled = $(this).val();
    function filterFilled(isFilled, rackId) {
        $.ajax({
            type: 'GET',
            url: '/rack/view/' + rackId,
            data: {'is_filled': isFilled},
            success: function(response) {
                $('#unit-container').html(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
// });

function filterUnitHardware() {
    var filterValue = document.getElementById('filter-filled').value;
    var cardUnits = document.querySelectorAll('.card-unit');

    cardUnits.forEach(function (cardUnit) {
        var cu = cardUnit.querySelector('.card-unit-hardware');
        var hasChildren = cu.childElementCount >0;
        if (filterValue === "") {
            cardUnit.style.display = 'block'; // Afficher tous les éléments
        } else if (filterValue === "true" && hasChildren) {
            cardUnit.style.display = 'block'; // Afficher si l'élément a des enfants
        } else if (filterValue === "false" && !hasChildren) {
            cardUnit.style.display = 'block'; // Afficher si l'élément n'a pas d'enfants
        } else {
            cardUnit.style.display = 'none'; // Masquer les autres éléments
        }
    });
}
