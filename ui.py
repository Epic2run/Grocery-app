from customtkinter import *
from models import Grocery_manager
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class GroceryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Grocery Management System")
        self.window.geometry("1100x650")
        self.window.config(bg="#D5E4C3")

        self.manager = Grocery_manager()
        self.manager.load_from_file()
        self.selected_product_name = None

        self.create_main_frames()
        self.create_left_panel_widgets()
        self.create_right_panel_widgets()

        self.update_table()

    def create_main_frames(self):
        self.left_frame = CTkFrame(self.window,width=320,fg_color="#4A5D4E")
        self.left_frame.pack(side="left",fill="y",padx=15,pady=15)
        self.left_frame.pack_propagate(False)

        self.right_frame = CTkFrame(self.window, fg_color="#4A5D4E")
        self.right_frame.pack(side="right",fill="both",expand=True,padx=15,pady=15)

    def create_left_panel_widgets(self):
        title_label = CTkLabel(self.left_frame,text="Control Panel",font=("Arial",20,"bold"))
        title_label.pack(pady=15)

        self.name_entry = CTkEntry(self.left_frame,placeholder_text="Product Name",width=280)
        self.name_entry.pack(pady=6)

        self.qty_entry = CTkEntry(self.left_frame,placeholder_text="Quantity",width=280)
        self.qty_entry.pack(pady=6)

        self.price_entry = CTkEntry(self.left_frame,placeholder_text="Price",width=280)
        self.price_entry.pack(pady=6)

        self.add_btn = CTkButton(self.left_frame,text="Add Item",fg_color="#C07A54",hover_color="dark green",width=280,command=self.add_product)
        self.add_btn.pack(pady=6)

        self.update_btn = CTkButton(self.left_frame,text="Update Selected",fg_color="#C07A54",hover_color="dark green",width=280,command=self.update_product)
        self.update_btn.pack(pady=6)

        self.del_btn = CTkButton(self.left_frame,text="Delete Selected",fg_color="#C07A54",hover_color="dark green",width=280,command=self.delete_product)
        self.del_btn.pack(pady=6)

        self.show_btn = CTkButton(self.left_frame,text="Show Items",fg_color="#C07A54",hover_color="dark green",width=280,command=self.show_items)
        self.show_btn.pack(pady=6)

        separator = CTkLabel(self.left_frame,text="--------------------------------------------------------------------")
        separator.pack(pady=5)

        self.search_entry = CTkEntry(self.left_frame,placeholder_text="Search by name...",width=280)
        self.search_entry.pack(pady=6)

        self.search_btn = CTkButton(self.left_frame,text="Search Item",fg_color="#C07A54",hover_color="dark green",width=280,command=self.search_product)
        self.search_btn.pack(pady=6)

        self.save_btn = CTkButton(self.left_frame,text="Save",fg_color="#C07A54",hover_color="dark green",width=280,command=self.save_products)
        self.save_btn.pack(pady=6)

        self.load_btn = CTkButton(self.left_frame,text="Load",fg_color="#C07A54",hover_color="dark green",width=280,command=self.load_products)
        self.load_btn.pack(pady=6)

        self.reset_btn = CTkButton(self.left_frame,text="Clear / Show All",fg_color="#C07A54",hover_color="dark green",width=280,command=self.reset)
        self.reset_btn.pack(pady=6)

    def create_right_panel_widgets(self):
        table_title = CTkLabel(self.right_frame,text="Product List",font=("Arial",20,"bold"))
        table_title.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview",font=("Arial",16))
        style.configure("Treeview.Heading",font=("Arial",16,"bold"))

        table_frame = CTkFrame(self.right_frame)
        table_frame.pack(fill="both",expand=True,padx=10,pady=10)

        columns = ("Name","Quantity","Price")

        self.tree = ttk.Treeview(table_frame,columns=columns,show="headings",height=40)

        self.tree.heading("Name",text="Product Name")
        self.tree.heading("Quantity",text="Quantity")
        self.tree.heading("Price",text="Price ($)")

        self.tree.column("Name",width=220,anchor="center")
        self.tree.column("Quantity",width=130,anchor="center")
        self.tree.column("Price",width=130,anchor="center")

        scrollbar = ttk.Scrollbar(table_frame,orient="vertical",command=self.tree.yview)

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        self.tree.bind("<<TreeviewSelect>>",self.on_row_select)

    def update_table(self,items=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if items is None:
            items = self.manager.items_list

        for item in items:
            self.tree.insert("", "end", values=(item.name,item.quantity,item.price))

    def add_product(self):
        name = self.name_entry.get().strip()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not qty or not price:
            CTkMessagebox(title="INFO",message="Please, fill all fields!")
            return

        try:
            quantity = int(qty)
            price_value = float(price)

            if quantity < 0 or price_value < 0:
                CTkMessagebox(title="INFO",message="Quantity and Price cannot be negative!")
                return

            self.manager.add_item(name,quantity,price_value)
            self.manager.save_to_file()
            self.update_table()
            self.clear_entries()

        except ValueError:
            CTkMessagebox(title="INFO",message="Quantity must be an integer and Price must be a number!")

    def update_product(self):
        if not self.selected_product_name:
            CTkMessagebox(title="INFO",message="Please, choose an item from store")
            return

        name = self.name_entry.get().strip()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not qty or not price:
            CTkMessagebox(title="INFO",message="Please, fill all fields!")
            return

        try:
            quantity = int(qty)
            price_value = float(price)

            if quantity < 0 or price_value < 0:
                CTkMessagebox(title="INFO",message="Quantity and Price cannot be negative!")
                return
            
            self.manager.update_item(self.selected_product_name,name,quantity,price_value)
            self.manager.save_to_file()
            self.update_table()
            self.clear_entries()
        except ValueError:
            CTkMessagebox(title="INFO",message="Quantity must be an integer and Price must be a number!")

    def delete_product(self):
        selected_items = self.tree.selection()
        if not selected_items:
            CTkMessagebox(title="INFO",message="Please, choose an item from store")
            return

        for item_id in selected_items:
            values = self.tree.item(item_id,"values")
            if values:
                name = str(values[0])
                self.manager.delete_item(name)

        self.manager.save_to_file()
        self.update_table()
        self.clear_entries()

    def show_items(self):
        self.update_table()

    def search_product(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.update_table()
            return
        
        results = self.manager.search_item(keyword)
        self.update_table(results)

    def save_products(self):
        self.manager.save_to_file()
        CTkMessagebox(title="Success",message="Products saved successfully!")

    def load_products(self):
        self.manager.load_from_file()
        self.update_table()
        self.clear_entries()
        CTkMessagebox(title="Success",message="Products loaded successfully!")

    def on_row_select(self,event):
        selected_item = self.tree.selection()
        if selected_item:
            item_data = self.tree.item(selected_item[0])
            values = item_data["values"]
            if values:
                self.selected_product_name = values[0]

                self.name_entry.delete(0,"end")
                self.name_entry.insert(0,values[0])

                self.qty_entry.delete(0,"end")
                self.qty_entry.insert(0,values[1])

                self.price_entry.delete(0,"end")
                self.price_entry.insert(0,values[2])

    def clear_entries(self):
        self.name_entry.delete(0,"end")
        self.qty_entry.delete(0,"end")
        self.price_entry.delete(0,"end")
        self.selected_product_name = None

    def reset(self):
        self.clear_entries()
        self.search_entry.delete(0,"end")
        self.update_table()