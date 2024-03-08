# %%
# !pip install numpy scipy matplotlib folium
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm
import folium

# %%
# Helper function to convert lat/lon to Cartesian coordinates (in meters)
def latlon_to_cartesian(lat, lon, origin_lat, origin_lon):
    R = 6371000  # Earth radius in meters
    x = R * np.radians(lon - origin_lon) * np.cos(np.radians(origin_lat))
    y = R * np.radians(lat - origin_lat)
    return x, y


# Define coordinates
bank_of_england = (51.514171, -0.088438)
thames_coords = [
    (51.489467, -0.236313),
    (51.468045, -0.216379),
    (51.464141, -0.190458),
    (51.473257, -0.179515),
    (51.480661, -0.173850),
    (51.484590, -0.148573),
    (51.483601, -0.137501),
    (51.485793, -0.129604),
    (51.494744, -0.122824),
    (51.508208, -0.118489),
    (51.509330, -0.096431),
    (51.501904, -0.058365),
    (51.508662, -0.043216),
    (51.506098, -0.030727),
    (51.490202, -0.028796),
    (51.485098, -0.007725),
    (51.490683, 0.000215),
    (51.502305, -0.005407),
    (51.506552, 0.005536),
]
satellite_path = [(51.451000, -0.300000), (51.560000, 0.000000)]

# %%
# Plot coordinates in folium
m = folium.Map(location=bank_of_england, zoom_start=12)
folium.Marker(location=bank_of_england, popup="Bank of England").add_to(m)
folium.PolyLine(thames_coords, color="green", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(satellite_path, color="blue", weight=2.5, opacity=1).add_to(m)
m
# The points on the map look okey.
# The thamesis maps, the bank of england too

# %%
# Convert all points to Cartesian coordinates
## Given how close the coordinates are, we can work in the cartesian plane
origin = bank_of_england  # Bank of England as origin
bank_of_england_cartesian = (0, 0)  # Origin

thames_cartesian = [
    latlon_to_cartesian(lat, lon, *origin) for lat, lon in thames_coords
]
satellite_path_cartesian = [
    latlon_to_cartesian(lat, lon, *origin) for lat, lon in satellite_path
]
# %%
# Plot Coordinates
plt.figure(figsize=(8, 8))
plt.plot(*bank_of_england_cartesian, "ro", label="Bank of England")
plt.plot(*zip(*thames_cartesian), "g", label="Thames")
plt.plot(*zip(*satellite_path_cartesian), "b", label="Satellite Path")
plt.legend()
plt.title("Cartesian Coordinates")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.show()
# Sanity check that aligns with the Folium map
# %%
# Create a grid for analysis
x_range = np.linspace(-10_000, 5_000, 300)
y_range = np.linspace(-4_000, 6_000, 300)
x_grid, y_grid = np.meshgrid(x_range, y_range)
# %%
# Log-normal for Bank of England
distance_grid = np.sqrt(x_grid**2 + y_grid**2)
lognorm_bank = lognorm(
    s=np.sqrt(np.log((4744 / 3777) ** 2 + 1)), scale=np.exp(np.log(4744))
).pdf(distance_grid)
# %%
# Plot the Log-normal for Bank of England
plt.figure(figsize=(10, 10))
plt.contourf(x_grid, y_grid, lognorm_bank, levels=50, cmap="viridis")
plt.scatter(0, 0, color="red", label="Bank of England")
plt.legend()
plt.title("Bank of England Probability Map")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.show()

# %%
# Define probability distributions
# Gaussian for Thames
def distance_to_thames(x, y):
    min_dist = np.min([np.hypot(x - tx, y - ty) for tx, ty in thames_cartesian])
    return min_dist


sigma_thames = 2730 / 2 / np.sqrt(2 * np.log(2))
gaussian_thames = np.vectorize(
    lambda x, y: norm.pdf(distance_to_thames(x, y), 0, sigma_thames)
)
# %%
# Plot the Gaussian for Thames
plt.figure(figsize=(10, 10))
plt.contourf(x_grid, y_grid, gaussian_thames(x_grid, y_grid), levels=50, cmap="viridis")
plt.scatter(0, 0, color="red", label="Bank of England")
plt.legend()
plt.title("Thames Probability Map")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.show()
# The probability function is not continous, as I am using the provided discrete points.
# An improvement can be interpolation between points.

# %%
# Gaussian for satellite path
## The great circle is the shortest distance between the two points along the surface of the spherical earth.
## Under cartesian assumptions is the euclidean distance. 
def distance_to_satellite_path(x, y):
    p1, p2 = satellite_path_cartesian
    d_line = np.abs(
        (p2[1] - p1[1]) * x - (p2[0] - p1[0]) * y + p2[0] * p1[1] - p2[1] * p1[0]
    ) / np.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
    return d_line


sigma_satellite = 3160 / 2 / np.sqrt(2 * np.log(2))
gaussian_satellite = np.vectorize(
    lambda x, y: norm.pdf(distance_to_satellite_path(x, y), 0, sigma_satellite)
)
# %%
# Plot the Gaussian for satellite path
plt.figure(figsize=(10, 10))
plt.contourf(
    x_grid, y_grid, gaussian_satellite(x_grid, y_grid), levels=50, cmap="viridis"
)
plt.scatter(0, 0, color="red", label="Bank of England")
plt.legend()
plt.title("Satellite Path Probability Map")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.show()

# %%
# Combine and normalize probabilities
# Assuming independence, we can multiply the probabilities.
combined_prob = (
    gaussian_thames(x_grid, y_grid) * lognorm_bank * gaussian_satellite(x_grid, y_grid)
)
combined_prob /= np.max(combined_prob)  # Normalize

# Find and mark the best location
max_prob_idx = np.unravel_index(
    np.argmax(combined_prob, axis=None), combined_prob.shape
)
best_location_cartesian = (x_range[max_prob_idx[1]], y_range[max_prob_idx[0]])
# %%
# Plot
plt.figure(figsize=(10, 10))
plt.contourf(x_grid, y_grid, combined_prob, levels=50, cmap="viridis")
plt.scatter(0, 0, color="red", label="Bank of England")
plt.scatter(*best_location_cartesian, color="white", label="Best Location")
plt.legend()
plt.title("Best Location Probability Map")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.show()
# %%
print(
    f"Best location (cartesian) to send the recruiters is at X: {best_location_cartesian[0]} meters, Y: {best_location_cartesian[1]} meters from the Bank of England."
)
# Back to Geographic Coordinates
best_location_latlon = (
    origin[0] + best_location_cartesian[1] / 6371000 * 180 / np.pi,
    origin[1] + best_location_cartesian[0] / 6371000 * 180 / np.pi,
)
print(
    f"Best location (lat/lon) to send the recruiters is at {best_location_latlon[0]} latitude, {best_location_latlon[1]} longitude."
)
# %%
# In Folium
m = folium.Map(location=origin, zoom_start=14)
folium.Marker(location=origin, popup="Bank of England").add_to(m)
folium.Marker(
    location=best_location_latlon,
    popup="Best Location",
    icon=folium.Icon(color="green"),
).add_to(m)
folium.PolyLine(thames_coords, color="green", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(satellite_path, color="blue", weight=2.5, opacity=1).add_to(m)
m
# %%
