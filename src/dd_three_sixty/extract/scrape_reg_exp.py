import argparse
import requests
import re
import json
import datetime
from bs4 import BeautifulSoup
from unicodedata import normalize


def scrape_weather_data(city):
    url = f"https://www.meteored.mx/{city}/historico"
    run_identifier = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_folder = f"/data/raw_data/{city}/"

    try:
        # Send a GET request to the URL with a timeout of 5 seconds
        response = requests.get(url, timeout=5)

        # Get the HTML content from the response
        html = response.text

        # Define the regular expressions for value extraction
        value_pattern = re.compile(r'<td class="columna_datos"><span.*?>(.*?)</span>')

        # Parse the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Find the table
        table = soup.find("table", id="tabla_actualizacion")

        # Find all the table rows
        rows = table.find_all("tr")

        # Prepare the data to be saved in JSON
        data = {
            "run_identifier": run_identifier,
            "request_url": url,
            "response_code": response.status_code,
            "requested_data": [],
        }

        # Iterate over each row
        for row in rows:
            # Find the cells in each row
            cells = row.find_all("td")

            # Extract the value from each cell
            for i in range(1, len(cells), 2):
                value_match = re.search(value_pattern, str(cells[i]))
                if value_match:
                    name = normalize("NFKD", cells[i - 1].text.strip()).encode("ASCII", "ignore").decode("utf-8")
                    value = normalize("NFKD", value_match.group(1)).encode("ASCII", "ignore").decode("utf-8")
                    data["requested_data"].append({"name": name, "value": value})

        # Save the data as JSON
        with open(f"{json_folder}{run_identifier}_response.json", "w") as file:
            json.dump(data, file, indent=4)

        print(f"Response saved to {json_folder}{run_identifier}_response.json")

    except Exception as error:
        # Prerrorpare the data for exception case
        data = {
            "run_identifier": run_identifier,
            "request_url": url,
            "response_code": None,
            "requested_data": [],
            "error_message": str(error),
        }

        # Save the data as JSON
        with open(f"{json_folder}{run_identifier}_response.json", "w") as file:
            json.dump(data, file, indent=4)

        print(f"An error occurred: {str(error)}")


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Scrape weather data for a specific city.")
    parser.add_argument("--city", type=str, help="City name (e.g., ciudad-de-mexico)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the city argument is provided
    if args.city:
        scrape_weather_data(args.city)
    else:
        print("Please provide the city name using the --city flag.")
