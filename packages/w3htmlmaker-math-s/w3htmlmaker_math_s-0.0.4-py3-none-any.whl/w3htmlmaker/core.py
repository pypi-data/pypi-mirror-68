import re


class HtmlArticle:
    title = ""
    text_html = ""

    def __init__(self, text, title):
        self.text_html = text
        self.title = title.capitalize()
        self.make_p()
        self.make_quote()
        self.make_short_code()
        self.make_code()
        self.make_title()
        self.make_container()

    def get_html(self):
        return self.text_html

    def make_container(self):
        self.text_html = "<div class=\"w3-container\">\n" + self.text_html + "</div>"

    def make_p(self):
        self.text_html = "<p>" + self.text_html.replace('\n', "</p><p>") + "</p>"
        self.text_html = self.text_html.replace("<p></longcode></p>", "\n</longcode>\n")
        self.text_html = self.text_html.replace("<p><longcode></p>", "\n<longcode>\n")
        self.text_html = self.text_html.replace("<p><quote></p>", "\n<quote>\n")
        self.text_html = self.text_html.replace("<p></quote></p>", "\n</quote>\n")
        self.text_html = self.text_html.replace("</p><p>", "</p>\n<p>")

    def make_quote(self):
        self.text_html = self.text_html.replace('<quote>', """
<div class="w3-panel w3-leftbar">
    <i class="fa fa-quote-right w3-xxlarge"></i>
        <i class="w3-serif w3-xlarge">
        """)
        self.text_html = self.text_html.replace('</quote>', "</i></div>")

    def make_short_code(self):
        self.text_html = self.text_html.replace('<shortcode>', "<code class=\"w3-codespan\">")
        self.text_html = self.text_html.replace('</shortcode>', "</code>")

    def make_title(self):
        self.text_html = "\t<h1>" + self.title + "</h1>\n" + self.text_html

    def make_code(self):
        self.text_html = self.text_html.replace("<longcode>", """
<div class="w3-container">
    <div class="w3-panel w3-card w3-light-grey">
        <div class="w3-code pythonHigh notranslate">""")
        self.text_html = self.text_html.replace("</longcode>", "</div>\n</div>\n</div>\n")


