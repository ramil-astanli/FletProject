import flet as ft
import httpx

class CRUDItem(ft.Column):
    def __init__(self, name, description, delete_callback):
        super().__init__()
        self.name = name 
        self.description = description
        self.delete_callback = delete_callback

        self.text_view = ft.ListTile(
            leading=ft.Icon(ft.Icons.AIRPLANEMODE_ACTIVE, color="blue"),
            title=ft.Text(self.name, weight="bold"),
            subtitle=ft.Text(self.description),
            trailing=ft.Row([
                ft.IconButton(ft.Icons.EDIT, icon_color="orange", on_click=self.edit_clicked),
                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=self.delete_clicked),
            ], tight=True)
        )

        self.name_edit = ft.TextField(value=self.name, label="Drone Adı", border_radius=10)
        self.desc_edit = ft.TextField(value=self.description, label="Təsvir", border_radius=10)
        
        self.edit_view = ft.Column([
            self.name_edit,
            self.desc_edit,
            ft.Row([
                ft.ElevatedButton(
                    "Yadda Saxla", 
                    icon=ft.Icons.CHECK,
                    on_click=self.save_clicked,
                    style=ft.ButtonStyle(color="white", bgcolor="green")
                ),
                ft.TextButton("Ləğv Et", on_click=self.cancel_clicked)
            ], alignment="end")
        ], visible=False, spacing=10)

        self.controls = [
            ft.Container(
                content=ft.Column([self.text_view, self.edit_view]),
                padding=10,
                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=10,
                margin=ft.margin.only(bottom=10)
            )
        ]

    def edit_clicked(self, e):
        self.text_view.visible = False
        self.edit_view.visible = True
        self.update()

    def cancel_clicked(self, e):
        self.edit_view.visible = False
        self.text_view.visible = True
        self.update()

    def delete_clicked(self, e):
        try:
            with httpx.Client() as client:
                response = client.post(
                    "http://127.0.0.1:8000/delete_drone", 
                    json={"name": self.name}
                )
            if response.status_code == 200:
                self.delete_callback(self) 
        except Exception as ex:
            print(f"Silmə xətası: {ex}")

    def save_clicked(self, e):
        old_name = self.name
        new_name = self.name_edit.value
        new_desc = self.desc_edit.value

        try:
            with httpx.Client() as client:
                response = client.post(
                    "http://127.0.0.1:8000/update_drone", 
                    json={
                        "old_name": old_name, 
                        "new_name": new_name, 
                        "description": new_desc
                    }
                )
            
            if response.status_code == 200:
                self.name = new_name
                self.description = new_desc
                self.text_view.title.value = self.name
                self.text_view.subtitle.value = self.description
                self.cancel_clicked(e) 
            else:
                print("Yeniləmə uğursuz oldu")
        except Exception as ex:
            print(f"Yeniləmə xətası: {ex}")