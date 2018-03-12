$(() => {$('.zipcode-select').bind('click', (e) => {
  event.preventDefault();
  const zipcode = $(event.target).attr('value')
  apiCall(zipcode);
})})

const apiCall = (zipcode) => {
  const url = '/zip_statistics/' + zipcode
  $('#zipcode').text(zipcode);
  $.ajax({
    method: 'GET',
    url: url,
    success: successHandler
  })
}

const successHandler = (data) => {
  if (data.hasOwnProperty('total_incidents')) {
    $('#total_incidents').text(data.total_incidents);
    $('#incidents_per_day').text(data.incidents_per_day);
    $('#average_response_time').text(data.average_response_time);
    $('#percent_emergencies').text(data.percent_emergencies + '%');
  }
  else {
    $('#error').text(data.error);
  }
}