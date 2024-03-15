import numpy as np
import glob
import pandas as pd

# Path to your dataset directory, adjust as needed
dataset_path = 'datasets/'

# List all CSV files in the directory
csv_files = glob.glob(dataset_path + '*.csv')

# Determine the number of files
num_files = len(csv_files)
num_lines = 80

# Possible values for each column
opti_flag_ids_possible = [1, 2, 3]
vecto_flag_ids_possible = [1, 2, 3, 4]
tbs_possible = [1, 2, 4, 8, 16, 32, 64, 128, 256]
n_threads_possible = np.arange(1, 33)  # 1 to 32

# Generate the data respecting the possible values
opti_flag_ids = np.random.choice(opti_flag_ids_possible, size=num_lines)
vecto_flag_ids = np.random.choice(vecto_flag_ids_possible, size=num_lines)
x_tbs_values = np.random.choice(tbs_possible, size=num_lines)
y_tbs_values = np.random.choice(tbs_possible, size=num_lines)
z_tbs_values = np.random.choice(tbs_possible, size=num_lines)
n_threads_values = np.random.choice(n_threads_possible, size=num_lines)
rank_values = np.round(np.random.uniform(0, 1, size=num_lines), 2)  # Uniformly distributed between 0 and 1

# Recreate DataFrame with constrained values
df_constrained = pd.DataFrame({
    "opti_flag_id": opti_flag_ids,
    "vecto_flag_id": vecto_flag_ids,
    "x_tbs": x_tbs_values,
    "y_tbs": y_tbs_values,
    "z_tbs": z_tbs_values,
    "n_threads": n_threads_values,
    "rank": rank_values
})

# Save the DataFrame to a new CSV file
constrained_file_path = f'data{num_files}.csv'
df_constrained.to_csv(constrained_file_path, index=False)

constrained_file_path, df_constrained.head()
