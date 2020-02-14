import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def neighbourhood_algorithm(df: pd.DataFrame,
                            field_id: str,
                            label_col: str,
                            x_coord_col: str,
                            y_coord_col: str,
                            threshold: int):
    # Coordinates study. Neighbourhood Algorithm. We use col_loc and row_loc as proxy for coordinates
    array_coordinates = np.array([df[x_coord_col], df[y_coord_col]])
    array_coordinates = np.transpose(array_coordinates)
    matrix_distances = pd.DataFrame(distance_matrix(x= array_coordinates, y=array_coordinates))
    matrix_distances = df[[field_id]].join(matrix_distances)
    matrix_distances.set_index(field_id, inplace=True)
    matrix_distances.columns = df[field_id].tolist()
    # Here we remove distances equal to 0 (same field) and distances above threshold
    matrix_distances = matrix_distances.mask(matrix_distances == 0)
    matrix_distances = matrix_distances.mask(matrix_distances >= threshold)
    matrix_distances.reset_index(inplace=True)
    matrix_distances = pd.merge(matrix_distances, df[[field_id, label_col]], left_on=field_id, right_on=field_id, how='left')
    matrix_distances.set_index(field_id, inplace=True)
    matrix_distances = matrix_distances.mask(matrix_distances >0, matrix_distances[label_col], axis=0)
    matrix_distances = matrix_distances.applymap(str)
    matrix_distances.drop([label_col], inplace=True, axis=1)
    matrix_distances = pd.melt(matrix_distances)
    matrix_distances = matrix_distances.applymap(str)
    matrix_distances = matrix_distances.groupby(['variable', 'value']).size().reset_index()
    matrix_distances = matrix_distances[matrix_distances.value != 'nan']
    matrix_distances = pd.crosstab(index=matrix_distances.variable, columns=matrix_distances.value, values=matrix_distances[0], aggfunc='sum')
    matrix_distances.reset_index(inplace=True, drop=False)
    return matrix_distances
