function toggleInputType() {
    const div1 = document.getElementsByClassName('input-location-block')[0];
    const div2 = document.getElementsByClassName('input-location-block')[1];
    const button1 = document.getElementsByClassName('input-button-block')[0];
    const button2 = document.getElementsByClassName('input-button-block')[1];
    const input_city_name = document.querySelector('input[name="city_name"]');
    const input_latitude = document.querySelector('input[name="latitude"]');
    const input_longitude = document.querySelector('input[name="longitude"]');

    if (div1.classList.contains('dark-overlay')) {
      div1.classList.remove('dark-overlay');
      div2.classList.add('dark-overlay');
      button1.classList.remove('light-dark-overlay');
      button2.classList.add('light-dark-overlay');
      input_latitude.value = '';
      input_longitude.value = '';
    } else {
      div2.classList.remove('dark-overlay');
      div1.classList.add('dark-overlay');
      button2.classList.remove('light-dark-overlay');
      button1.classList.add('light-dark-overlay');
      input_city_name.value = '';
    }
}