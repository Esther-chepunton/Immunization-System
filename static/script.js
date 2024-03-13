// static/scripts.js

document.addEventListener("DOMContentLoaded", function () {
  const immunizationForm = document.getElementById("immunization-form");
  immunizationForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(immunizationForm);
    fetch("/doctor", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        immunizationForm.reset();
      })
      .catch((error) => console.error("Error:", error));
  });

  fetch("/patient")
    .then((response) => response.json())
    .then((data) => {
      const immunizations = data.immunizations;
      const immunizationList = document.getElementById("immunization-list");
      const ul = document.createElement("ul");
      immunizations.forEach((immunization) => {
        const li = document.createElement("li");
        li.textContent = `Patient: ${immunization.patient_name}, Vaccine: ${immunization.vaccine_id}, Date: ${immunization.birth_date}`;
        ul.appendChild(li);
      });
      immunizationList.appendChild(ul);
    })
    .catch((error) => console.error("Error:", error));
});
