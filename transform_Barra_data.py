import os
import data_processing_tool as dpt
from datetime import timedelta, date, datetime
# import args_parameter as args

import numpy as np


import time
import xarray as xr
import sys
import data_processing_tool as dpt


def main():
    import platform 

    sys = platform.system()
    print("start")
    init_date=date(1970, 1, 1)
    start_date=date(1990, 1, 2)
    end_date=date(2012,12,25)
    import netCDF4 as nc
    if sys == "Windows":
        init_date=date(1970, 1, 1)
        start_date=date(1990, 1, 2)
        end_date=date(1990,12,25) #if 929 is true we should substract 1 day   
        file_ACCESS_dir="H:/climate/access-s1/" 
        file_BARRA_dir="D:/dataset/accum_prcp/"
    #         args.file_ACCESS_dir="E:/climate/access-s1/"
    #         args.file_BARRA_dir="C:/Users/JIA059/barra/"
        file_DEM_dir="../DEM/"
    else:
        file_ACCESS_dir_pr="/g/data/ub7/access-s1/hc/raw_model/atmos/pr/daily/"
        file_ACCESS_dir="/g/data/ub7/access-s1/hc/raw_model/atmos/"
        # training_name="temp01"
        file_BARRA_dir="/g/data/ma05/BARRA_R/v1/forecast/spec/accum_prcp/"

    dates=[start_date + timedelta(x) for x in range((end_date - start_date).days + 1)]
    for i in dates:
        print(i)
        data_high=dpt.read_barra_data_fc(file_BARRA_dir,i,nine2nine=True)
        label=dpt.map_aust(data_high,domain=[112.9, 154.25, -43.7425, -9.0])#,domain=domain)

        f_w = nc.Dataset('../data/barra_aus/'+i.strftime("%Y%m%d")+'.nc','w',format = 'NETCDF4')
        f_w.createDimension('lat',len(label["lat"].data))
        f_w.createDimension('lon',len(label["lon"].data))

        f_w.createVariable('lat',np.float32,('lat'))
        f_w.createVariable('lon',np.float32,('lon'))


        f_w.variables['lat'][:] = label["lat"].data
        f_w.variables['lon'][:] = label["lon"].data

        f_w.createVariable( 'barra', np.float32, ('lat','lon'))
        f_w.variables['barra'][:] = label.data

        f_w.close()
    
            
if __name__=='__main__':
    main()
