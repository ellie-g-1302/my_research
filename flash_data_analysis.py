# This is going to be a module to do data analysis and post processing for FLASH. This is developed and maintained by Ellie McGhee elizabeth.mcghee@slu.edu
# The dependancies needed are quality_of_life (https://github.com/ThomasLastName/quality_of_life) which has its own dependancies, pandas, numpy, yt, and matplolib
# This is specifically tailored for the ZPinch simulation of FLASH
import matplotlib.pyplot as plt
from quality_of_life import my_visualization_utils as mvu
import os
import pandas as pd
import numpy as np
import yt

class post_process_flash:
    # What this functions does is simply loads the particular plot file data generated from the simulation using YT
    def load_data(self, my_plot_file_name):
        ds = yt.load(my_plot_file_name)
        return ds
    
    # This generates a Slice plot using YT
    def make_SlicePlot(self, my_plot_file_name, my_var, slice_direction,  my_color = "hot"):
        ds = post_process_flash.load_data(self, my_plot_file_name)
        # this below sets the units. I only have this so far for the ZPInch simulation. 
        if my_var == "pion" or my_var == "pele" or my_var == "magp":
            units = "g/(cm*s**2)"
            if my_var == "pion":
                title = "Ion Pressure"
            elif my_var == "pele":
                title = "Electron Pressure"
            elif my_var == "magp":
                title = "Magnetic Field Squared"   
        elif my_var == "magz":
            units = "Gauss"
            title = "Magnetic Field"
        elif my_var == "tion":
            units = "kelvin"
            title = "Ion Temperature"
        elif my_var == "velx":
            units = "cm/s"
            title = "Velocity in x direction"
        elif my_var == "dens":
            units = "g/cm**3"
            title = "Density"
        elif my_var == "res2": # Resisitivity doesn't have any base units and I'm not sure how to override it
                title = "Resisitivity"
        
        if my_var == "res2":
            slc = yt.SlicePlot(ds, slice_direction, ("flash", my_var))    
            slc.annotate_title(title)
            slc.set_cmap(field=("flash", my_var), cmap = my_color)  
            slc.save()    # Something to work on is how to save it to a particular path
                
        else:
            slc = yt.SlicePlot(ds, slice_direction, ("flash", my_var))    
            slc.annotate_title(title)
            slc.set_cmap(field=("flash", my_var), cmap = my_color)  
            slc.set_unit(("flash", my_var), units)
            slc.save()    # Something to work on is how to save it to a particular path. This just saves it to a particular directory where you're working
      
    # This is a function to store the data as a CSV and has the option to return a list of the data, which is by default false      
    def save_plot_file_to_csv(self, my_plot_file_name, my_var, return_to_list = False, name_of_csv = "my_file.csv"):
        ds = post_process_flash.load_data(self, my_plot_file_name)
        ad = ds.all_data()
        var = ad[("flash", my_var)]
        
        df = pd.DataFrame(var)
        missing_val = str(list(df.columns))
        missing_val = missing_val.replace("[", "")
        missing_val = missing_val.replace("]", "")
        missing_val = float(missing_val)
        df.loc[-1] = missing_val
        df.index = df.index + 1
        df = df.sort_index()
        df = df.rename(columns={missing_val: my_var})
        df.to_csv(name_of_csv)
        
        if return_to_list == True:
            f = open(name_of_csv, "r")
            my_index = []
            my_y_data = []
            my_list = []
            for x in f:
                val = x.split(",")
                my_y_data.append(val[1])
                my_index.append(val[0])
            
            my_y_data.pop(0)
            my_index.pop(0)
        
            my_list.append(my_index)
            my_list.append(my_y_data)
        
            for i in range(len(my_list)):
                for j in range(len(my_list[i])):
                    my_list[i][j] = float(my_list[i][j])
                
            return my_list
        elif return_to_list == False:
            return 0
        
     # this returns the trajectory file as a list  
    def get_trajectory(self, my_trajectory_file):
        f = open(my_trajectory_file, "r")
        my_list = []
        my_time = []
        my_vel_in = []
        my_rinn = []
        my_vel_out = []
        my_rout = []
        
        for x in f:
            val = x.split(",")
            my_time.append(val[1])                
            my_rinn.append(val[2])
            my_vel_in.append(val[3])
            my_rout.append(val[4])
            my_vel_out.append(val[5])
            
        my_time.pop(0)
        my_time.pop(0)
        my_rinn.pop(0)
        my_vel_in.pop(0)
        my_rout.pop(0)
        my_vel_out.pop(0)
        
        for i in range(len(my_time)):
            my_time[i] = float(my_time[i])
            my_rinn[i] = float(my_rinn[i])
            my_vel_in[i] = float(my_vel_in[i])
            my_rout[i] = float(my_rout[i])
            my_vel_out[i] = float(my_vel_out[i])
            
        my_list.append(my_time)
        my_list.append(my_rinn)
        my_list.append(my_vel_in)
        my_list.append(my_rout)
        my_list.append(my_vel_out)
        
        return my_list
    
    # Okay now the very difficult one: making a gif from the data using Tom's module -----------------------------------------------------------------
    def make_gif_from_data(self, default_dir, my_file_prefix, num_of_plot_files, my_var, my_label, num_data,
                        color2 = None, my_label2 = None, my_var2 = None, color3 = None, my_label3 = None, my_var3 = None,
                        name_of_gif = "MyGif", color = "c", scale_val = None, 
                        scale_min = None, scale_max = None, my_scale = "linear", 
                        my_y_label = "My Data", change_dir = False, my_second_dir = None, 
                        my_third_dir = None):
        # What this does first is iterate over number of plot file to get the proper name
        my_index = []
        my_y_value = []
        
        my_y_value_2 = []
        my_y_value_3 = []
        for i in range(num_of_plot_files):
            if i < 10:
                file_name = my_file_prefix + "00" + str(i) 
            elif i >= 10 and i < 100:
                file_name = my_file_prefix + "0" + str(i) 
            elif i >= 100:
                file_name = my_file_prefix + str(i) 
            
            if num_data == 1:
                os.chdir(default_dir)
                my_csv_list = post_process_flash.save_plot_file_to_csv(self, file_name, my_var, return_to_list = True)
                my_index.append(my_csv_list[0]) #This saves the index in one list
                my_y_value.append(my_csv_list[1]) # This saves the actual variable data in another
            if num_data == 2:
                if change_dir == True:
                    if my_second_dir == None:
                        print("Error: No second directory input")
                    else: 
                        os.chdir(default_dir)
                        my_csv_list = post_process_flash.save_plot_file_to_csv(self, file_name, my_var, return_to_list = True)
                        os.chdir(my_second_dir)
                        my_csv_list_2 = post_process_flash.save_plot_file_to_csv(self, file_name, my_var2, return_to_list = True)
                        os.chdir(default_dir)
                        my_index.append(my_csv_list[0]) #This saves the index in one list
                        my_y_value.append(my_csv_list[1]) # This saves the actual variable data in another
                        my_y_value_2.append(my_csv_list_2[1])
                elif change_dir == False:
                    os.chdir(default_dir)
                    my_csv_list = post_process_flash.save_plot_file_to_csv(self, file_name, my_var, return_to_list = True)
                    my_csv_list_2 = post_process_flash.save_plot_file_to_csv(self, file_name, my_var2, return_to_list = True)
                    my_index.append(my_csv_list[0]) #This saves the index in one list
                    my_y_value.append(my_csv_list[1]) # This saves the actual variable data in another
                    my_y_value_2.append(my_csv_list_2[1])
            elif num_data == 3:
                if change_dir == True:
                    my_csv_list = post_process_flash.save_plot_file_to_csv(self, file_name, my_var, return_to_list = True)
                    os.chdir(my_second_dir)
                    my_csv_list_2 = post_process_flash.save_plot_file_to_csv(self, file_name, my_var2, return_to_list = True)
                    os.chdir(my_third_dir)
                    my_csv_list_3 = post_process_flash.save_plot_file_to_csv(self, file_name, my_var3, return_to_list= True)
                    os.chdir(default_dir)
                    my_index.append(my_csv_list[0]) #This saves the index in one list
                    my_y_value.append(my_csv_list[1]) # This saves the actual variable data in another
                    my_y_value_2.append(my_csv_list_2[1])
                    my_y_value_3.append(my_csv_list_3[1])
                elif change_dir == False:
                    os.chdir(default_dir)
                    my_csv_list = post_process_flash.save_plot_file_to_csv(self, file_name, my_var, return_to_list = True)
                    my_csv_list_2 = post_process_flash.save_plot_file_to_csv(self, file_name, my_var2, return_to_list = True)
                    my_csv_list_3 = post_process_flash.save_plot_file_to_csv(self, file_name, my_var3, return_to_list= True)
                    my_index.append(my_csv_list[0]) #This saves the index in one list
                    my_y_value.append(my_csv_list[1]) # This saves the actual variable data in another
                    my_y_value_2.append(my_csv_list_2[1])
                    my_y_value_3.append(my_csv_list_3[1])
            elif num_data < 1 or num_data > 3:
                print("Error: Invalid number of data files")
        
        gif = mvu.GifMaker(name_of_gif, ram_only=False)
        
        for i in range(num_of_plot_files):
            if num_data == 1:
                _ = plt.plot(my_index[i], my_y_value[i], color, label = my_label)
                if scale_val == True:
                    _ = plt.xlim([0, 256])
                    _ = plt.ylim([scale_min, scale_max])
                    _ = plt.ylabel(my_y_label)
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()

                else:
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(my_y_label)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()
            elif num_data == 2:
                _ = plt.plot(my_index[i], my_y_value[i], color, label = my_label)
                _ = plt.plot(my_index[i], my_y_value_2[i], color2, label = my_label2)
                if scale_val == True:
                    _ = plt.xlim([0, 256])
                    _ = plt.ylim([scale_min, scale_max])
                    _ = plt.ylabel(my_y_label)
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()

                else:
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(my_y_label)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()
            elif num_data == 2:
                _ = plt.plot(my_index[i], my_y_value[i], color, label = my_label)
                _ = plt.plot(my_index[i], my_y_value_2[i], color2, label = my_label2)
                _ = plt.plot(my_index[i], my_y_value_2[i], color3, label = my_label3)
                if scale_val == True:
                    _ = plt.xlim([0, 256])
                    _ = plt.ylim([scale_min, scale_max])
                    _ = plt.ylabel(my_y_label)
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()
                    
                else:
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(my_y_label)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()
            elif num_data < 1 or num_data > 3:
                print("Error: Invalid number of plot files")
            
        gif.develop(total_duration=10.0)
        
# Okay so it seems like its working. Yay!