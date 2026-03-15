# Tax Graph
This program will display a stacked line chart of net pay and tax amount for a range of biweekly wage amounts.

---

## How to Run
### In a terminal

1. Go to the project root directory, and install the required library.
```
   pip install matplotlib
```

2. Check the .json file(s) are in the same place as the .py file. Run the program.
```
   python tax_graph.py
```
3. Select a value in 'Filing Status' dropdown to display the graph for that filing status.
---

## Videos
- [Code Demo](https://youtu.be/ClrJi3jS8HU)
- [Code Walkthrough](https://youtu.be/PnJfQ-UDA8g)

---

## Citations

This project uses the following libraries and assets.

| Library / Asset                       | License Type                     | Usage               |
|:------------------------------------- |:---------------------------------|:--------------------|
| [matplotlib](https://matplotlib.org)  | PSF (Python Software Foundation) | chart visualization |
| [Tkinter](https://tkdocs.com/)        | CC BY-NC-SA 4.0                  | gui toolkit         |
| [json](https://docs.python.org/3/library/json.html)           | PSF (Python Software Foundation) | data format         |
---

## Tutorials, Documentation, and Code Referenced
- [Publication 15-T](https://www.irs.gov/pub/irs-pdf/p15t.pdf) for 2026 Percentage Method Tables BIWEEKLY Payroll Period
- [Form W-4](https://www.irs.gov/pub/irs-pdf/fw4.pdf) for 2026 Standard Deductions
- [California Withholding Schedules for 2026](https://edd.ca.gov/siteassets/files/pdf_pub_ctr/26methb.pdf) for Bi-weekly Payroll Period Tax Rate Tables
