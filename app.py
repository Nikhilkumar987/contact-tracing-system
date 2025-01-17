import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sklearn.cluster import DBSCAN
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json
from datetime import datetime

# File to store search logs
LOG_FILE = "search_log.json"

# Load and preprocess the data
df = pd.read_json("livedata2.json")
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Split the data into training and testing sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Use train_df for training the model
train_df[['latitude', 'longitude']] = np.radians(train_df[['latitude', 'longitude']])
model = DBSCAN(eps=0.0018288, min_samples=2, metric='haversine').fit(train_df[['latitude', 'longitude']])
train_df['cluster'] = model.labels_

# Function to find contacts by name
def find_contacts_by_name(person_name):
    contacts = []
    if person_name in train_df['id'].values:  # Using the 'id' column as the name column
        for cluster in set(train_df.loc[train_df['id'] == person_name, 'cluster']):
            if cluster != -1:  # Ignore noise points
                cluster_members = train_df[(train_df['cluster'] == cluster) & (train_df['id'] != person_name)]
                for _, row in cluster_members.iterrows():
                    contact = f"Contact Name: {row['id']} at ({np.degrees(row['latitude']):.6f}, {np.degrees(row['longitude']):.6f})"
                    contacts.append(contact)
    else:
        return f"No data found for Name: {person_name}"
    return "\n".join(contacts) if contacts else f"No close contacts found for Name: {person_name}"

# Function to find contacts by location
def find_contacts_by_location(lat, lon):
    contacts = []
    try:
        # Convert the input latitude and longitude to radians
        lat_rad = np.radians(float(lat))
        lon_rad = np.radians(float(lon))
        location = np.array([lat_rad, lon_rad])
        
        # Compute the haversine distance to all points in the dataset
        distances = np.sqrt((train_df['latitude'] - lat_rad)**2 + (train_df['longitude'] - lon_rad)**2)
        nearest_point_index = distances.idxmin()
        
        # Find the cluster of the nearest point
        cluster = train_df.loc[nearest_point_index, 'cluster']

        if cluster == -1:  # Noise point
            return f"No clusters found near location ({lat}, {lon})"
        
        # Get all members of the same cluster
        cluster_members = train_df[train_df['cluster'] == cluster]
        for _, row in cluster_members.iterrows():
            contact = f"Contact Name: {row['id']} at ({np.degrees(row['latitude']):.6f}, {np.degrees(row['longitude']):.6f})"
            contacts.append(contact)
    except ValueError:
        return "Invalid latitude or longitude entered."
    
    return "\n".join(contacts) if contacts else f"No contacts found near location ({lat}, {lon})"

# Function to log search results
def log_search(person_name=None, location=None, results=None):
    # Prepare log entry
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "search_type": "Name" if person_name else "Location",
        "search_input": person_name if person_name else location,
        "results": results.split("\n") if results else [],
    }
    
    # Read existing logs or create a new log file
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    # Append the new entry and write back to the file
    logs.append(log_entry)
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

# Function to display scatter plot and heat map
def show_visualization():
    contacts = result_text.get().split("\n")
    if not contacts or "No" in contacts[0]:
        messagebox.showinfo("No Data", "No contacts to display.")
        return
    
    latitudes = []
    longitudes = []
    names = []
    
    for contact in contacts:
        parts = contact.split(" at (")
        if len(parts) > 1:
            names.append(parts[0].replace("Contact Name: ", ""))
            coord_parts = parts[1].replace(")", "").split(", ")
            latitudes.append(float(coord_parts[0]))
            longitudes.append(float(coord_parts[1]))
    
    plt.figure(figsize=(12, 6))

    # Scatter plot
    plt.subplot(1, 2, 1)
    plt.scatter(longitudes, latitudes, c='blue', label="Contacts")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Scatter Plot of Contacts")
    for i, name in enumerate(names):
        plt.text(longitudes[i], latitudes[i], name, fontsize=9, ha='right')
    plt.legend()
    plt.grid(True)

    # Heat map
    plt.subplot(1, 2, 2)
    plt.hexbin(longitudes, latitudes, gridsize=30, cmap='YlOrRd', mincnt=1)
    plt.colorbar(label='Number of Contacts')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Heat Map of Contact Density")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Function to search based on user choice
def search_contacts():
    search_mode = mode.get()
    if search_mode == "Name":
        person_name = name_entry.get().strip()
        if person_name:
            results = find_contacts_by_name(person_name)
            result_text.set(results)
            log_search(person_name=person_name, results=results)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid Name.")
    elif search_mode == "Location":
        lat = lat_entry.get().strip()
        lon = lon_entry.get().strip()
        if lat and lon:
            location = {"latitude": lat, "longitude": lon}
            results = find_contacts_by_location(lat, lon)
            result_text.set(results)
            log_search(location=location, results=results)
        else:
            messagebox.showwarning("Input Error", "Please enter both Latitude and Longitude.")

# Main UI Window
root = tk.Tk()
root.title("COVID Contact Tracing Tool")

# Input frame
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Mode selection
mode = tk.StringVar(value="Name")
name_radio = ttk.Radiobutton(frame, text="Search by Name", variable=mode, value="Name")
name_radio.grid(row=0, column=0, padx=5, pady=5)

location_radio = ttk.Radiobutton(frame, text="Search by Location", variable=mode, value="Location")
location_radio.grid(row=0, column=1, padx=5, pady=5)

# Name input
name_label = tk.Label(frame, text="Enter Name:")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_entry = ttk.Entry(frame, width=30)
name_entry.grid(row=1, column=1, padx=5, pady=5)

# Location input
lat_label = tk.Label(frame, text="Latitude:")
lat_label.grid(row=2, column=0, padx=5, pady=5)
lat_entry = ttk.Entry(frame, width=15)
lat_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

lon_label = tk.Label(frame, text="Longitude:")
lon_label.grid(row=2, column=1, padx=5, pady=5, sticky="e")
lon_entry = ttk.Entry(frame, width=15)
lon_entry.grid(row=2, column=2, padx=5, pady=5)

# Search button
search_button = ttk.Button(frame, text="Find Contacts", command=search_contacts)
search_button.grid(row=3, column=0, columnspan=2, pady=5)

# Scatter plot and heat map button
scatter_button = ttk.Button(frame, text="Show Visualization", command=show_visualization)
scatter_button.grid(row=3, column=2, columnspan=2, pady=5)

# Results display
result_text = tk.StringVar()
result_label = tk.Label(root, text="Potential Contacts:", anchor="w")
result_label.pack(padx=10, pady=5, fill="x")

result_display = tk.Label(root, textvariable=result_text, anchor="nw", justify="left", bg="white", relief="sunken", wraplength=400)
result_display.pack(padx=10, pady=5, fill="both", expand=True)

# Start the UI loop
root.mainloop()
