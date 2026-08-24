from customtkinter import *
from models import Grocery_manager
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class GroceryApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Grocery Management System")
    self.root.geometry("1100x650")

    self.manager = Grocery_manager()
    self.manager.load_from_file()

    self.selected_product_name = None  

    self.create_main_frames()
    self.create_left_panel_widgets()
    self.create_right_panel_widgets()

    self.update_table()

  def create_main_frames(self):
    self.left_frame = CTkFrame(self.root, width=320)
    self.left_frame.pack(side="left", fill="y", padx=15, pady=15)
    self.left_frame.pack_propagate(False)

    self.right_frame = CTkFrame(self.root)
    self.right_frame.pack(
        side="right", fill="both", expand=True, padx=15, pady=15
    )

  def create_left_panel_widgets(self):
    title_label = CTkLabel(
        self.left_frame, text="Control Panel", font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)

    self.name_entry = CTkEntry(
        self.left_frame, placeholder_text="Product Name", width=280
    )
    self.name_entry.pack(pady=6)

    self.qty_entry = CTkEntry(
        self.left_frame, placeholder_text="Quantity", width=280
    )
    self.qty_entry.pack(pady=6)

    self.price_entry = CTkEntry(
        self.left_frame, placeholder_text="Price", width=280
    )
    self.price_entry.pack(pady=6)

    self.add_btn = CTkButton(self.left_frame, text="Add Item", fg_color="green", hover_color="#006400", width=280, command=self.add_product)
    self.add_btn.pack(pady=6)

    self.update_btn = CTkButton(self.left_frame,text="Update Selected",fg_color="blue",hover_color="#00008B",width=280,command=self.update_product)
    self.update_btn.pack(pady=6)

    self.del_btn = CTkButton(self.left_frame, text="Delete Selected", fg_color="red", hover_color="#8B0000", width=280, command=self.delete_product)
    self.del_btn.pack(pady=6)

    separator = CTkLabel(self.left_frame, text="-----------------------------")
    separator.pack(pady=2)

    self.search_entry = CTkEntry(self.left_frame, placeholder_text="Search by name...", width=280)
    self.search_entry.pack(pady=6)

    self.search_btn = CTkButton(self.left_frame, text="Search Item", fg_color="orange", text_color="black", hover_color="#FF8C00", width=280, command=self.search_product)
    self.search_btn.pack(pady=6)

    self.reset_btn = CTkButton(self.left_frame, text="Show All", fg_color="gray", hover_color="#696969", width=280, command=self.update_table)
    self.reset_btn.pack(pady=6)

  def create_right_panel_widgets(self):
    table_title = CTkLabel(self.right_frame, text="Product List", font=("Arial", 16, "bold"))
    table_title.pack(pady=10)

    table_frame = CTkFrame(self.right_frame)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Name", "Quantity", "Price")
    self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=22)

    self.tree.heading("Name", text="Product Name")
    self.tree.heading("Quantity", text="Quantity")
    self.tree.heading("Price", text="Price ($)")

    self.tree.column("Name", width=220, anchor="center")
    self.tree.column("Quantity", width=130, anchor="center")
    self.tree.column("Price", width=130, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame, orient="vertical", command=self.tree.yview
    )
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

  def update_table(self, items=None):
    for row in self.tree.get_children():
      self.tree.delete(row)

    if items is None:
      items = self.manager.items_list

    for item in items:
      self.tree.insert("", "end", values=(item.name, item.quantity, item.price))

  def add_product(self):
    name = self.name_entry.get().strip()
    qty = self.qty_entry.get().strip()
    price = self.price_entry.get().strip()

    if name and qty and price:
      try:
        self.manager.add_item(name, int(qty), float(price))
        self.manager.save_to_file()
        self.update_table()
        self.clear_entries()
      except ValueError:
        CTkMessagebox(title="INFO", message="Xəta: Miqdar və qiymət rəqəm olmalıdır!")

  def update_product(self):
    if not self.selected_product_name:
      print("Zəhmət olmasa cədvəldən yeniləmək üçün məhsul seçin!")
      return

    name = self.name_entry.get().strip()
    qty = self.qty_entry.get().strip()
    price = self.price_entry.get().strip()

    if name and qty and price:
      try:
        self.manager.update_item(
            self.selected_product_name, name, int(qty), float(price)
        )
        self.manager.save_to_file()
        self.update_table()
        self.clear_entries()
      except ValueError:
        CTkMessagebox(title="INFO", message="Xəta: Miqdar və qiymət rəqəm olmalıdır!")

  def delete_product(self):
    selected_items = self.tree.selection()

    if not selected_items:
        CTkMessagebox(title="INFO", message="Zəhmət olmasa cədvəldən məhsul seçin!")
        return

    for item_id in selected_items:
        values = self.tree.item(item_id, "values")

        if values:
            name = str(values[0])
            for item in self.manager.items_list:
                if str(item.name).lower() == name.lower():
                    self.manager.items_list.remove(item)
                    break

    self.manager.save_to_file()
    self.update_table()
    self.clear_entries()

  def search_product(self):
    keyword = self.search_entry.get().strip()
    if keyword:
      results = self.manager.search_item(keyword)
      self.update_table(results)
    else:
      self.update_table()

  def on_row_select(self, event):
    selected_item = self.tree.selection()
    if selected_item:
      item_data = self.tree.item(selected_item)
      values = item_data["values"]
      if values:
        self.selected_product_name = values[0]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, values[0])
        self.qty_entry.delete(0, "end")
        self.qty_entry.insert(0, values[1])
        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, values[2])

  def clear_entries(self):
    self.name_entry.delete(0, "end")
    self.qty_entry.delete(0, "end")
    self.price_entry.delete(0, "end")
    self.selected_product_name = None

class A:
  pass