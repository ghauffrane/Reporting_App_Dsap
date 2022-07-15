import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os

class Charts: 
    def __init__(self,  cycle_nbr, cycle_data, existing_variables):
        self.cycle_nbr = cycle_nbr
        self.cycle_data = cycle_data.copy().set_index(cycle_data["ts "])
        self.time_col_name = "ts "
        self.var_col_names = existing_variables

    
    def unichart(self, varnames, phase, output_dir): 
        phase_dict = { "filling": "1521.2 Filling cycle running status  (Pause = 0)", 
                "dewatering": "1531.2 Dewatering cycle running status  (Pause = 0)", 
                "pressing": "1541.2 Pressing  cycle running status  (Pause = 0)", 
                "drying": "1551.2 Drying cycle running status  (Pause = 0)"}
        
        filling_slice = self.cycle_data[self.time_col_name][self.cycle_data["1521.2 Filling cycle running status  (Pause = 0)"] == 1.0]
        dewatering_slice = self.cycle_data[self.time_col_name][self.cycle_data["1531.2 Dewatering cycle running status  (Pause = 0)"] == 1.0]
        press_slice = self.cycle_data[self.time_col_name][self.cycle_data["1541.2 Pressing  cycle running status  (Pause = 0)"] == 1.0]
        dry_slice = self.cycle_data[self.time_col_name][self.cycle_data["1551.2 Drying cycle running status  (Pause = 0)"] == 1.0]
        
        filling_idx = filling_slice[0] if len(filling_slice) > 0 else None
        dewatering_idx = dewatering_slice[0] if len(dewatering_slice) > 0 else None
        pressing_idx = press_slice[0] if len(press_slice) > 0 else None
        dry_idx = dry_slice[0] if len(dry_slice) > 0 else None
        vlines_list = []
        for idx in [filling_idx, dewatering_idx, pressing_idx, dry_idx]: 
            if idx != None:
                vlines_list.append(idx)

        ymin = np.array([self.cycle_data[vr].min() for vr in varnames]).min()
        ymax = np.array([self.cycle_data[vr].max() for vr in varnames]).max()


        fig, ax = plt.subplots(1, 1, figsize = (10,10))
        plot_label = varnames[0].split("-")[-1]

        if phase in phase_dict.keys(): 

            ax.plot(self.cycle_data[varnames[0]][self.cycle_data[phase_dict[phase]]==1.0], label = plot_label)
        
        elif phase == "all": 
            ax.plot(self.cycle_data[varnames[0]], label = plot_label)
            ax.vlines(x = vlines_list, ymin = ymin, ymax = ymax, color = 'red', linestyles="dotted")
            if filling_idx != None: 
                plt.text(filling_idx, ymax/2,'filling', c= 'red')
            if dewatering_idx != None: 
                plt.text(dewatering_idx, ymax/2,'dewatering', c= 'red')
            if pressing_idx != None: 
                plt.text(pressing_idx, ymax/4,'pressing', c= 'red')
            if dry_idx != None:
                plt.text(dry_idx, ymax/2,'drying', color = 'red')
        plt.xlabel("Time")
        ax.set_ylabel(plot_label)

        plt.title(f"{plot_label} - phase: {phase}")
        plt.gca().xaxis.set_major_locator(mdates.DayLocator((1,15)))
        # plt.gca().yaxis.set_major_locator(mdates.DayLocator((1,15)))
        plt.gcf().autofmt_xdate()
        #plt.subplots_adjust(bottom= 0.1, left = 0.1)
        ax.legend(loc = "upper left")
        savepath = os.path.normpath(f"{output_dir}/{plot_label} - phase: {phase} - cycle: {self.cycle_nbr}.png")
        plt.savefig(savepath)
        plt.close()
        
        return savepath


    def bichart(self, varnames, phase, output_dir):

        plot_label0 = varnames[0].split("-")[-1]
        plot_label1 = varnames[1].split("-")[-1]

        phase_dict = { "filling": "1521.2 Filling cycle running status  (Pause = 0)", 
                        "dewatering": "1531.2 Dewatering cycle running status  (Pause = 0)", 
                        "pressing": "1541.2 Pressing  cycle running status  (Pause = 0)", 
                        "drying": "1551.2 Drying cycle running status  (Pause = 0)"}
        
        filling_slice = self.cycle_data[self.time_col_name][self.cycle_data["1521.2 Filling cycle running status  (Pause = 0)"] == 1.0]
        dewatering_slice = self.cycle_data[self.time_col_name][self.cycle_data["1531.2 Dewatering cycle running status  (Pause = 0)"] == 1.0]
        press_slice = self.cycle_data[self.time_col_name][self.cycle_data["1541.2 Pressing  cycle running status  (Pause = 0)"] == 1.0]
        dry_slice = self.cycle_data[self.time_col_name][self.cycle_data["1551.2 Drying cycle running status  (Pause = 0)"] == 1.0]
        filling_idx = filling_slice[0] if len(filling_slice) > 0 else None
        dewatering_idx = dewatering_slice[0] if len(dewatering_slice) > 0 else None
        pressing_idx = press_slice[0] if len(press_slice) > 0 else None
        dry_idx = dry_slice[0] if len(dry_slice) > 0 else None
        vlines_list = []
        for idx in [filling_idx, dewatering_idx, pressing_idx, dry_idx]: 
            if idx != None:
                vlines_list.append(idx)

        ymin = np.array([self.cycle_data[vr].min() for vr in varnames]).min()
        ymax = np.array([self.cycle_data[vr].max() for vr in varnames]).max()


        fig, ax = plt.subplots(1, 1, figsize = (10, 10))
        ax2 = ax.twinx()
        if phase in phase_dict.keys(): 
            ax.plot(self.cycle_data[varnames[0]][self.cycle_data[phase_dict[phase]]==1.0], label = plot_label0, c = 'green')
            ax2.plot(self.cycle_data[varnames[1]][self.cycle_data[phase_dict[phase]]==1.0], label = plot_label1, c = 'blue')
        elif phase == "all": 
            ax.plot(self.cycle_data[varnames[0]], label = plot_label0, c = 'green')
            ax2.plot(self.cycle_data[varnames[1]], label = plot_label1, c = 'blue')
            ax.vlines(x = vlines_list, ymin = ymin, ymax = ymax, color = 'red', linestyles="dotted")
            if filling_idx != None: 
                plt.text(filling_idx, ymax/2,'filling', c= 'red')
            if dewatering_idx != None: 
                plt.text(dewatering_idx, ymax/2,'dewatering', c= 'red')
            if pressing_idx != None: 
                plt.text(pressing_idx, ymax/4,'pressing', c= 'red')
            if dry_idx != None:
                plt.text(dry_idx, ymax/2,'drying', color = 'red')
        plt.xlabel("Time")
        ax.set_ylabel(plot_label0)
        ax2.set_ylabel(plot_label1)
        plt.title(f"{plot_label0} & {plot_label1} - phase: {phase}")
        plt.gca().xaxis.set_major_locator(mdates.DayLocator((1,15)))
        # plt.gca().yaxis.set_major_locator(mdates.DayLocator((1,15)))
        plt.gcf().autofmt_xdate()
        #plt.subplots_adjust(bottom= 0.1, left = 0.1)
        ax.legend(loc = "upper left")
        ax2.legend(loc = "lower left")
        savepath = os.path.normpath(f"{output_dir}/{plot_label0} & {plot_label1} - phase: {phase} - cycle: {self.cycle_nbr}.png")
        plt.savefig(savepath)
        plt.close()
        return savepath  