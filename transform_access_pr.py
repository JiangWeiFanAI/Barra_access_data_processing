import os
import data_processing_tool as dpt
from datetime import timedelta, date, datetime
# import args_parameter as args
import numpy as np


import time
import xarray as xr

import data_processing_tool as dpt
import netCDF4 as nc
from netCDF4 import Dataset, num2date, date2num

import platform 


def get_filename_with_no_time_order(rootdir):
    '''get filename first and generate label '''
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i],)
        if os.path.isdir(path):
            _files.extend(get_filename_with_no_time_order(path))
        if os.path.isfile(path):
            if path[-3:]==".nc":
                _files.append(path)
    return _files


def get_filename_with_time_order(rootdir,ensemble,dates,var_name):
    '''get filename first and generate label ,one different w'''
    _files = []
    for en in ensemble:
        for date in dates:
            access_path=rootdir+en+"/"+"da_"+var_name+"_"+date.strftime("%Y%m%d")+"_"+en+".nc"
#             print(access_path)
            if os.path.exists(access_path):
#                 print(access_path)
                path=[access_path]
                path.append(en)
                path.append(date)
                _files.append(path)

#最后去掉第一行，然后shuffle
#     if nine2nine and date_minus_one==1:
#         del _files[0]
    return _files



def main():
    import netCDF4 as nc
    sys = platform.system()
    init_date=date(1970, 1, 1)
    start_date=date(1990, 1, 1)
    end_date=date(2012,12,25) #if 929 is true we should substract 1 day  
    if sys == "Windows":
        init_date=date(1970, 1, 1)
        start_date=date(1990, 1, 1)
        end_date=date(2012,12,25) #if 929 is true we should substract 1 day   
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

        
    nine2nine=True
    date_minus_one=1
    leading_time_we_use=7
    ensemble=['e10','e11']

    var_name="pr"
    dates=[start_date + timedelta(x) for x in range((end_date - start_date).days + 1)]
    file_list=get_filename_with_time_order(file_ACCESS_dir+var_name+'/daily/',ensemble,dates,var_name)
    time_leading=7

    lat_name="lat"
    lon_name="lon"

#     print(file_list)
    for i in file_list:
#         print(i)
        data = Dataset(i[0], 'r')
        var = data[var_name][:7,82:144,134:188]
        lat = data[lat_name][:][82:144]
        lon = data[lon_name][:][134:188]
#         print(var.shape)
        data.close()
    #         lr=dpt.read_access_data(i,idx=time_leading).data[82:144,134:188]*86400
        result=np.zeros((7,79,94))
        for idx,j in enumerate(var):
            result[idx]=dpt.interp_tensor_2d(j,(79,94))


        if not os.path.exists('../data/'+var_name+'/daily/'+i[1]):
            os.mkdir('../data/'+var_name+'/daily/'+i[1])
        
        f_w = nc.Dataset('../data/'+var_name+'/daily/'+i[1]+"/da_"+var_name+"_"+i[2].strftime("%Y%m%d")+"_"+i[1]+'.nc','w',format = 'NETCDF4')
        f_w.createDimension('lat',79)
        f_w.createDimension('lon',94)
        f_w.createDimension('time',time_leading)

        f_w.createVariable('lat',np.float32,('lat'))
        f_w.createVariable('lon',np.float32,('lon'))
        f_w.createVariable('time',np.int,('time'))



        f_w.variables['lat'][:] = np.zeros((79))
        f_w.variables['lon'][:] =  np.zeros((94))
        f_w.variables['time'][:] =  np.zeros((7))


        f_w.createVariable( var_name, np.float32, ('time','lat','lon'))
        f_w.variables[var_name][:] = result

        f_w.close()
               

    
            

    
            
if __name__=='__main__':
    main()
