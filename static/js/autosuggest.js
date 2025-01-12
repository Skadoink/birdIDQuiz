fetch('/static/species2024.csv')
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

// Define an array to store the selected species
let selectedSpecies = [];
hiddenSpeciesInpute = document.getElementById('selectedSpeciesInput');
if (hiddenSpeciesInpute.value) { // If there are already selected species
  selectedSpecies = hiddenSpeciesInpute.value.split(","); 
}
for (let i = 0; i < selectedSpecies.length; i++) {
  addSpecies(selectedSpecies[i]); // Add each hidden selected species to the display
}

function populateSpeciesList(speciesList) {
  const speciesInput = document.getElementById('speciesInput');
  const dataList = document.getElementById('speciesList');

  speciesList.forEach(species => {
    const option = document.createElement('option');
    option.value = species;
    dataList.appendChild(option);
  });

  speciesInput.addEventListener('input', function () {
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

// Function to add a species to the selectedSpecies array and display it
function addSpecies(species) {
  selectedSpecies.push(species);
  const selectedSpeciesDiv = document.getElementById('selectedSpecies');
  const speciesItem = document.createElement('div');
  speciesItem.textContent = species;
  selectedSpeciesDiv.appendChild(speciesItem);
  // Update the hidden input with the array as a comma-separated string
  document.getElementById('selectedSpeciesInput').value = selectedSpecies.join(',');
}

// Function to remove a species from the selectedSpecies array and update the display
function removeSpecies(species) {
  const index = selectedSpecies.indexOf(species);
  if (index !== -1) {
    selectedSpecies.splice(index, 1);
    const selectedSpeciesDiv = document.getElementById('selectedSpecies');
    selectedSpeciesDiv.removeChild(selectedSpeciesDiv.childNodes[index]);
  }
}

// // Add event listener to the form submission
// const form = document.querySelector('form');
// form.addEventListener('submit', function(event) {
//     event.preventDefault();
//     // Get the number of questions and perform further actions...
//     const numQuestionsInput = document.getElementById('num_questions');
//     const numQuestions = parseInt(numQuestionsInput.value);
//     // Rest of your logic to handle quiz start and species selection...
// });

// Event listener for species addition
const addSpeciesButton = document.getElementById('addSpeciesButton');
addSpeciesButton.addEventListener('click', function () {
  const inputSpecies = speciesInput.value.trim();
  if (inputSpecies !== '' && Array.from(speciesList.options).map(option => option.value).includes(inputSpecies) && !selectedSpecies.includes(inputSpecies)) {
    addSpecies(inputSpecies);
    speciesInput.value = '';
  }
  console.log(Array.from(speciesList.options).map(option => option.value));
});


// Event listener for species removal
const selectedSpeciesDiv = document.getElementById('selectedSpecies');
selectedSpeciesDiv.addEventListener('click', function (event) {
  const speciesItem = event.target;
  if (speciesItem.tagName === 'DIV') {
    const species = speciesItem.textContent;
    removeSpecies(species);
  }
});

