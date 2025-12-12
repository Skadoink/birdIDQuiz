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

/**
 * Toggles the accordion panel for the given quiz templates section
 * Seabird (sb), Shorebird (sh), Seabird Advanced (sba), Shorebird Advanced (sha)
 * @param {*} key section key, one of 'sb', 'sh', 'sba', 'sha' 
 */
function toggleSection(id) {
    const section = document.getElementById(id);
    const chevron = document.getElementById("chevron-" + id);
    const container = section.closest(".accordion-item");
    
    const allSections = document.querySelectorAll(".accordion-content");
    const allChevrons = document.querySelectorAll(".accordion-chevron");

    const isOpening = section.style.maxHeight === "0px" || !section.style.maxHeight;

    // STEP 1 — close all other sections first
    allSections.forEach(s => {
        if (s.id !== id) {
            s.style.maxHeight = "0px";
        }
    });
    allChevrons.forEach(c => {
        if (c.id !== "chevron-" + id) {
            c.classList.remove("rotate-180");
        }
    });

    if (!isOpening) {
        // Closing the currently opened section — no scroll needed
        section.style.maxHeight = "0px";
        chevron.classList.remove("rotate-180");
        return;
    }

    // STEP 2 — wait for the collapse animations to finish
    // Typically matches CSS close transition: 200ms
    setTimeout(() => {
        // STEP 3 — open the clicked section
        section.style.maxHeight = section.scrollHeight + "px";
        chevron.classList.add("rotate-180");

        // STEP 4 — THEN scroll it into view cleanly
        setTimeout(() => {
            container.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }, 50);
    }, 200); // match close animation duration
}
