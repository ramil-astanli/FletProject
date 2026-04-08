import flet as ft
import database  

class CRUDItem(ft.Column):
    def __init__(self, name, description, delete_callback):
        super().__init__()
        self.name = name 
        self.description = description
        self.delete_callback = delete_callback

        self.text_view = ft.ListTile(
            leading=ft.Icon(ft.Icons.AIRPLANEMODE_ACTIVE),
            title=ft.Text(self.name),
            subtitle=ft.Text(self.description),
            trailing=ft.Row([
                ft.IconButton(ft.Icons.EDIT, on_click=self.edit_clicked),
                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=self.delete_clicked),
            ], tight=True)
        )

        self.name_edit = ft.TextField(value=self.name, label="Drone Adı")
        self.desc_edit = ft.TextField(value=self.description, label="Təsvir")
        
        self.edit_view = ft.Column([
            self.name_edit,
            self.desc_edit,
            ft.Row([
                ft.ElevatedButton("Yadda Saxla", on_click=self.save_clicked),
                ft.TextButton("Ləğv Et", on_click=self.cancel_clicked)
            ])
        ], visible=False)

        self.controls = [self.text_view, self.edit_view]

    def edit_clicked(self, e):
        self.text_view.visible = False
        self.edit_view.visible = True
        self.update()

    def delete_clicked(self, e):
        database.delete_drone(self.name)
        self.delete_callback(self)

    def save_clicked(self, e):
        old_name = self.name
        new_name = self.name_edit.value
        new_desc = self.desc_edit.value

        database.update_drone(old_name, new_name, new_desc)

        self.name = new_name
        self.description = new_desc
        self.text_view.title.value = self.name
        self.text_view.subtitle.value = self.description
        
        self.cancel_clicked(e)

    def cancel_clicked(self, e):
        self.edit_view.visible = False
        self.text_view.visible = True
        self.update()