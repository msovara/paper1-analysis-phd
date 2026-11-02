# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 14:47:39 2025

@author: MthethoSovara
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import Polygon
import cartopy
from matplotlib.patches import Patch

def plot_southern_africa_regions(regions_data, output_filename="southern_africa_regions.png"):
    """
    Plots the specified Southern African regions on a map.

    Args:
        regions_data (dict): A dictionary where keys are region names and values
                             are tuples of (min_lat, max_lat, min_lon, max_lon).
        output_filename (str): The name of the file to save the plot.
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Set the extent of the map to cover Southern Africa and a bit beyond
    # [min_lon, max_lon, min_lat, max_lat]
    ax.set_extent([5, 50, -40, -5], crs=ccrs.PlateCarree())

    # Add standard Cartopy features for better context
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.7)
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.LAKES, facecolor='lightblue', edgecolor='black')
    ax.add_feature(cfeature.RIVERS, edgecolor='blue')

    # Define a list of distinct colors for the regions
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
    color_idx = 0
    legend_patches = []

    # Plot each region
    for region_name, (min_lat, max_lat, min_lon, max_lon) in regions_data.items():
        # Create a polygon for the region using its bounding box
        lons = [min_lon, max_lon, max_lon, min_lon, min_lon]
        lats = [min_lat, min_lat, max_lat, max_lat, min_lat]
        region_polygon = Polygon(zip(lons, lats))

        # Add the polygon to the map
        ax.add_geometries([region_polygon], ccrs.PlateCarree(),
                          facecolor=colors[color_idx % len(colors)],
                          edgecolor='black',
                          alpha=0.4, # Transparency for better visibility of underlying map
                          label=region_name,
                          linewidth=1.5) # Thicker border for regions

        # Add proxy Patch for legend
        legend_patches.append(Patch(facecolor=colors[color_idx % len(colors)], edgecolor='black',
                                   label=region_name, alpha=0.4, linewidth=1.5))

        # Add text label for the region, slightly offset for clarity if needed
        center_lon = (min_lon + max_lon) / 2
        center_lat = (min_lat + max_lat) / 2
        ax.text(center_lon, center_lat, region_name,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ccrs.PlateCarree(),
                fontsize=9, fontweight='bold', color='black',
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.3')) # Background for text

        color_idx += 1

    # Add gridlines and labels for latitude and longitude
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False    # Hide labels on the top axis
    gl.right_labels = False  # Hide labels on the right axis
    gl.xformatter = cartopy.mpl.ticker.LongitudeFormatter() # Format longitude labels
    gl.yformatter = cartopy.mpl.ticker.LatitudeFormatter()  # Format latitude labels

    plt.title("Defined Regions in Southern Africa for Drought Analysis", fontsize=14, pad=15)
    plt.legend(handles=legend_patches, loc='lower left', frameon=True, fancybox=True, shadow=True, borderpad=1)
    plt.savefig(output_filename, dpi=300, bbox_inches='tight') # Save with high resolution
    plt.show()

# Define the regions with their (min_lat, max_lat, min_lon, max_lon)
# Note: Latitudes are negative for Southern Hemisphere
regions = {
    "Southeastern region": (-35, -20, 25, 40),
    "Central region": (-25, -15, 20, 30),
    "Northwestern region": (-20, -10, 10, 25),
    "Southwestern region": (-35, -20, 10, 25)
}

# Call the function to plot the regions
plot_southern_africa_regions(regions)
