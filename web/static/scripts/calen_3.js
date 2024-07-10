$(document).ready(function(){
	const api_url = "http://localhost:5001/api/v1/reservation/"
	$('div.rating_container a.confirmation_confirm').on('click', function(){
		const res_id = $(this).parent().parent().attr('id')
		const user_confirm = confirm("Are You Sure ?")
		if (user_confirm) {
			fetch(`${api_url}${res_id}?action=confirmed`)
			.then(data => {
				return data.json()
			})
			.then(data => {
				console.log(data)
				window.location.reload()
			})
			.catch(err => {
				console.error(err)
			})
		}
	})

	$('div.rating_container a.confirmation_decline').on('click', function(){
		const res_id = $(this).parent().parent().attr('id')
		const user_confirm = confirm("Are You Sure ?")
		if (user_confirm) {
                        fetch(`${api_url}${res_id}?action=declined`)
                        .then(data => {
                                return data.json()
                        })
                        .then(data => {
                                console.log(data)
				window.location.reload()
                        })
                        .catch(err => {
                                console.error(err)
                        })

		}
	})

        $('div.rating_container a.confirmation_delete').on('click', function(){
                const res_id = $(this).parent().parent().attr('id')
                const user_confirm = confirm("Are You Sure ?")
                if (user_confirm) {
                        fetch(`${api_url}${res_id}?action=delete`)
                        .then(data => {
                                return data.json()
                        })
                        .then(data => {
                                console.log(data)
                                window.location.reload()
                        })
                        .catch(err => {
                                console.error(err)
                        })

                }
        })
})
