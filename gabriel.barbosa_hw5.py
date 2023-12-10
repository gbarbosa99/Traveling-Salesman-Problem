import pandas as pd
import mpu
import matplotlib.pyplot as plt


class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


def calculate_distance(city1, city2):
    return mpu.haversine_distance((city1.latitude, city1.longitude), (city2.latitude, city2.longitude))


def extract_random_cities(data_file, n):
    data = pd.read_csv(data_file)
    selected_cities = data.sample(n)
    cities = [City(row['city'], row['lat'], row['lng']) for _, row in selected_cities.iterrows()]
    return cities


def greedy_algorithm(city_tour):
    current_city = city_tour[0]
    unvisited_cities = city_tour[1:]

    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: calculate_distance(current_city, city))
        city_tour.remove(nearest_city)
        city_tour.append(nearest_city)
        current_city = nearest_city
        unvisited_cities.remove(nearest_city)

    return city_tour


def plot_tour(city_tour):
    lats, lons, names = zip(*[(city.latitude, city.longitude, city.name) for city in city_tour])
    lats += (city_tour[0].latitude,)
    lons += (city_tour[0].longitude,)
    names += (city_tour[0].name,)  # Add the first city name again to complete the loop

    plt.figure(figsize=(10, 6))
    plt.plot(lons, lats, marker='o', linestyle='-', color='b')

    for name, lon, lat in zip(names, lons, lats):
        plt.text(lon, lat, name, fontsize=8, ha='right', va='bottom')

    plt.title('City Tour')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()


def main():
    data_file = 'uscities.csv'
    n = 10
    random_cities = extract_random_cities(data_file, n)
    city_tour = random_cities.copy()
    city_tour = greedy_algorithm(city_tour)

    total_distance = sum(calculate_distance(city_tour[i], city_tour[i + 1]) for i in range(len(city_tour) - 1))
    total_distance += calculate_distance(city_tour[-1], city_tour[0])
    print(f"Total Distance: {total_distance} km")

    print("Tour:")
    for city in city_tour:
        print(city.name)

    plot_tour(city_tour)


if __name__ == "__main__":
    main()
