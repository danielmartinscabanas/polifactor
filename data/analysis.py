import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class Analyzer:
    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            if isinstance(data, pd.Series):
                self.data = data.to_frame()
            else:
                self.data = pd.DataFrame(data)
        else:
            self.data = data
        self.col_names = self.data.columns.values.tolist()

    def correl_mtx(self):
        return self.data.corr()        
    
    def plot_scatter_mtx(self):
        pd.plotting.scatter_matrix(self.data, alpha = 0.3, diagonal = 'kde')
        plt.show()

    def plot_autocorrel(self):
        for col_name in self.col_names:
            _auto_correl = pd.plotting.autocorrelation_plot(self.data[col_name])
            plt.title(f"Autocorrelation of: '{col_name}'.")
            _auto_correl.plot()
            plt.show()

    def complete(self):
        print(Analyzer.correl_mtx(self))
        Analyzer.plot_scatter_mtx(self)
        Analyzer.plot_autocorrel(self)