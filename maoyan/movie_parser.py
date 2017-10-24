from database import db
import numpy as np
import pandas as pd
import codecs

if __name__ == '__main__':
    '''
    data = pd.DataFrame.from_dict(list(db.maoyan_info.find({})))
    data.to_csv('data.csv')
    '''
    data = pd.DataFrame.from_dict(list(db.maoyan_com_info.find({})))
    data.to_csv('data_com.csv',sep='$')

    data = pd.DataFrame.from_dict(list(db.maoyan_cel_info.find({})))
    data.to_csv('data_cel.csv',sep='$')
