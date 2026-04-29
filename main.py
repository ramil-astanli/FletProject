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

    def route_change(route):
        # Səhifələri təmizləyirik
        page.views.clear()
        
        common_appbar = ft.AppBar(
            title=ft.Text("Astan Drone", weight="bold"),
            bgcolor="surfacevariant",  # Heç bir ft.colors yazmağa ehtiyac yoxdur
            actions=[theme_button],
        )

        # Route yoxlaması
        if page.route == "/" or page.route == "":
            login_view = LoginPage(page)
            login_view.appbar = common_appbar
            page.views.append(login_view)

        elif page.route == "/signup":
            signup_view = SignupPage(page)
            signup_view.appbar = common_appbar 
            page.views.append(signup_view)

        elif page.route == "/admin":
            admin_view = AdminDashboard(page)
            # Admin üçün də appbar istəyirsənsə bura əlavə edə bilərsən
            page.views.append(admin_view)
    
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.route = top_view.route # page.go yerinə bunu istifadə et
            page.update()
    # Event handler-ləri təyin edirik
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # İlk səhifəni təyin edirik
    page.route = "/"
    # mütləq route_change-i birbaşa çağırırıq ki, ilk açılışda ağ ekran olmasın
    route_change(page.route)

if __name__ == "__main__":
    # ft.app yerinə ft.run istifadə edirik (0.80.0+ üçün)
    ft.run(main)