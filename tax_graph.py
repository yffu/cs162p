import json
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TaxGraph:

    _tax_config = None
    
    def __init__(self):

        TaxGraph.tax_config('tax_config_fed.json')
        root = tk.Tk()
        root.title('Tax Graph')
        root.geometry('960x540')
        row_frame = tk.Frame(root)
        row_frame.pack()

        label = tk.Label(row_frame, text = 'Filing Status: ')
        label.pack(side = 'left', anchor = 'center')
        filing_statuses = TaxGraph._tax_config['filing_statuses']
        filing_stat = tk.StringVar(root)
        filing_stat.set(filing_statuses[0])
        dropdown = tk.OptionMenu(row_frame, filing_stat, *filing_statuses, command=self.update_plot)
        dropdown.pack(side = 'right', anchor = 'center')

        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_plot(filing_stat.get())
        root.mainloop()

    def update_plot(self, filing_status):
        tax_coord = self.get_coordinates_by_fs(filing_status)

        self.axes.clear()
        self.axes.set_title('Tax and Net Pay vs. Biweekly Income for Married Filing Status')
        self.axes.stackplot(*tax_coord, labels = ['Net Pay', 'Federal Tax'], colors = ['#002A84', '#F2A900'], edgecolor='white')
        self.axes.legend(loc='upper left')
        self.axes.set_xlabel('Biweekly Adjusted Gross Income')
        self.canvas.draw()

    def get_coordinates_by_fs(self, filing_status):
        tax_coord = list()
        adjusted_gross_hi = int(TaxGraph._tax_config['withholding_schedules'][filing_status][-1][0] * 1.2)
        x_range = range(0, adjusted_gross_hi, 50)
        y_tax_fed = [self.calc_tax(filing_status, x, TaxGraph._tax_config) for x in x_range]
        y_net_pay = [x_grs - y_tax for x_grs, y_tax in zip(x_range, y_tax_fed)]
        tax_coord = [x_range, y_net_pay, y_tax_fed]
        return tax_coord


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

    @classmethod
    def tax_config(cls, fn_config):
        if cls._tax_config is None:
            with open(fn_config) as f:
                cls._tax_config = json.load(f)


    @classmethod
    def calc_tax(cls, filing_status, adjusted_gross, tax_config):
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
        #print('filing_status', filing_status, 'adjusted_gross', adjusted_gross, 'taxable_income', taxable_income, 'tax_amt', tax_amt)
        return tax_amt


if __name__ == '__main__':
    tax_graph = TaxGraph()
