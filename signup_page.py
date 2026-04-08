import flet as ft
from database import register_user  

class SignupPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/signup",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE, 
        )
        
        self.name_field = ft.TextField(hint_text="Örn. Ahmet Yılmaz", prefix_icon=ft.Icons.PERSON_OUTLINE, border_radius=10)
        self.email_field = ft.TextField(hint_text="ahmet@istan.com", prefix_icon=ft.Icons.EMAIL_OUTLINED, border_radius=10)
        self.phone_field = ft.TextField(hint_text="+90 5XX XXX XX XX", prefix_icon=ft.Icons.PHONE_OUTLINED, border_radius=10)
        self.pass_field = ft.TextField(hint_text="********", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=10)
        self.pass_confirm_field = ft.TextField(hint_text="********", password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=10)

        def handle_signup(e):
            name = self.name_field.value
            email = self.email_field.value
            password = self.pass_field.value
            confirm_password = self.pass_confirm_field.value

            if not name or not email or not password:
                self.show_snack("Lütfen gerekli alanları doldurun!")
                return

            if password != confirm_password:
                self.show_snack("Şifreler uyuşmuyor!")
                return

            if register_user(email, password): # database.py funksiyasını çağırırıq
                print(f"Kayıt başarılı: {email}")
                self.show_snack("Kayıt başarılı! Giriş yapabilirsiniz.")
                page.go("/") # Uğurludursa Login səhifəsinə göndər
            else:
                self.show_snack("Bu e-posta zaten kullanımda!")

        self.controls = [
            ft.Container(
                width=400,
                padding=20,
                content=ft.Column([
                    ft.Column([
                        ft.Text("Aramıza Katılın", size=28, weight="bold"),
                        ft.Text("Lütfen hesap oluşturmak için bilgilerinizi girin.", 
                                size=14, color=ft.Colors.GREY_600),
                    ], spacing=5),

                    ft.Column([
                        ft.Text("Ad Soyad", weight="bold", size=14),
                        self.name_field,
                        
                        ft.Text("E-posta", weight="bold", size=14),
                        self.email_field,
                        
                        ft.Text("Telefon Numarası", weight="bold", size=14),
                        self.phone_field,
                        
                        ft.Text("Şifre", weight="bold", size=14),
                        self.pass_field,
                        
                        ft.Text("Şifre Tekrar", weight="bold", size=14),
                        self.pass_confirm_field,
                    ], spacing=8),

                    ft.Button(
                        content=ft.Row([
                            ft.Text("Kayıt Ol", size=16, weight="bold"),
                            ft.Icon(ft.Icons.ARROW_FORWARD, size=20),
                        ], alignment="center", spacing=10),
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        width=400,
                        height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=handle_signup # <--- Məntiq bura bağlandı
                    ),

                    ft.Text(
                        "Hesap oluşturarak, Kullanım Koşullarını ve Gizlilik Politikasını kabul etmiş olursunuz.",
                        size=11, text_align="center", color=ft.Colors.GREY_500
                    ),

                    ft.Row([
                        ft.Divider(expand=True),
                        ft.Text("VEYA ŞUNUNLA DEVAM ET", size=12, color=ft.Colors.GREY_500),
                        ft.Divider(expand=True),
                    ], alignment="center"),

                    # Sosial Düymələr
                    ft.OutlinedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.G_MOBILEDATA, color=ft.Colors.RED_400),
                            ft.Text("Google ile Kayıt Ol", color=ft.Colors.BLACK),
                        ], alignment="center"),
                        width=400, height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                    ),
                    ft.OutlinedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.APPLE, color=ft.Colors.BLACK),
                            ft.Text("Apple ile Kayıt Ol", color=ft.Colors.BLACK),
                        ], alignment="center"),
                        width=400, height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                    ),

                    ft.Row([
                        ft.Text("Zaten bir hesabınız var mı?"),
                        ft.TextButton("Giriş Yap", on_click=lambda _: page.go("/"))
                    ], alignment="center")
                    
                ], spacing=15, horizontal_alignment="center")
            )
        ]

    def show_snack(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), action="OK")
        self.page.snack_bar.open = True
        self.page.update()