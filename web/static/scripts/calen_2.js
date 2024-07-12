/*
        {
        "__class__": "Clinic",
        "address": "mokattam Nafoura square",
        "address_id": "af4a08bf-3afd-4b28-aee6-416591c45018",
        "closing_time": "22:00",
        "created_at": "2024-07-03T17:30:54",
        "id": "d1e0bc11-dcd9-417c-b41d-19f62b20f60b",
        "name": "CalenDent",
        "neighborhood": "Mokattam",
        "neighborhood_id": "24c5690a-9f7d-4d3a-8289-48bb7f080cd0",
        "opening_time": "17:00",
        "updated_at": "2024-07-03T17:30:54",
        "user": "Omar Afifi",
        "user_id": "d6d66f4d-c69b-4a4c-891c-e3000a807a10",
        "visit_price": 250.0,
        "stars": "0"
    }
*/

$(document).ready(function () {
	  $('button.search').on('click', function () {
    const neighborhood_id = $('div.neighborhood input[name="neighborhood"]:checked').val();
    const owner = $('div.owner_search input[name="owner"]').val();
    if (!neighborhood_id) {
      alert('Choose Neighborhood Please');
    }
    if (neighborhood_id) {
      const query = `?owner=${encodeURIComponent(owner)}`;
      fetch(`https://www.dentistomarashraf.tech/api/v1/neighborhood/${neighborhood_id}/clinics${query}`)
        .then(response => {
          return response.json();
        })
        .then(data => {
          const doc_section = document.querySelector('section.doctor');
			  const to_dlt = [];
			  for (const child of doc_section.children) {
				  to_dlt.push(child);
			  }
			  for (const elm of to_dlt) {
				  elm.remove();
			  }
			  for (let x = 0; x < data.length; x++) {
				  const the_section_of_doctor = $('section.doctor');
				  const doc_cont = $('<div class="doctor_container"></div>');
				  const ph_cont = $('<div class="photo_container"></div>');
				  const inf_cont = $('<div class="info_container"></div>');
				  const rat_cont = $('<div class="rating_container"></div>');
				  const us_img = $('<img src="\'../../static/images/user.png">');
				  const name_cont = $('<div class="clinic_name"></div>');
				  const owner_cont = $('<div class="clinic_owner"></div>');
				  const address_cont = $('<div class="clinic_address"></div>');
				  const city_cont = $('<div class="clinic_city"></div>');
				  const neighbor_cont = $('<div class="clinic_neighborhood"></div>');
				  const aval_cont = $('<div class="clinic_aval"></div>');
				  const vis_cont = $('<div class="clinic_visit"></div>');
				  const icon_hosp = $('<i class="fa-solid fa-hospital"></i>');
				  const icon_own = $('<i class="fa-solid fa-user-doctor"></i>');
				  const icon_addr = $('<i class="fa-solid fa-location-pin"></i>');
				  const icon_neighbor = $('<i class="fa-solid fa-map-location"></i>');
				  const icon_city = $('<i class="fa-solid fa-city"></i>');
				  const icon_clock = $('<i class="fa-solid fa-clock"></i>');
				  const icon_dollar = $('<i class="fa-regular fa-dollar-sign"></i>');
				  const the_clinic = $(`<h4><b>${data[x].name}</b></h4>`);
				  const the_owner = $(`<h4>${data[x].user}</h4>`);
				  const the_address = $(`<h4>${data[x].address}</h4>`);
				  const the_city = $(`<h4>${$('.city h4').text()}</h4>`);
				  const the_neighbor = $(`<h4>${data[x].neighborhood}</h4>`);
				  const the_aval = $(`<h4><b>from ${data[x].opening_time} to ${data[x].closing_time}</b></h4>`);
				  const the_dollar = $(`<h4><b>${data[x].visit_price}</b></h4>`);
				  const the_rate = $(`<h1>${data[x].stars}</h1>`);
				  const url = `https://www.dentistomarashraf.tech/book?clinic_id=${data[x].id}`
				  const the_button = $(`<a class="reservation" href="${url}">Book</a>`);

				  doc_cont.append(ph_cont);
				  doc_cont.append(inf_cont);
				  doc_cont.append(rat_cont);
				  ph_cont.append(us_img);
				  inf_cont.append(name_cont);
				  inf_cont.append(owner_cont);
				  inf_cont.append(address_cont);
				  inf_cont.append(city_cont);
				  inf_cont.append(neighbor_cont);
				  inf_cont.append(aval_cont);
				  inf_cont.append(vis_cont);
				  rat_cont.append(the_rate);
				  rat_cont.append(the_button);
				  name_cont.append(icon_hosp);
				  name_cont.append(the_clinic);
				  owner_cont.append(icon_own);
				  owner_cont.append(the_owner);
				  address_cont.append(icon_addr);
				  address_cont.append(the_address);
				  city_cont.append(icon_city);
				  city_cont.append(the_city);
				  neighbor_cont.append(icon_neighbor);
				  neighbor_cont.append(the_neighbor);
				  aval_cont.append(icon_clock);
				  aval_cont.append(the_aval);
				  vis_cont.append(icon_dollar);
				  vis_cont.append(the_dollar);
				  the_section_of_doctor.append(doc_cont);
			  }
        })
        .catch(err => {
          console.error(err);
        });
    }
  });
});
