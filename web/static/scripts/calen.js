function arrange_data(data){
	for (x = 0 ; x < data.length; x++){
		const option = $(`<option id="${data[x].id}" value="${data[x].id}">${data[x].name}</option>`)
		$('#neighborhood').append(option)
	}

}

function get_data(city){
	fetch(`http://localhost:5001/api/v1/city/${city}/neighborhood`)
	.then(response => {
		return response.json()
	})
	.then(data => {
		arrange_data(data)
	})
	.catch(err => {
		console.error(err)
	})
}


$(document).ready(function(){
	$('#city').on('change', function(){
		var city_id = $(this).val()
		if (city_id){
			choises = document.querySelector('#neighborhood')
			for (child of choises.children){
				if (child.textContent != "--Choose Neighborhood--"){
					child.parentElement.removeChild(child)
				}
			}
			get_data(city_id)
		}
	})
})
