import plotly.graph_objects as go
import numpy as np
import random
from plotly.subplots import make_subplots

# Function for adding line connections between two sets of points with color intensity based on rankings


# Example input data array (n_paths, 5) - replace with your actual data
n_paths = 1000
data = np.random.rand(n_paths, 5)  # Random data for demonstration

# Separate the components of the paths and their rankings
paths = data[:, :-1]  # All but the last column
rankings = data[:, -1]  # Last column

# Sort paths by rankings
sorted_indices = np.argsort(rankings)
sorted_paths = paths[sorted_indices]
sorted_rankings = rankings[sorted_indices]

# Path labels for the x-axis of the bar plot
path_labels = [f"Path {i+1}" for i in range(n_paths)]

# Create subplot figure
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'scatter3d'}, {'type': 'bar'}]],
                    column_widths=[0.7, 0.3],  # Adjust as needed
                    subplot_titles=("3D Visualization", "Path Rankings"))

iteration = 1


def add_connections_with_ranking(fig, points_from, points_to, base_color, rankings):
    """
    Add connections between sets of points with line color intensity based on rankings.
    
    :param fig: Plotly figure object to which the lines will be added.
    :param points_from: Array of source points for the connections.
    :param points_to: Array of destination points for the connections.
    :param base_color: Base color for the lines in RGBA format, with a placeholder for the alpha value.
    :param rankings: A list of rankings corresponding to the connections. Length should match the total number of lines to be drawn.
    """
    assert len(rankings) == len(points_from) * len(points_to), "Rankings length must match the total number of connections."
    
    ranking_idx = 0
    for point_from in points_from:
        for point_to in points_to:
            # Retrieve the ranking for this specific connection
            rank = rankings[ranking_idx]
            ranking_idx += 1
            
            # Calculate the tint color based on the ranking
            tint = base_color - base_color * rank  #  Tint color based on ranking
            color = f"rgba({tint},{tint},{tint},0.3)"
            fig.add_trace(go.Scatter3d(x=[point_from[0], point_to[0]],
                                       y=[point_from[1], point_to[1]],
                                       z=[point_from[2], point_to[2]],
                                       mode='lines',
                                       line=dict(color=color, width=2),
                                       showlegend=False
                                       ),row=1, col=1)
    print("connections added")

# Thread block sizes and parameters setup
thread_block_sizes = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])
log_thread_block_sizes = np.log2(thread_block_sizes)  # Apply log2 transformation

# Prepare points for the hypercube
x, y, z = np.meshgrid(log_thread_block_sizes, log_thread_block_sizes, log_thread_block_sizes)
thread_block_points = np.array([x.flatten()*2 -x.flatten()[len(x.flatten())-1]/2, y.flatten(), z.flatten()]).T

# Prepare points for Optimization Flags
opt_flag_z = np.max(z) + 3.5  # Slightly above the cube
opt_flag_points = np.array([np.linspace(np.min(x), np.max(x), len(['-O2', '-O3', '-Ofast'])),
                            np.full(len(['-O2', '-O3', '-Ofast']), np.max(y)/2),
                            np.full(len(['-O2', '-O3', '-Ofast']), opt_flag_z)]).T

# Prepare points for SIMD Flags
simd_flag_z = np.min(z) - 3 # Below optimization flags
simd_flag_points = np.array([np.linspace(np.min(x), np.max(x), len(['sse', 'avx', 'avx2', 'avx512'])),
                             np.full(len(['sse', 'avx', 'avx2', 'avx512']), np.max(y)/2),
                             np.full(len(['sse', 'avx', 'avx2', 'avx512']), simd_flag_z)]).T

# Prepare points for Number of Threads
thread_z = np.min(z) - 6  # At the cube level
thread_points = np.array([np.linspace(np.min(x)-6, np.max(x)+6, len(np.arange(1, 33))),
                          np.full(len(np.arange(1, 33)), np.max(y)/2),
                          np.full(len(np.arange(1, 33)), thread_z)]).T

# Initialize the figure25

# Add each parameter set


# Add thread block sizes cube in log scale
fig.add_trace(go.Scatter3d(x=thread_block_points[:, 0], y=thread_block_points[:, 1], z=thread_block_points[:, 2],
                           mode='markers', 
                           marker=dict(size=2, color='black'),
                           name='Thread Block Sizes',
                           showlegend=False
                           ), row=1, col=1)

# Optimization Flags names (corresponding to each flag)
opt_flag_names = ['-O2', '-O3', '-Ofast']

# Adding Optimization Flags with hover text
fig.add_trace(go.Scatter3d(
    x=opt_flag_points[:, 0], 
    y=opt_flag_points[:, 1], 
    z=opt_flag_points[:, 2],
    mode='markers+text',  # Combine markers and text
    marker=dict(size=5, color='red'),
    text=opt_flag_names,  # Assign the names as hover text
    hoverinfo='text',  # Show only the text on hover
    name='Optimization Flags',
    showlegend=False
), row=1, col=1)


# SIMD Flags names (corresponding to each flag)
simd_flag_names = ['sse', 'avx', 'avx2', 'avx512']

# Adding SIMD Flags with hover text
fig.add_trace(go.Scatter3d(
    x=simd_flag_points[:, 0], 
    y=simd_flag_points[:, 1], 
    z=simd_flag_points[:, 2],
    mode='markers+text',  # Use markers for points
    marker=dict(size=5, color='red'),
    text=simd_flag_names,  # Assign the names as hover text
    hoverinfo='text',  # Show only the text on hover
    name='SIMD Flags',
    showlegend=False
), row=1, col=1)

# Generate labels for each number of threads
thread_labels = [f'{n}' for n in np.arange(1, 33)]

# Adding Number of Threads with hover text
fig.add_trace(go.Scatter3d(
    x=thread_points[:, 0],
    y=thread_points[:, 1],
    z=thread_points[:, 2],
    mode='markers+text',  # Use markers for points
    marker=dict(size=5, color='orange'),
    text=thread_labels,  # Assign the labels as hover text
    hoverinfo='text',  # Show only the text on hover
    name='Number of Threads',
    showlegend=False
), row=1, col=1)


# Base color for the lines without the alpha value
base_color = 105
# These should be replaced with actual rankings data
example_rankings = np.random.rand(len(opt_flag_points) * len(thread_block_points))  # For opt_flag to thread_block connections
example_rankings2 = np.random.rand(len(thread_block_points) * len(simd_flag_points))  # For thread_block to simd_flag connections
example_rankings3 = np.random.rand(len(simd_flag_points) * len(thread_points))  # For simd_flag to thread_points connections

# Add connections with specified rankings
add_connections_with_ranking(fig, opt_flag_points, thread_block_points, base_color, example_rankings)
add_connections_with_ranking(fig, thread_block_points, simd_flag_points, base_color, example_rankings2)
add_connections_with_ranking(fig, simd_flag_points, thread_points, base_color, example_rankings3)





###SECONDPLOT
# Add bar trace for sorted rankings to the second subplot
fig.add_trace(go.Bar(
    x=path_labels,  # Use path_labels for the x-axis
    y=sorted_rankings,
    marker_color='black',  # Customize as needed
    name='Path Rankings',
    showlegend=False
), row=1, col=2)


# Update layout for better visualization
fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        camera=dict(eye=dict(x=0, y=-1.7, z=0))
    ),
    bargap=0.2,  # Adjust spacing for the bar chart
    title='',
    width=1800,  # Adjust width for better side-by-side view
    margin=dict(l=50, r=50, b=50, t=50)  # Adjust margins as needed
)



fig.write_image(f"figs/fig_iter_n{iteration}.png", height = 1000, width = 1800,  scale = 2)

