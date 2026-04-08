import flet as ft
from database import init_db
from admin import AdminDashboard
from login_page import LoginPage

from signup_page import SignupPage


def main(page: ft.Page):
    init_db()
    page.title = "Astan Drone App"
    page.window.width = 390
    page.window.height = 800
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.padding = 0
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.BEDTIME
            theme_button.icon_color = "black"
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.SUNNY
            theme_button.icon_color = "yellow"
        page.update()
    theme_button = ft.IconButton(
        icon=ft.Icons.BEDTIME,
        icon_color="black",
        on_click=change_theme
    )
    def route_change(e):
        page.views.clear()
        common_appbar = ft.AppBar(
            title=ft.Text("Astan Drone", weight="bold"),
            bgcolor="surfacevariant", 
            actions=[theme_button],
        )
        if page.route == "/" or page.route == "":
            view = LoginPage(page)
            view.appbar = common_appbar
            page.views.append(view)

        elif page.route == "/signup":
            view = SignupPage(page)
            view.appbar = common_appbar 
            page.views.append(view)
        elif page.route == "/admin":
            page.views.append(AdminDashboard(page))
    
        page.update()
    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
    page.on_route_change = route_change

    page.on_view_pop = view_pop

   


    page.route = "/"

    route_change(None)


if __name__ == "__main__":

    ft.run(main) 