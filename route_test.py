import requests

print("SMARTTRAFFIC - ROUTE TEST")

def get_coordinates(place):
    url = "https://nominatim.openstreetmap.org/search"
    response = requests.get(
        url,
        params={"q": place, "format": "json", "limit": 1},
        headers={"User-Agent": "SmartTrafficStudentProject/1.0"},
        timeout=20
    )
    response.raise_for_status()
    results = response.json()

    if not results:
        return None

    return float(results[0]["lon"]), float(results[0]["lat"])


try:
    start = input("Starting location: ")
    destination = input("Destination: ")

    origin = get_coordinates(start)
    target = get_coordinates(destination)

    if origin is None or target is None:
        print("Location not found. Check the spelling.")
    else:
        url = "https://router.project-osrm.org/route/v1/driving/"
        url += str(origin[0]) + "," + str(origin[1]) + ";"
        url += str(target[0]) + "," + str(target[1])

        response = requests.get(
            url,
            params={"overview": "false", "alternatives": "true"},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        if result["code"] != "Ok" or not result["routes"]:
            print("No route found.")
        else:
            for i, route in enumerate(result["routes"], 1):
                print("\nRoute", i)
                print("Distance:", round(route["distance"] / 1000, 2), "km")
                print("Estimated time:", round(route["duration"] / 60, 1), "minutes")

            print("\nThese are routing estimates, not live traffic predictions.")

except requests.RequestException as error:
    print("Network or routing error:", error)
except (ValueError, KeyError) as error:
    print("Could not process the route:", error)
