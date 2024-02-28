$(document).ready(function() {
          // When the country dropdown changes
          $('#country-dropdown').change(function() {
              // Get the selected country name
              var countryName = $(this).val();
              // Send a GET request to fetch the states of the selected country
              $.get('/states/' + countryName + '/', function(states) {
                  // Clear the current options in the state dropdown
                  $('#state-dropdown').empty();
                  // Add a default option to the state dropdown
                  $('#state-dropdown').append($('<option selected disabled>').text('-- Select State --'));
                  // Add each state of the selected country to the state dropdown
                  $.each(states, function(index, state) {
                      $('#state-dropdown').append($('<option>').text(state.state_name));
                  });
              });
          });



  // Function to make the AJAX request
  function fetchDashboardData() {
    fetch('/dashboard/') // Update the URL to your actual endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(data => {
        document.getElementById('total_domain_not_live').textContent = data.dashboard_data.total_domain_not_live;
        document.getElementById('total_domain_live_with_no_MX').textContent = data.dashboard_data.total_domain_live_with_no_MX;
        document.getElementById('total_amount_of_mx_data').textContent = data.dashboard_data.total_amount_of_mx_data;
        document.getElementById('total_amount_of_new_unverified_data').textContent = data.dashboard_data.total_amount_of_new_unverified_data;

      })
      .catch(error => console.error('Fetch error', error));
  }

  // Call the function when the page is loaded or when needed
  setInterval(fetchDashboardData,3000);

      });



