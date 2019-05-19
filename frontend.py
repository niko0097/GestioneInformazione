#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from search_engine import *
import sys
import json
import ast

class UserInterface:
    # INITIALIZE ALL THE COMPONENTS FOR EVERY VIEW
    def __init__(self,window):
        self.window = window
        self.phrase_entry = Entry(self.window, width=22)
        self.table_entry = Entry(self.window, width=22)
        self.year_entry = Entry(self.window, width=22)
        self.text_field_cbb = ttk.Combobox(self.window, values=['authors','year','title'])
        self.venue_entry = Entry(self.window, width=22)
        self.venue_field_cbb = ttk.Combobox(self.window, values=['title','publisher','journal'])
        self.number_scale = Scale(from_=0, to=200, resolution=10, orient=HORIZONTAL, length=200)
        self.ranking_cbb = ttk.Combobox(self.window, values=['boolean','bm25','BM25'])
        self.required_label = Label(self.window, text="Required Fields", font="none 18 bold")
        self.phrase_label = Label(self.window, text="Phrase")
        self.table_label = Label(self.window, text="Table")
        self.optional_lable = Label(self.window, text="Optional Fields", font="none 18")
        self.year_table = Label(self.window, text="Year")
        self.text_field_label = Label(self.window, text="Text Field")
        self.venue_label = Label(self.window, text="Venue")
        self.venue_field_label = Label(self.window, text="Venue field")
        self.number_label = Label(self.window, text="Number of Records\n(Set 0 to see all records)", justify=LEFT)
        self.ranking_label = Label(self.window, text="Ranking Type")
        self.search_button = Button(self.window, text="SEARCH", font="none 14 bold", command=self.launch_query)

    # CALL THE SEARCH ENGINE PASSING THE PARAMETERS
    def launch_query(self):
        phrase = self.phrase_entry.get()
        table = self.table_entry.get()
# add more controls on input type (table)
        if(not phrase or not table):
            print('Error')
            return

        year = self.year_entry.get()
# if not int?
        if(year):
            year = int(year)
        else:
            year = None
        text_field = self.text_field_cbb.get()
        if (text_field == ""):
            text_field = None
        venue = self.venue_entry.get()
        if (venue == ""):
            venue = None
        venue_field = self.venue_field_cbb.get()
        if (venue_field == ""):
            venue_field = None
        ranking = self.ranking_cbb.get()
        if (ranking == ""):
            ranking = None
# set 0 = all results
        number = self.number_scale.get()

        print("\n\nNext Query includes the following parameters:\n"\
            "\nPhrase: " + phrase + "\nTable: " + table + "\nYear: " + str(year) + \
            "\nText Field: " + str(text_field) + "\nVenue: " + str(venue) + \
            "\nVenue Field: " + str(venue_field) + "\nNumber: " + str(number) + "\nRanking: " + str(ranking))

        SE = searchEng(phrase,
                        table,
                        year=year,
                        text_field=text_field,
                        venue=venue,
                        venue_field=venue_field,
                        ranking=ranking,
                        num=number)

        records = SE.interrogation()

        self.clearAll()
        self.printView(records)

    def printView(self,records):
        self.tree = ttk.Treeview(self.window)
        self.tree.heading('#0', text='Title')
        self.tree.column('#0', stretch=YES, width=1500)
        self.scrollbar = Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.i = 0
        for rec in records:
            self.tree.insert('', 'end', iid=self.i, text=rec['title'])
            self.tree.insert(self.i, 'end', text="Authors: " + rec['authors'])
            self.tree.insert(self.i, 'end', text="Year: " + rec['year'])
            self.tree.insert(self.i, 'end', text="URL: " + rec['url'])
            self.tree.item(self.i, open=True)
            # for key,val in rec.items():
            #     print(str(key) + " --> " + str(val))
            # print(json.dumps(ast.literal_eval(str(rec)), indent=4))
            self.i += 1

        self.tree.config(height=50)
        self.tree.grid(row=0, column=0, sticky=N+S)
        self.scrollbar.grid(row=0, column=1, sticky=N+S)

# CLEAR THE WHOLE WINDOW IN ORDER TO REUSE IT
    def clearAll(self):
        self.phrase_entry.grid_forget()
        self.table_entry.grid_forget()
        self.year_entry.grid_forget()
        self.text_field_cbb.grid_forget()
        self.venue_entry.grid_forget()
        self.venue_field_cbb.grid_forget()
        self.number_scale.grid_forget()
        self.ranking_cbb.grid_forget()
        self.required_label.grid_forget()
        self.phrase_label.grid_forget()
        self.table_label.grid_forget()
        self.optional_lable.grid_forget()
        self.year_table.grid_forget()
        self.text_field_label.grid_forget()
        self.venue_label.grid_forget()
        self.venue_field_label.grid_forget()
        self.number_label.grid_forget()
        self.ranking_label.grid_forget()
        self.search_button.grid_forget()

    # DISPLAY ALL THE COMPONENTS INSIDE THE WINDOW
    def display_search(self):
        # REQUIRED
        self.required_label.grid(row=0, columnspan=2, pady=10)

        self.phrase_label.grid(row=1, sticky=W, padx=5)
        self.phrase_entry.grid(row=1, column=1, pady=5, padx=10)

        self.table_label.grid(row=2, sticky=W, padx=5)
        self.table_entry.grid(row=2, column=1, pady=5)

        # OPTIONAL
        self.optional_lable.grid(row=3, columnspan=2, pady=10)

        self.year_table.grid(row=4, sticky=W, padx=5)
        self.year_entry.grid(row=4, column=1, pady=5)

        self.text_field_label.grid(row=5, sticky=W, padx=5)
        self.text_field_cbb.grid(row=5, column=1, pady=5)

        self.venue_label.grid(row=6, sticky=W, padx=5)
        self.venue_entry.grid(row=6, column=1, pady=5)

        self.venue_field_label.grid(row=7, sticky=W, padx=5)
        self.venue_field_cbb.grid(row=7, column=1, pady=5)

        self.number_label.grid(row=8, sticky=W, padx=5)
        self.number_scale.grid(row=8, column=1, ipady=5)

        self.ranking_label.grid(row=9, sticky=W, padx=5)
        self.ranking_cbb.grid(row=9, column=1)

        self.search_button.grid(row=10, column=0, columnspan=2, ipady=5, ipadx=5, pady=20)

        self.window.mainloop()



def main():
    window = Tk()
    window.title("GAvI Search Engine")
    UI = UserInterface(window)
    UI.display_search()



if __name__ == '__main__':
    main()
