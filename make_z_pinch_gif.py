import matplotlib.pyplot as plt
from quality_of_life import my_visualization_utils as mvu
import Flash_data 
    
class make_z_pinch_gif:
    def __init__(self, my_var, name_of_csv = "my_file.csv"):
        self.name_of_csv = name_of_csv
        self.my_var = my_var
    
    def make_gif_4_max(my_file_1, my_label_1, num_plot_files, plot_num, name_of_gif, 
                    scale_val = None, scale_min = None, scale_max = None,
                    units = None, my_label_2 = None, my_label_3 = None, 
                    my_label_4 = None, my_file_2 = None, my_file_3 = None, 
                    my_file_4 = None, color_1 = "c", color_2 = "g", color_3 = "r", 
                    color_4 = "m", my_scale = "linear"):
        
        my_index = []
        my_y_values_1 = []
        my_y_values_2 = []
        my_y_values_3 = []
        my_y_values_4 = []

        for i in range(num_plot_files):
            if i < 10:
                if plot_num == 1:
                    file_1 = my_file_1 + "00" + str(i) + ".csv"
                elif plot_num == 2:
                    file_1 = my_file_1 + "00" + str(i) + ".csv"
                    file_2 = my_file_2 + "00" + str(i) + ".csv"
                elif plot_num == 3:
                    file_1 = my_file_1 + "00" + str(i) + ".csv"
                    file_2 = my_file_2 + "00" + str(i) + ".csv"
                    file_3 = my_file_3 + "00" + str(i) + ".csv"
                elif plot_num == 4:
                    file_1 = my_file_1 + "00" + str(i) + ".csv"
                    file_2 = my_file_2 + "00" + str(i) + ".csv"
                    file_3 = my_file_3 + "00" + str(i) + ".csv"
                    file_4 = my_file_4 + "00" + str(i) + ".csv"
            elif i >= 10 and i < 100:
                if plot_num == 1:
                    file_1 = my_file_1 + "0" + str(i) + ".csv"
                elif plot_num == 2:
                    file_1 = my_file_1 + "0" + str(i) + ".csv"
                    file_2 = my_file_2 + "0" + str(i) + ".csv"
                elif plot_num == 3:
                    file_1 = my_file_1 + "0" + str(i) + ".csv"
                    file_2 = my_file_2 + "0" + str(i) + ".csv"
                    file_3 = my_file_3 + "0" + str(i) + ".csv"
                elif plot_num == 4:
                    file_1 = my_file_1 + "0" + str(i) + ".csv"
                    file_2 = my_file_2 + "0" + str(i) + ".csv"
                    file_3 = my_file_3 + "0" + str(i) + ".csv"
                    file_4 = my_file_4 + "0" + str(i) + ".csv"

            elif i >= 100:
                if plot_num == 1:
                    file_1 = my_file_1 + str(i) + ".csv"
                elif plot_num == 2:
                    file_1 = my_file_1 + str(i) + ".csv"
                    file_2 = my_file_2 + str(i) + ".csv"
                elif plot_num == 3:
                    file_1 = my_file_1 + str(i) + ".csv"
                    file_2 = my_file_2 + str(i) + ".csv"
                    file_3 = my_file_3 + str(i) + ".csv"
                elif plot_num == 4:
                    file_1 = my_file_1 + str(i) + ".csv"
                    file_2 = my_file_2 + str(i) + ".csv"
                    file_3 = my_file_3 + str(i) + ".csv"
                    file_4 = my_file_4 + str(i) + ".csv"

            if plot_num == 1:
                my_csv_data_1 = Flash_data(file_1).make_csv_to_list()
                my_index.append(my_csv_data_1[0])
                my_y_values_1.append(my_csv_data_1[1])
            elif plot_num == 2:
                my_csv_data_1 = Flash_data(file_1).make_csv_to_list()
                my_csv_data_2 = Flash_data(file_2).make_csv_to_list()
                my_index.append(my_csv_data_1[0])

                my_y_values_1.append(my_csv_data_1[1])
                my_y_values_2.append(my_csv_data_2[1])
            elif plot_num == 3:
                my_csv_data_1 = Flash_data(file_1).make_csv_to_list()
                my_csv_data_2 = Flash_data(file_2).make_csv_to_list()
                my_csv_data_3 = Flash_data(file_3).make_csv_to_list()

                my_index.append(my_csv_data_1[0])

                my_y_values_1.append(my_csv_data_1[1])
                my_y_values_2.append(my_csv_data_2[1])
                my_y_values_3.append(my_csv_data_3[1])
            elif plot_num == 4:
                my_csv_data_1 = Flash_data(file_1).make_csv_to_list()
                my_csv_data_2 = Flash_data(file_2).make_csv_to_list()
                my_csv_data_3 = Flash_data(file_3).make_csv_to_list()
                my_csv_data_4 = Flash_data(file_4).make_csv_to_list()
                my_index.append(my_csv_data_1[0])

                my_y_values_1.append(my_csv_data_1[1])
                my_y_values_2.append(my_csv_data_2[1])
                my_y_values_3.append(my_csv_data_3[1])
                my_y_values_4.append(my_csv_data_4[1])

        gif = mvu.GifMaker(name_of_gif, ram_only=False)

        if plot_num == 1:
            for i in range(num_plot_files):
                _ = plt.plot(my_index[i], my_y_values_1[i], color_1, label = my_label_1)
                if scale_val == True:
                    _ = plt.xlim([0, 256])
                    _ = plt.ylim([scale_min, scale_max])

                else:
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(units)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()

        elif plot_num > 1 and plot_num <= 4:
            if plot_num == 2:
                for i in range(len(my_index)):
                    _ = plt.plot(my_index[i], my_y_values_1[i], color_1, label = my_label_1)
                    _ = plt.plot(my_index[i], my_y_values_2[i], color_2, label = my_label_2)
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(units)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()

            elif plot_num == 3:
                for i in range(len(my_index)):
                    _ = plt.plot(my_index[i], my_y_values_1[i], color_1, label = my_label_1)
                    _ = plt.plot(my_index[i], my_y_values_2[i], color_2, label = my_label_2)
                    _ = plt.plot(my_index[i], my_y_values_3[i], color_3, label = my_label_3)
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(units)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()

            elif plot_num == 4:
                for i in range(len(my_index)):
                    _ = plt.plot(my_index[i], my_y_values_1[i], color_1, label = my_label_1)
                    _ = plt.plot(my_index[i], my_y_values_2[i], color_2, label = my_label_2)
                    _ = plt.plot(my_index[i], my_y_values_3[i], color_3, label = my_label_3)
                    _ = plt.plot(my_index[i], my_y_values_4[i], color_4, label = my_label_4)
                    _ = plt.xlim([0, 256])
                    _ = plt.title(str(i) + " ns", loc = "right")
                    _ = plt.ylabel(units)
                    _ = plt.yscale(my_scale)
                    _ = plt.legend()
                    gif.capture()

            elif plot_num < 1 or plot_num > 4:
                print("Error. Invalid number of plot files")




        gif.develop(total_duration=10.0)

        return 0