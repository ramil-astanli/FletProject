import flet as ft
import httpx

class SignupPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/signup",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE, 
        )
        
     
        
        self.name_field = ft.TextField(label="Ad Soyad", hint_text="Örn. Ahmet Yılmaz", prefix_icon=ft.Icons.PERSON_OUTLINE, border_radius=10, width=350)
        self.email_field = ft.TextField(label="E-posta", hint_text="ahmet@istan.com", prefix_icon=ft.Icons.EMAIL_OUTLINED, border_radius=10, width=350)
        self.phone_field = ft.TextField(label="Telefon", hint_text="+90 5XX XXX XX XX", prefix_icon=ft.Icons.PHONE_OUTLINED, border_radius=10, width=350)
        self.pass_field = ft.TextField(label="Şifre", hint_text="********", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=10, width=350)
        self.pass_confirm_field = ft.TextField(label="Şifre Tekrar", hint_text="********", password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=10, width=350)

        def handle_signup(e):
            if not self.name_field.value or not self.email_field.value or not self.pass_field.value:
                self.show_snack("Lütfen gerekli alanları doldurun!")
                return
            if self.pass_field.value != self.pass_confirm_field.value:
                self.show_snack("Şifreler uyuşmuyor!")
                return

            try:
                with httpx.Client() as client:
                    response = client.post(
                        "http://127.0.0.1:8000/signup", 
                        json={
                            "email": self.email_field.value, 
                            "password": self.pass_field.value,
                            "name": self.name_field.value
                        }
                    )
                
                if response.status_code == 200:
                    self.show_snack("Kayıt başarılı!")
                    self.page.go("/")
                else:
                    self.show_snack("Hata oluştu!")
            except Exception:
                self.show_snack("Sunucuya bağlanılamadı!")

        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text("Kayıt Ol", size=30, weight="bold"),
                    self.name_field,
                    self.email_field,
                    self.phone_field,
                    self.pass_field,
                    self.pass_confirm_field,
                    ft.ElevatedButton(
                        "Kaydı Tamamla",
                        on_click=handle_signup,
                        width=350,
                        height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                    ),
                    ft.TextButton("Zaten hesabınız var mı? Giriş yapın", on_click=lambda _: self.page.go("/"))
                ], horizontal_alignment="center", spacing=15),
                padding=20
            )
        ]

    def show_snack(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), action="OK")
        self.page.snack_bar.open = True
        self.page.update()