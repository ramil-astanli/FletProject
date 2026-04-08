import flet as ft
from CRUDItem import CRUDItem
import database 

class AdminDashboard(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/admin", padding=20)
        self.main_page = page
        self.items_list = ft.Column()

        self.new_name = ft.TextField(label="Drone Adı", expand=True)
        self.new_desc = ft.TextField(label="Təsvir (Model, Spesifikasiya)", expand=True)

        self.controls = [
            ft.Row([
                ft.Text("Drone İdarəetmə Paneli", size=28, weight="bold"),
                ft.IconButton(ft.Icons.LOGOUT, on_click=lambda _: self.main_page.go("/"))
            ], alignment="spaceBetween"),
            
            ft.Row([
                self.new_name,
                self.new_desc,
                ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_item)
            ]),
            ft.Divider(),
            self.items_list
        ]
        
        self.load_data()

    def load_data(self):
        drones = database.get_drones() 
        for d in drones:
            self.items_list.controls.append(
                CRUDItem(d[0], d[1], self.delete_item)
            )

    def add_item(self, e):
        self.new_name.error_text = None
        self.new_desc.error_text = None
    
        is_valid = True
        if not self.new_name.value.strip():
            self.new_name.error_text = "Dron adını boş qoymaq olmaz!"
            is_valid = False
        
        if not self.new_desc.value.strip():
            self.new_desc.error_text = "Təsvir hissəsini doldurun!"
        is_valid = False

        if not is_valid:
            self.update() 
            return

     
        database.add_drone(self.new_name.value, self.new_desc.value)
    
        item = CRUDItem(self.new_name.value, self.new_desc.value, self.delete_item)
        self.items_list.controls.append(item)
    
        self.new_name.value = ""
        self.new_desc.value = ""
    
        self.update()

    def add_item(self, e):
        self.new_name.error_text = None
        self.new_desc.error_text = None
    
        error_found = False
    
        if not self.new_name.value.strip():
            self.new_name.error_text = "Zəhmət olmazsa name-i doldurun"
            error_found = True
        
        if not self.new_desc.value.strip():
            self.new_desc.error_text = "Zəhmət olmazsa description-u doldurun"
            error_found = True

        if error_found:
            self.new_name.update()
            self.new_desc.update()
            return

        database.add_drone(self.new_name.value, self.new_desc.value)
    
        new_item = CRUDItem(self.new_name.value, self.new_desc.value, self.delete_item)
        self.items_list.controls.append(new_item)
    
        self.new_name.value = ""
        self.new_desc.value = ""
    
        self.update()
    def delete_item(self, item):
        self.items_list.controls.remove(item)
        self.main_page.update()