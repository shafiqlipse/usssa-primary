function get_age() {
  var date_of_birth_select = document.getElementById("id_date_of_birth");
  var age_select = document.getElementById("id_age"); // Make sure this ID matches the one in your HTML

  // Show a loading indicator for ages
  age_select.innerHTML = "<option disabled selected>Loading age...</option>";

  console.log("Selected date_of_birth:", date_of_birth_select.value);

  // Fetch ages for the selected date_of_birth using AJAX
  var date_of_birth = date_of_birth_select.value;
  if (!date_of_birth) {
    console.error("Date of birth is undefined or empty");
    return;
  }

  fetch(`/calculate_age_choices/?date_of_birth=${date_of_birth}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch age choices");
      }
      return response.json();
    })
    .then((data) => {
      // Log the received data for debugging
      console.log("Received data:", data);

      // Hide the loading indicator
      age_select.innerHTML = "";

      // Log the received data for debugging
      console.log("Received data:", data);

      // Update the 'age' dropdown with the fetched data
      if (data && data.ages && data.ages.length > 0) {
        data.ages.forEach((ageArray) => {
          var option = document.createElement("option");
          option.value = ageArray[0]; // Use the first element as the value
          option.text = ageArray[1]; // Use the second element as the text
          age_select.add(option);
        });
      } else {
        console.error("No valid age data found in the response:", data);
        // Optionally, you can clear the dropdown or handle the absence of data in another way
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      // Update the 'age' dropdown with an error message
      age_select.innerHTML =
        "<option disabled selected>Error loading ages</option>";
    });
}
