function get_athletes() {
  var sport_select = document.getElementById("id_sport");
  var gender_select = document.getElementById("id_gender");
  var age_select = document.getElementById("id_age");
  var athlete_select = document.getElementById("id_athletes");
  var official_select = document.getElementById("id_officials");

  // Show loading indicators for athletes and officials
  athlete_select.innerHTML = "<p>Loading athletes...</p>";
  official_select.innerHTML = "<p>Loading officials...</p>";

  // Fetch athletes for the selected sport, gender, and age using AJAX
  var sport_id = sport_select.value;
  var gender = gender_select.value;
  var age_id = age_select.value;

  // Fetch athletes
  fetch(`/get_athletes/?sport_id=${sport_id}&gender=${gender}&age_id=${age_id}`)
    .then((response) => response.json())
    .then((data) => {
      // Hide the loading indicator for athletes
      athlete_select.innerHTML = "";

      // Update the 'athlete' checkbox list with the fetched data
      if (data.athletes.length === 0) {
        athlete_select.innerHTML = "<p>No athletes found.</p>";
      } else {
        data.athletes.forEach((athlete) => {
          var div = document.createElement("div");
          var label = document.createElement("label");
          var input = document.createElement("input");
          input.type = "checkbox";
          input.value = athlete.id;
          input.name = "athletes"; // Ensure this is the correct name
          label.innerText = athlete.name;
          div.appendChild(input);
          div.appendChild(label);
          athlete_select.appendChild(div);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching athletes:", error);
      athlete_select.innerHTML =
        "<p>Error fetching athletes. Please try again.</p>";
    });

  // Fetch officials
}

// Attach the get_athletes function to the onchange events of the sport, gender, and age elements
document.getElementById("id_sport").onchange = get_athletes;
document.getElementById("id_gender").onchange = get_athletes;
document.getElementById("id_age").onchange = get_athletes;

// '''''''''''''''''''''''''''''''''''//-----------------------------------
// Assuming you have a form with the ID "your_form_id"
// Assuming you have a form with the ID "your_form_id"

function getOfficials() {
  // Show loading indicator for officials
  var officialSelect = document.getElementById("id_officials");
  officialSelect.innerHTML = "<option>Loading officials...</option>";

  // Fetch officials for the logged-in user using AJAX
  fetch("/get_officials/")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // Hide the loading indicator for officials
      officialSelect.innerHTML = "<option>-------</option>";

      // Update the 'official' dropdown list with the fetched data
      if (data.officials.length === 0) {
        officialSelect.innerHTML = "<option>No officials found.</option>";
      } else {
        data.officials.forEach((official) => {
          var option = document.createElement("option");
          option.value = official.id;
          option.innerText = official.name;
          officialSelect.appendChild(option);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching officials:", error);
      officialSelect.innerHTML =
        "<option>Error fetching officials. Please try again.</option>";
    });
}

function get_teams() {
  
}
// Call the getOfficials function when the page loads
// document.getElementById("id_athletes").onchange = getOfficials;
// document.addEventListener("DOMContentLoaded",
