// Load the species list from hidden input
let allSpecies = document.getElementById('allSpeciesInput').value;
populateSpeciesList(allSpecies.split(','));

// Old code to load species list from CSV file
// fetch('/static/species2024.csv')
//   .then(response => response.text())
//   .then(csvData => {
//     const rows = csvData.split('\n');
//     const speciesList = [];
//     for (let i = 0; i < rows.length; i++) {
//       const row = rows[i].trim(); // Trim leading/trailing whitespaces
//       if (row) {
//         const columns = row.split(',');
//         const speciesName = columns[1];
//         speciesList.push(speciesName);
//       }
//     }
//     populateSpeciesList(speciesList);
//   })
//   .catch(error => {
//     console.error('Error loading CSV file:', error);
//   });

let selectedSpecies = []; // Array to store the selected species
hiddenSpeciesInput = document.getElementById('selectedSpeciesInput');
if (hiddenSpeciesInput.value) { // If there are already selected species (eg from a previous form submission)
  hiddenSpeciesInput.value.split(",").forEach(addSpecies); // Display the selected species
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

/**
 * Adds a species to the selectedSpecies array and display it
 * @param {string} species - The species to add (species name, not species code)
 *  */ 
function addSpecies(species) {
  selectedSpecies.push(species);
  const selectedSpeciesDiv = document.getElementById('selectedSpecies');
  const speciesItem = document.createElement('div');
  speciesItem.textContent = species;
  // Add remove button to each species item
  speciesItem.classList.add('selected-species-item');
  speciesItem.title = 'Click to remove';
  
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
    // Update the hidden input with the array as a comma-separated string
    document.getElementById('selectedSpeciesInput').value = selectedSpecies.join(',');
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

// Function to select a template and populate the form
function selectTemplate(templateId) {
  // Get templates from the hidden input
  const templatesData = document.getElementById('quizTemplatesData').value;
  const templates = JSON.parse(templatesData);
  
  // Get species code to name mapping from hidden input
  const speciesCodesData = document.getElementById('speciesCodesToNamesData').value;
  const speciesCodesToNames = JSON.parse(speciesCodesData);
  
  // Find the template by template ID
  const template = templates.find(t => t.id === templateId);
  if (!template || !template.species || template.species.length === 0) {
    console.warn('Template not found or has no species:', templateId);
    return;
  }

  // Clear existing selections
  selectedSpecies = [];
  document.getElementById('selectedSpecies').innerHTML = '';

  // Add each species from the template using the species codes
  template.species.forEach(speciesCode => {
    // Look up the species name using the code-to-name mapping
    const speciesName = speciesCodesToNames[speciesCode];
    
    if (speciesName) {
      addSpecies(speciesName);
    } else {
      console.warn('Species name not found for code:', speciesCode);
    }
  });
}

