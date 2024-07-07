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
    $('.city h4').text($(this).attr("class"))
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
          const input = $(`<input type="radio" name="neighborhood" value="${data[x].id}" class="${data[x].name}">`);
          const label = $(`<label for="neighborhood">${data[x].name}</label>`);
          list.append(input);
          list.append(label);
          $('.neighborhood_popover').append(list);
	  $('input[name="neighborhood').on('change', function (){
	    $('.neighborhood h4').text($(this).attr("class"))
	  })
        }
      })
      .catch(err => {
        console.log(err);
      });
  });
});
