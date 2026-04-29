import flet as ft
from CRUDItem import CRUDItem
import httpx 
import time # Gecikmə üçün mütləqdir

class AdminDashboard(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/admin", 
            padding=20,
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.ADD_BOX, label="Əlavə Et"),
                    ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS, label="Statistika"),
                    ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT, label="Dronlar"),
                ],
                on_change=self.handle_nav_change,
                selected_index=0
            )
        )
        self.main_page = page
        
        # UI Elementləri
        self.items_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        self.new_name = ft.TextField(label="Drone Adı", expand=True)
        self.new_desc = ft.TextField(label="Təsvir", expand=True)
        
        # Header
        self.header = ft.Row([
            ft.Text("Drone İdarəetmə", size=28, weight="bold"),
            ft.IconButton(
                icon=ft.Icons.LOGOUT, 
                on_click=lambda _: self.logout()
            )
        ], alignment="spaceBetween")

        self.show_add_section()

    def logout(self):
        self.page.route = "/"
        self.page.update()

    def handle_nav_change(self, e):
        index = e.control.selected_index
        if index == 0:
            self.show_add_section()
        elif index == 1:
            self.show_stats_section()
        elif index == 2:
            self.show_list_section()
        self.update()

    def show_add_section(self):
        self.controls = [
            self.header,
            ft.Container(height=20),
            ft.Text("Yeni Drone Əlavə Edin", size=20, weight="w500", color="blue"),
            ft.Column([
                self.new_name,
                self.new_desc,
                ft.FilledButton( # ElevatedButton xətası verməməsi üçün FilledButton
                    content=ft.Row(
                        [ft.Icon(ft.Icons.SAVE), ft.Text("Bazaya Əlavə Et")],
                        alignment="center",
                    ),
                    on_click=self.add_item,
                    width=400,
                )
            ], spacing=20)
        ]

    def show_stats_section(self):
        total_drones = 0
        try:
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/drones")
                if response.status_code == 200:
                    total_drones = len(response.json())
        except Exception as ex:
            print(f"Statistika xətası: {ex}")

        # Statistika UI-ı burada yaradılır
        self.controls = [
            self.header,
            ft.Container(height=40),
            # ft.Center yerinə ft.Container istifadə edirik:
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ANALYTICS, size=80, color="blue"),
                    ft.Text("Sistemdəki Dron Sayı", size=20, weight="w500"),
                    ft.Text(str(total_drones), size=50, weight="bold", color="blue"),
                    ft.Container(
                        content=ft.Text("Məlumatlar real vaxt rejimində API-dən alınır", size=12, italic=True),
                        margin=ft.margin.only(top=20)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), # Sütunu mərkəzləyirik
                alignment=ft.Alignment.CENTER, # Konteyneri ekranın mərkəzinə gətiririk
                expand=True
            )
        ]

    def show_list_section(self):
        self.load_data()
        self.controls = [
            self.header,
            ft.Container(height=10),
            ft.Text("Qeydiyyatdakı Dronlar", size=20, weight="w500", color="green"),
            ft.Divider(height=20, thickness=1),
            self.items_list 
        ]

    def load_data(self):
            self.items_list.controls.clear()
            try:
                with httpx.Client() as client:
                    response = client.get("http://127.0.0.1:8000/drones")
                
                if response.status_code == 200:
                    drones = response.json()
                    for d in drones:
                        # ARQUMENTLƏRİ ADLARI İLƏ GÖNDƏRİRİK (BU ÇOX VACİBDİR)
                        item = CRUDItem(
                            name=d[0], 
                            description=d[1], 
                            delete_callback=self.delete_item
                        )
                        self.items_list.controls.append(item)
            except Exception as ex:
                print(f"API xətası: {ex}")
            self.update() # Siyahını vizual yeniləmək üçün

    def add_item(self, e):
        if not self.new_name.value.strip() or not self.new_desc.value.strip():
            self.new_name.error_text = "Boş buraxmayın!"
            self.update()
            return
            
        drone_name = self.new_name.value
        drone_desc = self.new_desc.value

        # --- FastAPI İnteqrasiyası ---
        try:
            with httpx.Client() as client:
                # Qeyd: api_server.py-da bu endpoint-i yaratmalısan
                response = client.post(
                    "http://127.0.0.1:8000/add_drone", 
                    json={"name": drone_name, "description": drone_desc}
                )
            
            if response.status_code == 200:
                # Uğurlu olduqda SnackBar göstər
                snack = ft.SnackBar(content=ft.Text(f"'{drone_name}' uğurla əlavə olundu!"))
                self.page.overlay.append(snack)
                snack.open = True
                
                # Sahələri təmizlə və siyahıya keç
                self.new_name.value = ""
                self.new_desc.value = ""
                self.navigation_bar.selected_index = 2
                self.show_list_section()
            else:
                print("Xəta: API dronu əlavə edə bilmədi.")
                
        except Exception as ex:
            print(f"Bağlantı xətası: {ex}")
        
        self.page.update()
        self.update()


    def delete_item(self, item):
        # 1. Siyahıdan vizual olaraq çıxarırıq
        self.items_list.controls.remove(item)
        
        # 2. İstifadəçiyə silinmə barədə kiçik bildiriş (SnackBar) çıxarırıq
        # Bu, istifadəçinin əməliyyatın uğurlu olduğunu anlaması üçün yaxşıdır
        snack = ft.SnackBar(
            content=ft.Text(f"'{item.name}' bazadan silindi."),
            bgcolor="red"
        )
        self.page.overlay.append(snack)
        snack.open = True
        
        # 3. Ekranı yeniləyirik
        self.update()