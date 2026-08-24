class Product:
  def __init__(self, name, quantity, price):
    self.name = name
    self.price = price
    self.quantity = quantity


class Grocery_manager:
  def __init__(self):
    self.items_list = []

  def add_item(self, name, quantity, price):
    for item in self.items_list:
      if str(item.name).strip().lower() == str(name).strip().lower():
        item.quantity += quantity
        item.price = price
        return

    new_product = Product(name, quantity, price)
    self.items_list.append(new_product)

  def delete_item(self, name):
    target_name = str(name).strip().lower()
    new_list = []
    
    for item in self.items_list:
      if str(item.name).strip().lower() != target_name:
        new_list.append(item)

    self.items_list = new_list

  def update_item(self, old_name, new_name, new_quantity, new_price):
    target_old = str(old_name).strip().lower()

    for item in self.items_list:
      if str(item.name).strip().lower() == target_old:
        item.name = new_name
        item.quantity = new_quantity
        item.price = new_price
        break

  def get_all_items(self):
    for i in self.items_list:
      print(f"Name: {i.name}\nQuantity: {i.quantity}\nPrice: {i.price}\n")

  def save_to_file(self):
    with open("Products.txt", "w", encoding="utf-8") as f:
      for p in self.items_list:
        f.write(f"{p.name},{p.quantity},{p.price}\n")

  def search_item(self, keyword):
    result = []
    target = str(keyword).strip().lower()
    for item in self.items_list:
      if str(item.name).lower().startswith(target):
        result.append(item)
    return result

  def load_from_file(self):
    self.items_list = []
    try:
      with open("Products.txt", "r", encoding="utf-8") as f:
        for line in f:
          line = line.strip()
          if line:
            name, qty, price = line.split(",")
            self.items_list.append(Product(name, int(qty), float(price)))
    except FileNotFoundError:
      pass