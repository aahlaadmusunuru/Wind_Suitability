import pandas as pd
import os
import arcpy

# Define the file path
DJI_path = r'Y:\Wind Resource Probability Allocation Maps\Wind_GSL_AA\Djibouti\parameters.csv'

# Load the CSV file into a Pandas DataFrame
DJI = pd.read_csv(DJI_path)


# Ensure column names are correctly stripped of leading/trailing spaces (if needed)
DJI.columns = DJI.columns.str.strip()


Output_Path_List=DJI['Output'].unique().tolist()


# Ensure Output_Path is a valid single string (taking the first unique value)
if len(Output_Path_List) > 0:
    Output_Path = str(Output_Path_List[0])  # Convert to string if needed
    Output_Path_GDB = os.path.join(Output_Path, 'Tool_Results.gdb')
    print(Output_Path_GDB)
else:
    print("No valid Output path found.")

# Get the directory containing the GDB
gdb_folder, gdb_name = os.path.split(Output_Path)



# Check if the GDB exists, if not, create it
if not arcpy.Exists(Output_Path):
    arcpy.management.CreateFileGDB(gdb_folder, gdb_name.replace(".gdb", ""))
    print(f"Created GDB: {Output_Path}")
else:
    print(f"GDB already exists: {Output_Path}")


# Filter the data where 'Classes' is 'Roads' OR 'Include_Exclude' is 'T'
DJI_F1 = DJI[(DJI['Classes'].str.strip() == 'Roads') & (DJI['Include_Exclude'].str.strip() == 'T')]

# Roads Buffer Combined  

Roads_Merge_output_gdb = os.path.join(Output_Path_GDB,'Roads_Merge')

# Check if the output feature class exists, then delete it
if arcpy.Exists(Roads_Merge_output_gdb):
    arcpy.Delete_management(Roads_Merge_output_gdb)
    print(f"Existing feature class {Roads_Merge_output_gdb} removed successfully.")

# Get the list of road dataset paths
Road_SRC = DJI_F1['SRC'].astype(str).str.strip().tolist()


# Merge all road datasets into a single feature class
try:
    arcpy.management.Merge(inputs=Road_SRC, output=Roads_Merge_output_gdb)
    print(f"Merge successful. Output saved to: {Roads_Merge_output_gdb}")
except Exception as e:
    print(f"Error during merge: {e}")



# Filter the data where 'Classes' is 'Electricity' OR 'Include_Exclude' is 'T'
DJI_F2 = DJI[(DJI['Classes'].str.strip() == 'Electricity') & (DJI['Include_Exclude'].str.strip() == 'T')]

# Electricity Buffer Combined  

Electricity_Merge_output_gdb = os.path.join(Output_Path_GDB,'Electricity_Merge')

# Check if the output feature class exists, then delete it
if arcpy.Exists(Electricity_Merge_output_gdb):
    arcpy.Delete_management(Electricity_Merge_output_gdb)
    print(f"Existing feature class {Electricity_Merge_output_gdb} removed successfully.")

# Get the list of Electricity dataset paths
Electricity_SRC = DJI_F2['SRC'].astype(str).str.strip().tolist()


# Merge all elec datasets into a single feature class
try:
    arcpy.management.Merge(inputs=Electricity_SRC, output=Electricity_Merge_output_gdb)
    print(f"Merge successful. Output saved to: {Electricity_Merge_output_gdb}")
except Exception as e:
    print(f"Error during merge: {e}")

# Roads and Electricity Intersected locations


Roads_Electricity_Paths = [Roads_Merge_output_gdb, Electricity_Merge_output_gdb]
roads_Electricity_Intersection_output_Combine_gdb = os.path.join(Output_Path_GDB,'Roads_Electricity_Intersection')
# Check if the output feature class exists, then delete it
if arcpy.Exists(roads_Electricity_Intersection_output_Combine_gdb):
    arcpy.Delete_management(roads_Electricity_Intersection_output_Combine_gdb)
    print(f"Existing feature class {roads_Electricity_Intersection_output_Combine_gdb} removed successfully.")


arcpy.analysis.Intersect(Roads_Electricity_Paths,roads_Electricity_Intersection_output_Combine_gdb)



