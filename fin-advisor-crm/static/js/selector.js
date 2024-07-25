function createDropdownOptions(selectElement, optionsData) {
  optionsData.forEach(optionText => {
    const option = document.createElement('option');
    option.text = optionText;
    option.value = optionText.toLowerCase();  // Adjust value setting as needed
    selectElement.appendChild(option);
  });
}

const selectElement = document.getElementById('mySelect');
const optionsData = ['One', 'Two', 'Three'];  // Replace with your data source

createDropdownOptions(selectElement, optionsData);

