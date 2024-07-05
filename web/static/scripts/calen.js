function arrange_data (data) {
  for (x = 0; x < data.length; x++) {
    const option = $(`<option id="${data[x].id}" value="${data[x].id}">${data[x].name}</option>`);
    $('#neighborhood').append(option);
  }
}

function get_data (city) {
  fetch(`http://localhost:5001/api/v1/city/${city}/neighborhood`)
    .then(response => {
      return response.json();
    })
    .then(data => {
      arrange_data(data);
    })
    .catch(err => {
      console.error(err);
    });
}

$(document).ready(function () {
  $('#city').on('change', function () {
    const city_id = $(this).val();
    if (city_id) {
      const choises = document.querySelector('#neighborhood');
      console.log(choises);
      const to_dlt = [];
      for (const child of choises.children) {
        if (child.textContent != '--Choose Neighborhood--') {
          to_dlt.push(child);
        }
      }
      for (const elem of to_dlt) {
	  elem.remove();
      }
      get_data(city_id);
    }
  });

  $('header').after().click(function () {
    window.location.href = 'http://localhost:5000';
  });

  $('input[name="city"]').on('change', function () {
    const choises = document.querySelector('.neighborhood_popover');
    const to_dlt = [];
    for (child of choises.children) {
      if (child.textContent != 'Choose neighborhood') {
        to_dlt.push(child);
      }
    }
    for (const elem of to_dlt) {
      elem.remove();
    }
    const city_id = $(this).val();
    fetch(`http://localhost:5001/api/v1/city/${city_id}/neighborhood`)
      .then(response => {
        return response.json();
      })
      .then(data => {
        for (x = 0; x < data.length; x++) {
          const list = $('<li class="radio_input"></li>');
          const input = $(`<input type="radio" name="neighborhood" value="${data[x].id}">`);
          const label = $(`<label for="neighborhood">${data[x].name}</label>`);
          list.append(input);
          list.append(label);
          $('.neighborhood_popover').append(list);
        }
      })
      .catch(err => {
        console.log(err);
      });
  });
  $('button.search').on('click', function () {
	  const neighborhood_id = $('div.neighborhood input[name="neighborhood"]:checked').val();
	  const owner = $('div.owner_search input[name="owner"]').val();
	  if (!neighborhood_id) {
		  alert('Choose Neighborhood Please');
	  }
	  if (neighborhood_id) {
		  const query = `?owner=${encodeURIComponent(owner)}`;
		  fetch(`http://localhost:5001/api/v1/neighborhood/${neighborhood_id}/clinics${query}`)
		  .then(response => {
			  return response.json();
		  })
		  .then(data => {
			  console.log(data);
		  })
		  .catch(err => {
			  console.error(err);
		  });
	  }
  });
});
