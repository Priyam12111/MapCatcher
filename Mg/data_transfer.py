from pymongo import MongoClient
import pandas as pd

# Step 1: Connect to MongoDB
client = MongoClient("mongodb+srv://Priyam:5H7SatQX2vjV60ea@mapcasher.fkurktv.mongodb.net/")
db = client["MapData"]
collection = db["LargeData"]

# Step 2: Load large dataset into a pandas DataFrame
df = pd.read_excel(r"Mg\cropMain20240312220305.xlsx")

# Step 3: Convert DataFrame to a list of dictionaries (MongoDB documents)
data_list = df.to_dict(orient="records")

# Step 4: Insert data into MongoDB using insert_many()
collection.insert_many(data_list)

# Close the MongoDB connection (optional)
client.close()
