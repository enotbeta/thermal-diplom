import numpy as np
import pandas as pd
import math
from sklearn.cluster import KMeans


def create_trend(data, close_data_size, ratio):
    length_of_frame = len(data)
    sum_temp_close = 0
    sum_temp_rear = 0
    count = 0
    avg_temp_list = np.zeros(length_of_frame)
    for i in range(close_data_size):
        sum_temp_close += data[i]
        count += 1
        avg_temp_list[i] = sum_temp_close / count

    for i in range(close_data_size, len(data)):
        if data[i] == np.nan:
            data[i] = 0
        sum_temp_close = sum_temp_close + data[i] - data[i - close_data_size]
        avg_temp_list[i] = sum_temp_close / close_data_size

    return avg_temp_list


def create_sdv_trend(data_mean, data_slide_mean, close_data_size, ratio):
    length_of_frame = len(data_mean)
    sum_temp_close = 0
    sum_temp_rear = 0
    count = 0
    avg_sdv_list = np.zeros(length_of_frame)
    for i in range(close_data_size):
        sum = 0
        for j in range(i + 1):
            sum += pow((data_slide_mean[i - j] - data_mean[i]), 2)
            count += 1
        avg_sdv_list[i] = math.sqrt(sum / (i + 1))

    for i in range(close_data_size, len(data_mean)):
        sum = 0
        for j in range(close_data_size):
            sum += pow((data_slide_mean[i - j] - data_mean[i]), 2)
        avg_sdv_list[i] = math.sqrt(sum / close_data_size)
    return create_trend(avg_sdv_list, close_data_size, 0)


# clustering
def clusterise(dataframe, number_of_clusters):
    clusters = []
    data = np.array(dataframe['ts'])
    data = data.reshape(-1, 1)
    kmeans = KMeans(n_clusters=number_of_clusters)
    kmeans.fit(data)
    clustered_data = kmeans.predict(data)
    dataframe['cluster'] = clustered_data
    clusters = []
    for name in dataframe['cluster'].unique():
        clusters.append(dataframe.loc[dataframe['cluster'] == name])
    return clusters
