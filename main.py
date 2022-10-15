#libs for GUI
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pickle
#libs for smart search
import pandas as pd
from razdel import tokenize, sentenize
from gensim import corpora, models, similarities
from gensim.utils import tokenize

full = pd.read_csv('full_table.csv', low_memory=False)
df_compare = pd.DataFrame(columns=['name'], index=range(full.shape[0]))
full.drop_duplicates(inplace=True)
full.reset_index(inplace=True)
full.fillna('', inplace=True)

full['name_char_okpd'] = full['product_name'] + ' ' + full['product_characteristics'] + ' ' + full['okpd2_name']
full['name_char_okpd'] = full['name_char_okpd'].apply(lambda x: list(x.split()))


with open('index.pickle', 'rb') as f:
    index = pickle.load(f)

with open('dictionary.pickle', 'rb') as g:
    dictionary = pickle.load(g)

with open('tfidf.pickle', 'rb') as h:
    tfidf = pickle.load(h)


class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lolipop Zakupki")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.geometry("1400x700")
        self.search_page = SearchPage(parent=self.main_frame)


class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)

        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")

        self.stored_dataframe = pd.DataFrame()

    def set_datatable(self, dataframe):

        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):

        self.delete(*self.get_children())
        columns = list(dataframe.columns)

        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col)

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)

        return None

    def find_rec(self, queary):
        for text in queary:
            kw_vector = dictionary.doc2bow(tokenize(text))
            df_compare['name'] = index[tfidf[kw_vector]]
        spisok = df_compare['name'].loc[df_compare['name'] > 0.25].sort_values(ascending = False).index
        return spisok

    def find_value(self, keys):

        spisok_rec = self.find_rec(keys)
        new_df = self.stored_dataframe

        df_rec = pd.DataFrame(columns=full.columns, index=[str(i) + ' recommendation:' for i in range(len(spisok_rec))])

        for j in range(len(spisok_rec)):
            df_rec.loc[str(j) + ' recommendation:'] = full.iloc[spisok_rec[j]]

        df_rec = df_rec[['product_name', 'price', 'product_characteristics', 'okpd2_code', 'inn', 'country_code']]

        self._draw_table(df_rec)


    def reset_table(self):

        self._draw_table(self.stored_dataframe)


class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_names_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background='#2799d6', font='Courier 16')
        self.file_names_listbox.place(relheight=0.05, relwidth=0.05)
        self.file_names_listbox.drop_target_register(DND_FILES)
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        self.file_names_listbox.bind("<Double-1>", self._display_file)

        self.search_entrybox = tk.Entry(parent, background='#2799d6', font='Courier 16')
        self.search_entrybox.place(relx=0.05, relwidth=0.95)
        self.search_entrybox.bind("<Return>", self.search_table)

        # Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(rely=0.05, relx=0.05, relwidth=0.95, relheight=0.95)

        self.path_map = {}
        self.drop_inside_list_box_1()

    def drop_inside_list_box(self, event):

        file_paths = self._parse_drop_files(event.data)
        current_listbox_items = set(self.file_names_listbox.get(0, "end"))
        for file_path in file_paths:

            if file_path.endswith(".csv"):
                path_object = Path(file_path)
                file_name = path_object.name[:-4]
                if file_name not in current_listbox_items:
                    self.file_names_listbox.insert("end", file_name)
                    self.path_map[file_name] = file_path

    def drop_inside_list_box_1(self):

        path_object = Path("./full_table.csv")
        file_name = "Start"
        self.file_names_listbox.insert("end", file_name)
        self.path_map[file_name] = path_object

    def _display_file(self, event):

        file_name = self.file_names_listbox.get(self.file_names_listbox.curselection())
        path = self.path_map[file_name]
        df = pd.read_csv(path, encoding='utf-8')
        self.data_table.set_datatable(dataframe=df)

    def _parse_drop_files(self, filename):#chtenie imeni

        size = len(filename)
        res = []  # list of file paths
        name = ""
        idx = 0

        while idx < size:

            if filename[idx] == "{":
                j = idx + 1
                while filename[j] != "}":

                    name += filename[j]
                    j += 1
                res.append(name)
                name = ""
                idx = j

            elif filename[idx] == " " and name != "":
                res.append(name)
                name = ""

            elif filename[idx] != " ":
                name += filename[idx]

            idx += 1

        if name != "":
            res.append(name)

        return res

    def search_table(self, event): #razbienie na iacheiki.

        entr = self.search_entrybox.get()
        entry = list([entr])
        self.data_table.find_value(entry)


if __name__ == "__main__":

    root = Application()
    root.mainloop()