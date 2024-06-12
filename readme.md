# DOM Analysis Script

## Overview

This Python script fetches the HTML content from a specified URL, analyzes the DOM structure, and outputs detailed information into a single Excel file with multiple sheets. The analysis includes counts of common HTML tags, attributes, CSS classes, and IDs, as well as general information about the DOM structure.

## Features

- Fetches HTML content from a specified URL.
- Analyzes the DOM structure to gather various metrics.
- Outputs the analysis into a multi-sheet Excel file.
- Provides counts for common HTML tags, attributes, CSS classes, and IDs.
- Generates a summary of the analysis in the first sheet of the Excel file.

## Requirements

- Python 3.x
- Required Python packages: \`requests\`, \`beautifulsoup4\`, \`pandas\`, \`openpyxl\`

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `config.json` file in the project directory with the following structure:

```
{
    "url": "https://example.com/"
}
```

Replace "https://example.com." with the URL you want to analyze.

## Usage

Run the script to analyze the DOM and generate the output file:

```python dom_explorer.py```

The script will generate an Excel file named based on the URL and timestamp, containing the analysis results.

## Example Output

The Excel file will contain the following sheets:
- **DOM Analysis Info**: Summary information about the DOM structure.
- **Common Tags**: Counts of the most common HTML tags.
- **Attributes Count**: Counts of the most common attributes.
- **Common CSS Classes**: Counts of the most common CSS classes.
- **Common IDs**: Counts of the most common IDs.
- **All CSS Classes**: List of all CSS classes and their counts.
- **All IDs**: List of all IDs and their counts.

## License

This project is licensed under the MIT License.
