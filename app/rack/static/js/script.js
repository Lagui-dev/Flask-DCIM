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