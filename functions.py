import numpy as np
import pandas as pd


class Event:
    def __init__(self, id, dataframe):
        self.df = dataframe.loc[dataframe["id"] == id]
        self.id = id
        self.std = 0
        self.avg = 0

    def filter(self, sigma=2):
        self.avg = self.df["temperatureAvg"].mean()
        self.std = self.df.std(ddof=0)["temperatureAvg"]
        self.df = self.df.loc[self.df['temperatureAvg'] > 1]
        self.df = self.df.loc[(self.avg - sigma * self.std < self.df['temperatureAvg']) \
                              & (self.df['temperatureAvg'] < self.avg + sigma * self.std) ]
        self.avg = self.df["temperatureAvg"].mean()
        self.std = self.df.std(ddof=0)["temperatureAvg"]


class Model:
    def __init__(self, dataframe_input, number_of_rows = 10):
        self.df_all = None
        self.df_stat = None
        self.df = dataframe_input
        self.events = []
        self.load(number_of_rows = number_of_rows)



    def show(self, index):
        return self.events[index].df

    def filter(self, sigma=2):
        for item in self.events:
            item.filter(sigma)
        self.concat()

    def concat(self):
        self.concat_all()
        self.concat_stat()

    def concat_all(self):
        self.df_all = self.events[0].df
        for item in range(1, len(self.events)):
            self.df_all = pd.concat([self.df_all, self.events[item].df])

    def concat_stat(self):
        var_mean = []
        var_std = []
        var_id = []
        for item in self.events:
            var_mean.append(item.avg)
            var_std.append(item.std)
            var_id.append(item.id)
        self.df_stat = pd.DataFrame({'id': var_id, 'temperatureAvg': var_mean, 'temperatureSdv': var_std})

    def load(self, dataframe = None, number_of_rows = 10):
        if dataframe is not None:
            self.df = dataframe
        self.events = []
        for id_name in self.df["id"].unique():
            if len(self.df.loc[self.df["id"] == id_name]) > number_of_rows:
                self.events.append(Event(id_name, self.df))
                #print(len(self.df.loc[self.df["id"] == id_name]), id_name)

        self.concat()


class Import:
    def do_import(data):
        data_list = data.split("\r")
        data_list = list(map(lambda x: x[2:], data_list))
        data_list = data_list[1:-1]
        data_list = list(map(lambda x: x.split(' '), data_list))
        id = np.array(list(map(lambda x: x[2], data_list)))
        dist = np.array(list(map(lambda x: x[5], data_list)))
        t = np.array(list(map(lambda x: x[8], data_list)))
        ts = np.array(list(map(lambda x: x[11], data_list)))
        x = np.array(list(map(lambda x: x[14], data_list)))
        y = np.array(list(map(lambda x: x[17], data_list)))
        w = np.array(list(map(lambda x: x[20], data_list)))
        h = np.array(list(map(lambda x: x[23], data_list)))
        strange_thing = np.array(list(map(lambda x: x[24], data_list)))
        x_ir = np.array(list(map(lambda x: x[27], data_list)))
        y_ir = np.array(list(map(lambda x: x[30], data_list)))
        w_ir = np.array(list(map(lambda x: x[33], data_list)))
        h_ir = np.array(list(map(lambda x: x[36], data_list)))
        df = pd.DataFrame({"id": id, "dist": dist, "t": t, "ts": ts, "x": x, "y": y, "w": w, "h": h, \
                           "strange_thing": strange_thing, "x_ir": x_ir, "y_ir": y_ir, "w_ir": w_ir, "h_ir": h_ir})

#model.df_stat[['id','temperatureAvg']].plot(x = 'id', y = 'temperatureAvg', kind = 'scatter')
#model.df_all[['id','temperatureAvg']].plot(x = 'id', y = 'temperatureAvg', kind = 'scatter')