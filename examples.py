from data import stocks, analysis
from models import linear_models
import pandas as pd

#returns = stocks.get_stocks(['WEGE3.SA', 'ITSA4.SA'], start = '2019-5-2', returns = True)
data = {
  "calories": [420, 380, 390, 254, 236, 364, 368],
  "duration": [50, 40, 45, 36, 14, 25, 65]
}
data = pd.DataFrame(data)


#lm = linear_models.linearModel(data)
r = analysis.Analyzer(data)
r.complete()