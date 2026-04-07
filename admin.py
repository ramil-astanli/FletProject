import flet as ft

def main(page: ft.Page):
    page.title = "Astan Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW
    
    page.window.width = 390
    page.window.height = 800
    page.window.resizable = False 
    
    page.window.center() 
    
    page.update()

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.BEDTIME
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.SUNNY
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.SUNNY, 
        on_click=change_theme
    )

    def home_view():
        def stat_card(title, value, percentage, icon_color):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(width=40, height=40, bgcolor=icon_color, border_radius=10),
                        ft.Row([ft.Icon(ft.Icons.TRENDING_UP, size=14), ft.Text(f"+%{percentage}", size=12, weight="bold")], spacing=2)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(title, size=11, color=ft.Colors.OUTLINE, weight="bold"),
                    ft.Text(value, size=22, weight="bold"),
                ], spacing=10),
                padding=15, 
                bgcolor=ft.Colors.SURFACE_CONTAINER, 
                border_radius=20, 
                expand=True
            )
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Merhaba, Admin", size=26, weight="bold"),
                    ft.Text("İşletmenizin bugünkü özeti burada.", color=ft.Colors.OUTLINE),
                ]), padding=ft.padding.only(top=40, left=20, right=20)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        stat_card("MÜŞTERİLER", "1,284", "12", ft.Colors.BLUE_400),
                        stat_card("SİPARİŞLER", "342", "8", ft.Colors.GREEN_400),
                    ], spacing=15),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, size=24),
                            ft.Text("ÜRÜN ENVANTERİ", size=11, color=ft.Colors.OUTLINE, weight="bold"),
                            ft.Text("4,510", size=22, weight="bold"),
                        ], spacing=8),
                        padding=20, bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=20, width=float("inf")
                    ),
                    ft.Text("Hızlı İşlemler", size=18, weight="bold"),
                    ft.Row([
                        ft.Column([ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_color=ft.Colors.BLUE), ft.Text("Yeni Müşteri", size=10)], horizontal_alignment="center"),
                        ft.Column([ft.IconButton(ft.Icons.NORTH_EAST, icon_color=ft.Colors.GREEN), ft.Text("Yeni Sipariş", size=10)], horizontal_alignment="center"),
                        ft.Column([ft.IconButton(ft.Icons.ADD_BOX_OUTLINED, icon_color=ft.Colors.ORANGE), ft.Text("Ürün Ekle", size=10)], horizontal_alignment="center"),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Son Aktiviteler", size=18, weight="bold"),
                    ft.Container(
                        content=ft.Column([
                            ft.ListTile(leading=ft.CircleAvatar(content=ft.Text("AY")), title=ft.Text("Ahmet Yılmaz"), subtitle=ft.Text("Yeni sipariş: #ORD-5542"), trailing=ft.Text("10 dk")),
                            ft.Divider(height=1),
                            ft.ListTile(leading=ft.CircleAvatar(content=ft.Text("EK"), bgcolor="orange"), title=ft.Text("Elif Kaya"), subtitle=ft.Text("Müşteri kaydı tamamlandı"), trailing=ft.Text("45 dk")),
                        ]), bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=20
                    ),
                ], spacing=20), padding=20
            )
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    def customers_view():
        def client_item(name, email, phone, addr_count):
            return ft.Container(
                content=ft.ListTile(
                    leading=ft.CircleAvatar(content=ft.Text(name[0])),
                    title=ft.Text(name, weight="bold", size=14),
                    subtitle=ft.Text(f"{email}\n{phone}", size=11, color=ft.Colors.OUTLINE),
                    trailing=ft.Container(content=ft.Text(f"📍 {addr_count} Adres", size=10, weight="bold"), padding=5, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=10)
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=15, margin=ft.margin.only(bottom=10)
            )

        return ft.Column([
            ft.Container(content=ft.Row([ft.Text("Müşteriler", size=24, weight="bold"), ft.IconButton(ft.Icons.FILTER_ALT_OUTLINED)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.only(top=40, left=20, right=20)),
            ft.Container(content=ft.TextField(hint_text="Müşteri ara...", prefix_icon=ft.Icons.SEARCH, border_radius=15, bgcolor=ft.Colors.SURFACE_CONTAINER), padding=20),
            ft.Container(content=ft.Column([
                client_item("Ahmet Yılmaz", "ahmet@mail.com", "+90 532", "2"),
                client_item("Zeynep Demir", "zeynep@mail.com", "+90 544", "1"),
                client_item("Can Tekin", "info@lojistik.com", "+90 212", "4"),
            ]), padding=ft.padding.only(left=20, right=20, bottom=100))
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # --- 3. SİPARİŞLER GÖRÜNÜMÜ ---
    def orders_view():
        def order_item(order_id, name, date, amount, status, status_color):
            return ft.Container(
                content=ft.Column([
                    ft.Row([ft.Text(order_id, size=10, weight="bold"), ft.Text(date, size=11, color=ft.Colors.OUTLINE)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.ListTile(title=ft.Text(name, weight="bold"), subtitle=ft.Text("Hızlı Teslimat"), trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT)),
                    ft.Row([ft.Text(amount, weight="bold", size=16, color=ft.Colors.BLUE), ft.Chip(label=ft.Text(status), bgcolor=status_color)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]), padding=15, bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=15, margin=ft.margin.only(bottom=10)
            )

        return ft.Column([
            ft.Container(content=ft.Text("Siparişler", size=24, weight="bold"), padding=ft.padding.only(top=40, left=20, right=20)),
            ft.Container(content=ft.Column([
                order_item("AST-001", "Ahmet Yılmaz", "12 Haz", "1.250 TL", "Beklemede", ft.Colors.ORANGE_300),
                order_item("AST-002", "Ayşe Demir", "11 Haz", "3.400 TL", "Tamamlandı", ft.Colors.GREEN_300),
            ]), padding=20)
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # --- 4. ÜRÜNLER GÖRÜNÜMÜ ---
    def products_view():
        return ft.Column([
            ft.Container(content=ft.Text("Ürün Kataloğu", size=24, weight="bold"), padding=ft.padding.only(top=40, left=20, right=20)),
            ft.Container(content=ft.Text("Stokta olan ürünler listesi burada görünecek."), padding=20)
        ], expand=True)

    main_container = ft.Container(content=home_view(), expand=True)

    def navigate(e):
        index = e.control.selected_index
        views = [home_view(), customers_view(), orders_view(), products_view()]
        main_container.content = views[index]
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=navigate,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Ana Sayfa"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINED, selected_icon=ft.Icons.PERSON, label="Müşteriler"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART_OUTLINED, selected_icon=ft.Icons.SHOPPING_CART, label="Siparişler"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2_OUTLINED, selected_icon=ft.Icons.INVENTORY, label="Ürünler"),
        ],
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Astan Dashboard", weight="bold"),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[theme_button],
    )

    page.add(main_container)

if __name__ == "__main__":
    ft.app(target=main)