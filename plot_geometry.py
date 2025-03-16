import pandas as pd
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
import argparse
import os

def read_stl_2d(stl_file, min_height=0.5):
    """Read an STL file and return its 2D convex hull projection (x, y coordinates).
       If the shape is nearly 1D, expand it into a rectangle.
    """
    # Read the STL file
    your_mesh = mesh.Mesh.from_file(stl_file)
    
    # Extract x, y coordinates
    vertices_2d = your_mesh.vectors.reshape(-1, 3)[:, :2]

    # Remove duplicate points
    vertices_2d = np.unique(vertices_2d, axis=0)

    if len(vertices_2d) < 3:
        return expand_to_rectangle(vertices_2d, min_height)

    # Check if all points are collinear
    
    y_min, y_max = np.min(vertices_2d[:, 1]), np.max(vertices_2d[:, 1])
    height = y_max - y_min
    
    if is_collinear(vertices_2d) or height < min_height:
        return expand_to_rectangle(vertices_2d, min_height)

    # Compute convex hull normally if not 1D
    hull = ConvexHull(vertices_2d)
    return vertices_2d[hull.vertices]

def is_collinear(points, tol=1e-6):
    """Check if all points are collinear."""
    if len(points) < 3:
        return True  # Less than 3 points is always "collinear"

    p1, p2 = points[0], points[1]
    dx, dy = p2 - p1

    for i in range(2, len(points)):
        px, py = points[i]
        # Compute cross-product to check if the point is on the same line
        if abs((px - p1[0]) * dy - (py - p1[1]) * dx) > tol:
            return False  # Found a non-collinear point

    return True  # All points are collinear

def expand_to_rectangle(points, min_height):
    """Expand collinear points into a small rectangle."""
    if len(points) == 1:
        # Single point - make a small square
        p1 = points[0]
        p2 = p1 + np.array([min_height, 0])  # Horizontal offset
        p3 = p1 + np.array([0, min_height])  # Vertical offset
        p4 = p1 + np.array([min_height, min_height])  # Diagonal point
        return np.array([p1, p2, p4, p3])

    # Find the two most distant points in the collinear set
    dists = np.linalg.norm(points - points[0], axis=1)
    farthest_idx = np.argmax(dists)
    p1, p2 = points[0], points[farthest_idx]

    # Compute perpendicular direction for artificial thickness
    dx, dy = p2 - p1
    norm = np.sqrt(dx**2 + dy**2)
    perp_dir = np.array([-dy, dx]) / norm  # Rotate 90 degrees and normalize

    # Expand into a rectangle
    p1a = p1 + perp_dir * min_height
    p1b = p1 - perp_dir * min_height
    p2a = p2 + perp_dir * min_height
    p2b = p2 - perp_dir * min_height

    return np.array([p1a, p2a, p2b, p1b])




def plot_geometry(experiment_name, exclude_components=None, output_file=None):
    """Plot geometry components from a CSV file."""
    # Read the CSV file
    csv_file = f"./data_files/data/{experiment_name}/geometry_components_{experiment_name}.csv"
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 10))
    
    # List of components to exclude
    e = [1,3,4,5,7,8]
    exclude_components = [f"reflector{i}" for i in e]
    exclude_components2 = ["silica gasket 1", "silica gasket 2", "reflectorholder1", "reflectorholder2"]
    [exclude_components.append(i) for i in exclude_components2]

    
    for _, row in df.iterrows():
        if exclude_components and row['name'] in exclude_components:
            continue  # Skip excluded components

        # Read and plot the STL file
        stl_file = row['stl_filepath']
        color = row['color']
        
        try:
            vertices_2d = read_stl_2d(stl_file)
            polygon = Polygon(vertices_2d, facecolor=color, edgecolor='black', alpha=0.5, label=row['name'])
            plt.gca().add_patch(polygon)
        except Exception as e:
            print(f"Error processing {row['name']}: {str(e)}")

        except Exception as e:
            print(f"Error processing source: {str(e)}")
    
    plt.axis('equal')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title('Geometry Components')
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description='Plot geometry components from STL files')
    parser.add_argument('--experiment', required=True, help='Enter an experiment name')
    parser.add_argument('--exclude', nargs='+', help='List of component names to exclude')
    parser.add_argument('--output', help='Path to save the output plot')
    
    args = parser.parse_args()
    
    plot_geometry(args.experiment, args.exclude, args.output)

if __name__ == '__main__':
    main()
