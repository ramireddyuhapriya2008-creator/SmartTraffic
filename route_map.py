import requests
import folium

def get_coordinates(place):
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": place, "format": "json", "limit": 1},
        headers={"User-Agent": "SmartTrafficStudentProject/1.0"},
        timeout=20
    )
    response.raise_for_status()
    data = response.json()

    if not data:
        return None

    return [float(data[0]["lat"]), float(data[0]["lon"])]

try:
    start = input("Starting location: ")
    destination = input("Destination: ")

    origin = get_coordinates(start)
    target = get_coordinates(destination)

    if origin is None or target is None:
        print("Location not found. Check spelling.")
    else:
        url = "https://router.project-osrm.org/route/v1/driving/"
        url += str(origin[1]) + "," + str(origin[0]) + ";"
        url += str(target[1]) + "," + str(target[0])

        response = requests.get(
            url,
            params={
                "overview": "full",
                "geometries": "geojson"
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        if result["code"] != "Ok" or not result["routes"]:
            print("No route found.")
        else:
            route = result["routes"][0]

            route_points = [
                [point[1], point[0]]
                for point in route["geometry"]["coordinates"]
            ]

            distance = round(route["distance"] / 1000, 2)
            duration = round(route["duration"] / 60, 1)

            traffic_map = folium.Map(
                location=[
                    (origin[0] + target[0]) / 2,
                    (origin[1] + target[1]) / 2
                ],
                zoom_start=10,
                tiles=None
            )

            folium.TileLayer(
                tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                attr="© OpenStreetMap contributors",
                name="OpenStreetMap"
            ).add_to(traffic_map)

            folium.Marker(
                origin, tooltip="Start",
                icon=folium.Icon(color="green")
            ).add_to(traffic_map)

            folium.Marker(
                target, tooltip="Destination",
                icon=folium.Icon(color="red")
            ).add_to(traffic_map)

            folium.PolyLine(
                route_points,
                color="blue",
                weight=5,
                tooltip="Route: " + str(distance) + " km"
            ).add_to(traffic_map)

            traffic_map.fit_bounds([origin, target])
            traffic_map.save("smarttraffic_route.html")

            print("Distance:", distance, "km")
            print("Estimated time:", duration, "minutes")
            print("Map saved successfully.")

except requests.RequestException as error:
    print("Network error:", error)
except (ValueError, KeyError) as error:
    print("Processing error:", error)
