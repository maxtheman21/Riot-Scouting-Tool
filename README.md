# League of Legends Scouting Tool

## Overview

This is a Python-based scouting tool for **League of Legends** designed to analyze previous games from college teams. The tool takes a college with it's 5 starting players and organizes the champions into an image.

## Features

- **Player Data Aggregation**: Fetch the champions played in each 5 roles.
- **Statistical Analysis**: Process and summarize key performance metrics such as rank, win rates, champion pool, and more.
- **Visualization**: Automatically generate an image that consolidates the statistics of all team members into a clean and readable format.

## Requirements

- Python 3.8+
- Riot Games API Key
- The following Python libraries:
  - `requests`
  - `Pillow`
  - `json`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maxtheman21/Riot-Scouting-Tool.git
   cd Riot-Scouting-Tool
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Obtain a Riot Games API key from [Riot Developer Portal](https://developer.riotgames.com/) and add it to a creds.py file:

## Usage

1. Ensure all example files are updated to your specifications.

2. Change the JSON for previous games and update the list of players.

3. The tool will fetch data, process it, and generate an output image in the `output/` directory.

## Output Example

The generated image includes:
- Player names and solo queue ranks
- Champions played in their position
- Wins and losses
- More coming soon

## Troubleshooting

- **API Errors**: Ensure your Riot API key is valid and not expired.
- **Empty Output**: Check if the summoner names are spelled correctly and exist in the given region.
- **Library Issues**: Ensure all dependencies are installed and compatible with your Python version.

## Acknowledgments

- Riot Games for providing the API
- The Python community for the libraries that make this project possible

---

Feel free to suggest additional features or report bugs in the [Issues](https://github.com/maxtheman21/Riot-Scouting-Tool/issues) section of the repository.

