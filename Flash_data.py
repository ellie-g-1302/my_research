# This is a class that will allow the user to load FLASH data into a useable form. Maintained by Ellie McGhee
# -----------------------------------------------------------------------------------------------------------
# Dependancies needed: yt, numpy, pandas, matplotlib, scikit-learn, quality_of_life, pytorch, tensorflow

from quality_of_life import my_visualization_utils as mvu
import yt
import pandas as pd
import matplotlib.pyplot as plt

class Flash_Data:
    def __init__(self, plot_file_to_load, slice_direction = "z", my_var = None, 
                 my_color = "hot", name_of_csv = "my_file.csv", my_trajectory_file = None):
        self.plot_file_to_load = plot_file_to_load
        self.slice_direction = slice_direction
        self.my_var = my_var
        self.my_color = my_color
        self.name_of_csv = name_of_csv
        self.my_trajectory_file = my_trajectory_file
        
    # This function just loads the data ----------------------------------------------------------------------
    def load_data(self):
        ds = yt.load(self.my_file)
        return ds
    
    # This generates a Slice Plot from yt --------------------------------------------------------------------
    def make_SlicePlot(self):
        ds = Flash_Data.load_data(self)
        
        if self.my_var == None:
            print("Error. No variable input")
        else:      
            if self.my_var == "pion" or self.my_var == "pele" or self.my_var == "magp":
                units = "g/(cm*s**2)"
                if self.my_var == "pion":
                    title = "Ion Pressure"
                elif self.my_var == "pele":
                    title = "Electron Pressure"
                elif self.my_var == "magp":
                    title = "Magnetic Field Squared"   
            elif self.my_var == "magz":
                units = "Gauss"
                title = "Magnetic Field"
            elif self.my_var == "tion":
                units = "kelvin"
                title = "Ion Temperature"
            elif self.my_var == "velx":
                units = "cm/s"
                title = "Velocity in x direction"
            elif self.my_var == "dens":
                units = "g/cm**3"
                title = "Density"
            elif self.my_var == "res2":
                title = "Resisitivity"  # This variable doesn't generate any units for some reason and 
                                        # I'm not sure how to manually override it
            # Now let's actually make the plots -----------------------------------------------------------------
            
            if self.my_var == "res2":
                slc = yt.SlicePlot(ds, self.slice_direction, ("flash", self.my_var))    
                slc.annotate_title(title)
                slc.set_cmap(field=("flash", self.my_var), cmap = self.my_color)  
                slc.save()    # Something to work on is how to save it to a particular path
                
            else:
                slc = yt.SlicePlot(ds, self.slice_direction, ("flash", self.my_var))    
                slc.annotate_title(title)
                slc.set_cmap(field=("flash", self.my_var), cmap = self.my_color)  
                slc.set_unit(("flash", self.my_var), units)
                slc.save()    # Something to work on is how to save it to a particular path

    # This function will svae the plot files as a CSV file ----------------------------------------------------
    def save_plot_file_to_csv(self):
        ds = Flash_Data.load_data(self)
        
        ad = ds.all_data()
        var = ad[("flash", self.my_var)]
        
        df = pd.DataFrame(var)
        missing_val = str(list(df.columns))
        missing_val = missing_val.replace("[", "")
        missing_val = missing_val.replace("]", "")
        missing_val = float(missing_val)
        df.loc[-1] = missing_val
        df.index = df.index + 1
        df = df.sort_index()
        df = df.rename(columns={missing_val: self.my_var})
        df.to_csv(self.name_of_csv)
        
    # Now this function will return the CSV data as a list -----------------------------------------------------------------
    def make_csv_to_list(self):
        my_csv = Flash_Data.save_plot_file_to_csv(self)
        f = open(my_csv, "r")
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
    
    def get_trajectory(self):
        if self.my_trajectory_file == None:
            print("Error: No Trajectory file input.")
        else:
            f = open(self.my_trajectory_file, "r")
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