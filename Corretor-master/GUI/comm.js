$('#corrigir').on('click', () => {
	if($('#entrada').val()){
		$.post('', {entrada: $('#entrada').val()}, (possiveis) => {
			htmlLista = '';
			possiveis.forEach((possibilidade) => {
				htmlLista += `<li class="list-group-item">${possibilidade}</li>`;
			});
			$('#correcoes').html(htmlLista);
			$('.card').show();
		});
	}
});