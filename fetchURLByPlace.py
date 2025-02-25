import requests
import csv

API_KEY = "" # your Places API key
PLACE = "Houston"


def fetch_apartments():
    """
    Use the Text Search API to find apartments in PLACE.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": "apartments in " + PLACE, "key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching apartments: {response.text}")
    print("Status Code:", response.status_code)
    data = response.json()
    print("Response:", data)
    return data.get("results", [])


def get_place_details(place_id):
    """
    Use the Place Details API to fetch details including the Google Maps URL.
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "url", "key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching details for {place_id}: {response.text}")
    data = response.json()
    return data.get("result", {})


def main():
    print("Fetching apartments in " + PLACE + "...")
    apartments = fetch_apartments()
    if not apartments:
        print("No apartments found.")
        return

    # Open a CSV file for writing the output
    with open("apartments.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write CSV header
        writer.writerow(["Apartment Name", "Google Maps URL"])

        for apt in apartments:
            name = apt.get("name", "Unnamed Apartment")
            place_id = apt.get("place_id")
            if not place_id:
                continue  # Skip if no place ID is found

            details = get_place_details(place_id)
            maps_url = details.get("url", "URL not available")
            writer.writerow([name, maps_url])
            print(f"Saved: {name} - {maps_url}")

    print("All apartment URLs saved to apartments.csv")


if __name__ == "__main__":
    main()
