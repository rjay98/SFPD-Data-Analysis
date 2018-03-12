const handleSuccess = (data) => {
  if (data.hasOwnProperty('result')) {
    $('#result').text(data.result[1]);
  }
  else {
    $('#error').text(data.error);
  }
  $('#predict_button').text("Predict")
}

$(() => {
  $('div#process_input').bind('click', function() {
    var predict_dat = {
      "longitude": $('input[name="longitude"]').val(),
      "latitude": $('input[name="latitude"]').val(),
      "hour": $('input[name="hour"]').val(),
      "minute": $('input[name="minute"]').val(),
      "second": $('input[name="second"]').val(),
    };
    console.log(predict_dat)
    event.preventDefault();
    setTimeout(function() {
      $('#predict_button').text("Predicting...");
      $.getJSON('/predict_dispatch', predict_dat, handleSuccess)
    }, 500);
    $('#predict_button').text("Predict");
  });
});
