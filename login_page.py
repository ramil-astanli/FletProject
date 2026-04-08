import flet as ft
from database import check_user  
class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=ft.Colors.SURFACE, 
        )

        self.email_field = ft.TextField(
            hint_text="ornek@mail.com",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY_500)
        )
        
        self.password_field = ft.TextField(
            hint_text="********",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY_500)
        )

        def handle_login(e):
            email = self.email_field.value
            password = self.password_field.value

            if not email or not password:
                self.show_snack("Lütfen tüm alanları doldurun!")
                return

            if check_user(email, password):
                if email == "admin@mail.com" and password == "admin123":
                    self.show_snack("Admin girişi başarılı!")
                    self.page.go("/admin")  # Admin panelinə gedir
                else:
                    self.show_snack("Giriş başarılı!")
                    self.page.go("/dashboard") # Normal istifadəçi panelinə gedir
            else:
                self.show_snack("E-posta veya şifre hatalı!")

        def show_msg(e):
            self.show_snack("Bu özellik yakında aktif edilecek!")

        self.controls = [
            ft.Container(
                width=350,
                padding=20,
                content=ft.Column([
                    ft.Column([
                        ft.Text("Tekrar Hoş Geldiniz", size=28, weight="bold"),
                        ft.Text("Hesabınıza erişmek için bilgilerinizi girin.", 
                                size=14, color=ft.Colors.GREY_600),
                    ], spacing=5),

                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                    ft.Column([
                        ft.Text("E-posta Adresi", weight="bold", size=14),
                        self.email_field,
                        ft.Row([
                            ft.Text("Şifre", weight="bold", size=14),
                            ft.TextButton("Şifremi Unuttum?", on_click=show_msg),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.password_field,
                    ], spacing=10),

                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

                    ft.Button(
                        "Giriş Yap",
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        width=350,
                        height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=handle_login 
                    ),

                    ft.Row([
                        ft.Divider(expand=True),
                        ft.Text("VEYA", size=12, color=ft.Colors.GREY_500),
                        ft.Divider(expand=True),
                    ], alignment="center"),

                    ft.OutlinedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.G_MOBILEDATA, color=ft.Colors.RED),
                            ft.Text("Google ile Devam Et", color=ft.Colors.BLACK),
                        ], alignment="center", spacing=10),
                        width=350, height=50,
                        on_click=show_msg
                    ),

                    ft.Row([
                        ft.Text("Bir hesabınız yok mu?"),
                        ft.TextButton("Hemen Kayıt Ol", on_click=lambda _: self.page.go("/signup"))
                    ], alignment="center")
                ], spacing=15, horizontal_alignment="center")
            )
        ]

    def show_snack(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), action="OK")
        self.page.snack_bar.open = True
        self.page.update()