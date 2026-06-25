import json
import urllib.parse
import urllib.request
from kivy.lang import Builder
from kivymd.app import MDApp

# طراحی رابط کاربری اندروید (طراحی شده با KivyMD)
KV = """
MDScreen:
    md_bg_color: [0.95, 0.95, 0.95, 1]

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        MDLabel:
            text: "روایتگر هوشمند مذهبی"
            font_style: "H5"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            theme_text_color: "Primary"

        MDTextField:
            id: name_input
            hint_text: "نام شخصیت مورد نظر را وارد کنید"
            helper_text: "مثال: حسین بن علی"
            helper_text_mode: "on_focus"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.9
            base_direction: "rtl"

        MDRaisedButton:
            text: "جستجو و نمایش داستان"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.9
            md_bg_color: [0.15, 0.68, 0.37, 1]
            on_release: app.search_action()

        ScrollView:
            size_hint_y: 0.7
            md_bg_color: [1, 1, 1, 1]

            MDLabel:
                id: result_label
                text: "نتیجه جستجو اینجا نمایش داده می‌شود..."
                font_style: "Body1"
                halign: "right"
                size_hint_y: None
                height: self.texture_size[1]
                padding: [dp(15), dp(15)]
                base_direction: "rtl"
"""


class ReligiousApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def get_biography(self, name):
        # یکدست‌سازی حروف فارسی برای سرچ دقیق در ویکی‌پدیا
        name = name.replace("ي", "ی").replace("ك", "ک").strip()
        base_url = "https://fa.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": name,
        }
        url = base_url + "?" + urllib.parse.urlencode(params)

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
                pages = data["query"]["pages"]
                page_id = list(pages.keys())[0]

                if page_id != "-1":
                    return pages[page_id]["extract"]
                else:
                    return None
        except Exception as e:
            return f"خطا در اتصال به اینترنت: {e}"

    def search_action(self):
        target_name = self.root.ids.name_input.text.strip()

        if not target_name:
            self.root.ids.result_label.text = (
                "لطفاً ابتدا نام مورد نظر را وارد کنید!"
            )
            return

        self.root.ids.result_label.text = "در حال جستجو..."

        bio = self.get_biography(target_name)

        if bio and bio.strip():
            self.root.ids.result_label.text = bio
        else:
            self.root.ids.result_label.text = (
                f"متأسفانه صفحه‌ای با نام «{target_name}» پیدا نشد.\n\n"
                f"نکته: نام را به صورت کامل وارد کنید (مثال: حسین بن علی)"
            )


if __name__ == "__main__":
    ReligiousApp().run()