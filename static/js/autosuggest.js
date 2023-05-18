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
    const inputValue = this.value.toLowerCase();
    const filteredOptions = speciesList.filter(species => species.toLowerCase().startsWith(inputValue));
    dataList.innerHTML = '';
    filteredOptions.forEach(option => {
      const newOption = document.createElement('option');
      newOption.value = option;
      dataList.appendChild(newOption);
    });
  });
}
