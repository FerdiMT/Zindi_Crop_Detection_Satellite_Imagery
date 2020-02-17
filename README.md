# Zindi_Radiant Earth Computer Vision for Crop Detection from Satellite Imagery
https://zindi.africa/competitions/iclr-workshop-challenge-2-radiant-earth-computer-vision-for-crop-recognition

#### Changelog:



| ID     | Version                             | Comments                                                     | Zindi score | Issues/Todo's                                                |
| ------ | ----------------------------------- | ------------------------------------------------------------ | ----------- | ------------------------------------------------------------ |
| id_1   | ML-Baseline                         | Baseline                                                     | 1.2549      | Some fields in training set might be NA/0, the ones that are less than a pixel. Instea of fillna(0) maybe just remove them.<br />Gridsearch parameters<br />Generate algorithm to detect neighbourhood. |
| id_2   | ML-Neighbourhood Algorithm          | Added the Neighbourhood Algorithm (own)                      | 1.2570      | Standardize results from neighbourhood algo (matrix_distances).<br />PCA<br />Check other models<br />Gridsearch parameters |
| id_3   | ML-Neighbourhood Algorithm XGB      |                                                              | 1.2554      |                                                              |
| id_3.1 | ML- XGB                             | No neighbourhood algo                                        | 1.2800      |                                                              |
| id_4   | ML-XGB-Neighbourhood in percentages | Put the results of neighbourhood algorithm in percentages (by rows) | 1.2286      |                                                              |