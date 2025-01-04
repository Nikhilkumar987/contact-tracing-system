import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sklearn.cluster import DBSCAN

# Load and preprocess the data
df = pd.read_json("livedata2.json")
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Perform clustering
df[['latitude', 'longitude']] = np.radians(df[['latitude', 'longitude']])
model = DBSCAN(eps=0.0018288, min_samples=2, metric='haversine').fit(df[['latitude', 'longitude']])
df['cluster'] = model.labels_

# Function to find contacts by name
def find_contacts_by_name(person_name):
    contacts = []
    if person_name in df['id'].values:  # Using the 'id' column as the name column
        for cluster in set(df.loc[df['id'] == person_name, 'cluster']):
            if cluster != -1:  # Ignore noise points
                cluster_members = df[(df['cluster'] == cluster) & (df['id'] != person_name)]
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
        lat_rad = np.radians(float(lat))
        lon_rad = np.radians(float(lon))
        point_cluster = model.fit_predict([[lat_rad, lon_rad]])
        cluster = point_cluster[0]

        if cluster == -1:  # Noise point
            return f"No clusters found near location ({lat}, {lon})"
        
        cluster_members = df[df['cluster'] == cluster]
        for _, row in cluster_members.iterrows():
            contact = f"Contact Name: {row['id']} at ({np.degrees(row['latitude']):.6f}, {np.degrees(row['longitude']):.6f})"
            contacts.append(contact)
    except ValueError:
        return "Invalid latitude or longitude entered."
    return "\n".join(contacts) if contacts else f"No contacts found near location ({lat}, {lon})"

# Function to search based on user choice
def search_contacts():
    search_mode = mode.get()
    if search_mode == "Name":
        person_name = name_entry.get().strip()
        if person_name:
            results = find_contacts_by_name(person_name)
            result_text.set(results)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid Name.")
    elif search_mode == "Location":
        lat = lat_entry.get().strip()
        lon = lon_entry.get().strip()
        if lat and lon:
            results = find_contacts_by_location(lat, lon)
            result_text.set(results)
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
search_button.grid(row=3, column=1, columnspan=2, pady=5)

# Results display
result_text = tk.StringVar()
result_label = tk.Label(root, text="Potential Contacts:", anchor="w")
result_label.pack(padx=10, pady=5, fill="x")

result_display = tk.Label(root, textvariable=result_text, anchor="nw", justify="left", bg="white", relief="sunken", wraplength=400)
result_display.pack(padx=10, pady=5, fill="both", expand=True)

# Start the UI loop
root.mainloop()
