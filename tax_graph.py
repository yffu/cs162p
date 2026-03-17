"""
Tax Graph
_____________
This program will display a stacked line chart of net pay and tax amount for a range of biweekly wage amounts.

Author: Yuanfang Fu
Date: March 2026
Dependencies: tkinter, matplotlib, json
"""

import json
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TaxGraph:

    _tax_config = None
    
    def __init__(self):
        """Creates tk window, dropdown selector, matplotlib graph, and enters mainloop to listen for changes"""
        TaxGraph.load_tax_config('tax_config_fed.json')
        root = tk.Tk()
        root.title('Tax Graph')
        root.geometry('960x540')
        row_frame = tk.Frame(root)
        row_frame.pack()

        label = tk.Label(row_frame, text = 'Filing Status: ')
        label.pack(side = 'left', anchor = 'center')
        filing_statuses = self.tax_config['filing_statuses']
        filing_stat = tk.StringVar(root)
        filing_stat.set(filing_statuses[0])
        dropdown = tk.OptionMenu(row_frame, filing_stat, *filing_statuses, command=self.update_plot)
        dropdown.pack(side = 'right', anchor = 'center')

        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.axes.set_title('Tax and Net Pay vs. Biweekly Income')
        self.axes.set_xlabel('Biweekly Adjusted Gross Income')
        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tax_pts_store = dict()
        self.update_plot(filing_stat.get())
        root.mainloop()

    def update_plot(self, filing_status):
        """Gets tax coordinates for the filing status, and updates the graph with the coordinates"""
        tax_coord = self.get_coordinates_by_fs(filing_status)

        self.axes.clear()
        self.axes.stackplot(*tax_coord, labels = ['Net Pay', 'Federal Tax', 'State (CA) Tax'], colors = ['#002A84', '#F2A900', '#FFC133'], edgecolor='white')
        self.axes.legend(loc='upper left')
        self.canvas.draw()

    def get_coordinates_by_fs(self, filing_status):
        """Checks if tax coordinates exists in store for the filing status - if not create list of adjusted gross as x values,
        Calculates tax from adjusted gross, and net pay as difference of adjusted gross and tax"""
        tax_pts = self.tax_pts_store.get(filing_status)
        if tax_pts:
            print('tax points found in store')
        else:
            adjusted_gross_hi = int(self.tax_config['withholding_schedules'][filing_status][-1][0] * 1.2)
            x_range = range(0, adjusted_gross_hi, 50)
            y_tax_fed = [self.calc_tax(filing_status, x, self.tax_config) for x in x_range]
            y_net_pay = [x_grs - y_tax for x_grs, y_tax in zip(x_range, y_tax_fed)]
            tax_pts = [x_range, y_net_pay, y_tax_fed]
            self.tax_pts_store[filing_status] = tax_pts
        return tax_pts


    @property
    def axes(self):
        return self.__axes

    @axes.setter
    def axes(self, a):
        self.__axes = a

    @property
    def canvas(self):
        return self.__canvas

    @canvas.setter
    def canvas(self, c):
        self.__canvas = c

    @property
    def tax_pts_store(self):
        return self.__tax_pts_store

    @tax_pts_store.setter
    def tax_pts_store(self, tps):
        self.__tax_pts_store = tps

    @property
    def tax_config(self):
        return self._tax_config
    
    @classmethod
    def load_tax_config(cls, fn_config):
        """Load federal tax configuration from json to class variable"""
        if cls._tax_config is None:
            with open(fn_config) as f:
                cls._tax_config = json.load(f)


    @classmethod
    def calc_tax(cls, filing_status, adjusted_gross, tax_config):
        """Calculates taxable income from adjusted gross, finds the correct withholding rate and calculates tax withholding"""
        tax_brackets = tax_config['withholding_schedules'][filing_status]
        std_ded = tax_config['standard_deductions'][filing_status]
        # gross_pay - pre-tax deductions - standard_deduction = taxable_income
        taxable_income = max(adjusted_gross - std_ded, 0)
        tax_amt = None
        for tb in tax_brackets:
            if taxable_income >= tb[0] and (tb[1] is None or taxable_income <= tb[1]):
                # tax_amt = base_withholding + (taxable_income - over) * rate)
                tax_amt = round(tb[2] + (taxable_income - tb[0]) * tb[3], 2)
                break
        return tax_amt


class TaxGraphSte(TaxGraph):

    _tax_config_ste = None

    @classmethod
    def load_tax_config_ste(cls, fn_config):
        """Load state tax configuration from json to class variable"""
        if cls._tax_config is None:
            with open(fn_config) as f:
                cls._tax_config_ste = json.load(f)

    def __init__(self, fn_config):
        """"Calls init method of superclass, and just loads additional state tax configuration"""
        TaxGraphSte.load_tax_config_ste(fn_config)
        super().__init__()

    def get_coordinates_by_fs(self, filing_status):
        """Calls get coordinates of superclass, calculates list of state tax withholding from state tax config,
        subtracts state tax withholding from net pay and returns the updated tax points"""
        tax_pts = super().get_coordinates_by_fs(filing_status)
        if len(tax_pts) == 3:
            y_tax_ste = [self.calc_tax(filing_status, x, self.tax_config_ste) for x in tax_pts[0]]
            y_net_pay = [y_net - y_tax for y_net, y_tax in zip(tax_pts[1], y_tax_ste)]
            tax_pts[1] = y_net_pay
            tax_pts.append(y_tax_ste)
        return tax_pts

    @property
    def tax_config_ste(self):
        return self._tax_config_ste
        

if __name__ == '__main__':
    # tax_graph = TaxGraph()
    tax_graph = TaxGraphSte('tax_config_ca.json')
