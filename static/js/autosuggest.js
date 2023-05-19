fetch('/static/species.csv')
  .then(response => response.text())
  .then(csvData => {
    const rows = csvData.split('\n');
    const speciesList = [];
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i].trim(); // Trim leading/trailing whitespaces
      if (row) {
        const columns = row.split(',');
        const speciesName = columns[1];
        speciesList.push(speciesName);
      }
    }
    populateSpeciesList(speciesList);
  })
  .catch(error => {
    console.error('Error loading CSV file:', error);
  });

function populateSpeciesList(speciesList) {
  const speciesInput = document.getElementById('speciesInput');
  const dataList = document.getElementById('speciesList');
  
  speciesList.forEach(species => {
    const option = document.createElement('option');
    option.value = species;
    dataList.appendChild(option);
  });
  
  speciesInput.addEventListener('input', function() {
    const inputValue = this.value;
    const fuzzyResults = fuzzysort.go(inputValue, speciesList);
    const filteredOptions = fuzzyResults.map(result => result.target);
    dataList.innerHTML = '';
    filteredOptions.forEach(option => {
      const newOption = document.createElement('option');
      newOption.value = option;
      dataList.appendChild(newOption);
    });
  });
}

// Define an array to store the selected species
let selectedSpecies = [];

// Function to add a species to the selectedSpecies array and display it
function addSpecies(species) {
    selectedSpecies.push(species);
    const selectedSpeciesDiv = document.getElementById('selectedSpecies');
    const speciesItem = document.createElement('div');
    speciesItem.textContent = species;
    selectedSpeciesDiv.appendChild(speciesItem);
}

document.addEventListener('DOMContentLoaded', function() {
    // Rest of your existing code here...

    // Add event listener to the form submission
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        // Get the number of questions and perform further actions...
        const numQuestionsInput = document.getElementById('num_questions');
        const numQuestions = parseInt(numQuestionsInput.value);
        // Rest of your logic to handle quiz start and species selection...
    });

    // Event listener for species selection
    const speciesInput = document.getElementById('speciesInput');
    speciesInput.addEventListener('change', function() {
        const selectedSpecies = speciesInput.value;
        if (selectedSpecies.trim() !== '') {
            addSpecies(selectedSpecies);
            speciesInput.value = '';
        }
    });
});
