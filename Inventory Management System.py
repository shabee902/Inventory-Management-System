import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
import pandas as pd

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Inventory Management System")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Inventory data storage
        self.inventory = []

        # Styling
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Configuring grid resizing
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.rowconfigure(6, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Creating Menu
        self.create_menu()

        # Toolbar
        self.toolbar = ttk.Frame(self.main_frame, padding="5")
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        ttk.Button(self.toolbar, text="Import CSV", command=self.load_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Export", command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Update Item", command=self.update_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Delete Item", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Clear Fields", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)

        # Filters
        self.filter_frame = ttk.LabelFrame(self.main_frame, text="Filters", padding="10")
        self.filter_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.W)

        ttk.Label(self.filter_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.filter_category = ttk.Combobox(self.filter_frame, values=["All", "Electronics", "Accessories", "Furniture", "Audio", "Storage"])
        self.filter_category.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.filter_category.set("All")

        ttk.Label(self.filter_frame, text="Price Range:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.filter_price_min = ttk.Entry(self.filter_frame, width=10)
        self.filter_price_min.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.filter_frame, text="to").grid(row=0, column=4, padx=5, pady=5)
        self.filter_price_max = ttk.Entry(self.filter_frame, width=10)
        self.filter_price_max.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.filter_frame, text="Apply Filters", command=self.apply_filters).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(self.filter_frame, text="Clear Filters", command=self.clear_filters).grid(row=0, column=7, padx=5, pady=5)

        # Input fields
        ttk.Label(self.main_frame, text="Item Name:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.item_name = ttk.Entry(self.main_frame, font=("Arial", 12))
        self.item_name.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.category = ttk.Entry(self.main_frame, font=("Arial", 12))
        self.category.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Quantity:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.quantity = ttk.Entry(self.main_frame, font=("Arial", 12))
        self.quantity.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Price:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.price = ttk.Entry(self.main_frame, font=("Arial", 12))
        self.price.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # Treeview for inventory display
        self.tree = ttk.Treeview(self.main_frame, columns=("Item", "Category", "Quantity", "Price", "Total"), show="headings", height=15)
        self.tree.heading("Item", text="Item")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Total", text="Total")

        self.tree.column("Item", anchor=tk.W, width=200)
        self.tree.column("Category", anchor=tk.W, width=150)
        self.tree.column("Quantity", anchor=tk.CENTER, width=100)
        self.tree.column("Price", anchor=tk.CENTER, width=100)
        self.tree.column("Total", anchor=tk.CENTER, width=120)

        self.tree.grid(row=6, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.apply_dark_theme = False

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open CSV", command=self.load_csv)
        file_menu.add_command(label="Export", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Dark/Light Theme", command=self.toggle_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Maximize", command=lambda: self.root.state('zoomed'))
        menubar.add_cascade(label="View", menu=view_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def apply_filters(self):
        category_filter = self.filter_category.get()
        price_min = self.filter_price_min.get()
        price_max = self.filter_price_max.get()

        filtered_inventory = self.inventory

        if category_filter != "All":
            filtered_inventory = [item for item in filtered_inventory if item["category"] == category_filter]

        if price_min or price_max:
            try:
                price_min = float(price_min) if price_min else 0
                price_max = float(price_max) if price_max else float('inf')
                filtered_inventory = [item for item in filtered_inventory if price_min <= item["price"] <= price_max]
            except ValueError:
                messagebox.showerror("Error", "Price filter values must be numeric.")
                return

        self.display_filtered_inventory(filtered_inventory)

    def clear_filters(self):
        self.filter_category.set("All")
        self.filter_price_min.delete(0, tk.END)
        self.filter_price_max.delete(0, tk.END)
        self.update_display()

    def display_filtered_inventory(self, inventory):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, item in enumerate(inventory):
            self.tree.insert('', 'end', iid=idx, values=(item['name'], item['category'], item['quantity'], item['price'], item['total']))

    def add_item(self):
        name = self.item_name.get().strip()
        category = self.category.get().strip()
        try:
            qty = int(self.quantity.get())
            price = float(self.price.get())

            if not name or not category:
                raise ValueError("Item name and category cannot be empty")

            if qty < 0 or price < 0:
                raise ValueError("Quantity and Price cannot be negative")

            total = qty * price

            self.inventory.append({"name": name, "category": category, "quantity": qty, "price": price, "total": total})
            self.update_display()
            messagebox.showinfo("Success", f"Item '{name}' added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.clear_inputs()

    def update_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to update")
            return

        try:
            name = self.item_name.get().strip()
            category = self.category.get().strip()
            qty = int(self.quantity.get())
            price = float(self.price.get())

            if not name or not category:
                raise ValueError("Item name and category cannot be empty")

            if qty < 0 or price < 0:
                raise ValueError("Quantity and Price cannot be negative")

            total = qty * price

            item_index = self.tree.index(selected_item[0])
            self.inventory[item_index] = {"name": name, "category": category, "quantity": qty, "price": price, "total": total}

            self.update_display()
            messagebox.showinfo("Success", f"Item '{name}' updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return

        item_index = self.tree.index(selected_item[0])
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")
        if confirm:
            del self.inventory[item_index]
            self.update_display()
            messagebox.showinfo("Success", "Item deleted successfully!")

    def update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, item in enumerate(self.inventory):
            self.tree.insert('', 'end', iid=idx, values=(item['name'], item['category'], item['quantity'], item['price'], item['total']))

    def clear_inputs(self):
        self.item_name.delete(0, tk.END)
        self.category.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.price.delete(0, tk.END)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                self.inventory = [{"name": row['Item'], "category": row['Category'], "quantity": int(row['Quantity']), "price": float(row['Price']), "total": float(row['Total'])} for row in reader]
            self.update_display()
            messagebox.showinfo("Success", "Inventory loaded successfully!")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("Excel files", "*.xlsx")])
        if not file_path:
            return

        extension = file_path.split('.')[-1]

        try:
            if extension == 'csv':
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Item", "Category", "Quantity", "Price", "Total"])
                    writer.writeheader()
                    for item in self.inventory:
                        writer.writerow({"Item": item['name'], "Category": item['category'], "Quantity": item['quantity'], "Price": item['price'], "Total": item['total']})
                messagebox.showinfo("Success", "Inventory exported successfully as CSV!")

            elif extension == 'json':
                with open(file_path, mode='w') as file:
                    json.dump(self.inventory, file, indent=4)
                messagebox.showinfo("Success", "Inventory exported successfully as JSON!")

            elif extension == 'xlsx':
                df = pd.DataFrame(self.inventory)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", "Inventory exported successfully as Excel!")

            else:
                messagebox.showerror("Error", "Unsupported file format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

    def toggle_theme(self):
        if self.apply_dark_theme:
            self.enable_light_theme()
        else:
            self.enable_dark_theme()
        self.apply_dark_theme = not self.apply_dark_theme

    def enable_dark_theme(self):
        self.root.configure(bg="black")
        self.main_frame.configure(style="TFrame")
        self.tree.configure(style="TFrame")
        self.tree.tag_configure("dark", background="gray20", foreground="white")

    def enable_light_theme(self):
        self.root.configure(bg="white")
        self.main_frame.configure(style="TFrame")
        self.tree.configure(style="TFrame")

    def show_about(self):
        about_text = (
            "Advanced Inventory Management System v1.0\n"
            "Developed by Syed Shabee ul Hassan\n\n"
            "Features:\n"
            "- Import and Export inventory data in CSV, JSON, and Excel formats.\n"
            "- Interactive filtering and sorting capabilities.\n"
            "- Dark and Light theme toggle.\n"
            "- Fully responsive layout.\n"
            "- Data validation and error handling.\n"
        )
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
