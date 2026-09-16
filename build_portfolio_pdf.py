from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf" / "Adusei_Kenneth_Client_Portfolio.pdf"

W, H = A4
M = 42
INK = colors.HexColor("#26384E")
NAVY = colors.HexColor("#1E3045")
PAPER = colors.HexColor("#FBFAF6")
CREAM = colors.HexColor("#F1EEE7")
MIST = colors.HexColor("#E8EEF7")
BLUE = colors.HexColor("#A9C8FF")
RED = colors.HexColor("#D91F3A")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#D9D6CE")
WHITE = colors.white


def set_font(c, face="Helvetica", size=10):
    c.setFont(face, size)


def wrap(c, text, width, font="Helvetica", size=10, leading=None):
    leading = leading or size * 1.45
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = word if not current else current + " " + word
        if stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines, leading


def paragraph(c, text, x, y, width, font="Helvetica", size=10, color=INK, leading=None):
    lines, leading = wrap(c, text, width, font, size, leading)
    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def label(c, text, x, y, color=RED):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x, y, text.upper())


def rule(c, x1, y, x2, color=LINE):
    c.setStrokeColor(color)
    c.setLineWidth(.65)
    c.line(x1, y, x2, y)


def footer(c, page, dark=False):
    col = colors.HexColor("#B8C2D0") if dark else MUTED
    c.setFillColor(col)
    c.setFont("Helvetica", 7.5)
    c.drawString(M, 22, "ADUSEI KENNETH  /  CLIENT PORTFOLIO")
    c.drawRightString(W - M, 22, f"{page:02d}")


def image_crop(c, filename, x, y, width, height, anchor="center"):
    path = ROOT / filename
    with Image.open(path) as img:
        iw, ih = img.size
    scale = max(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    if anchor == "top":
        dx, dy = x + (width - dw) / 2, y + height - dh
    elif anchor == "bottom":
        dx, dy = x + (width - dw) / 2, y
    else:
        dx, dy = x + (width - dw) / 2, y + (height - dh) / 2
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, width, height)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), dx, dy, width=dw, height=dh, mask="auto")
    c.restoreState()


def cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # Selected-work collage
    panel_x = W * .62
    c.setFillColor(BLUE)
    c.rect(panel_x, 0, W-panel_x, H, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(panel_x + 21, H-49, "SELECTED VISUAL WORK")
    c.setFont("Helvetica", 7)
    c.drawRightString(W-20, H-49, "01 - 03")
    # Main card
    c.setFillColor(WHITE)
    c.roundRect(panel_x + 19, 401, W-panel_x-38, 255, 7, stroke=0, fill=1)
    image_crop(c, "assets/Fellows ROUNDTABLE-.png", panel_x + 25, 446, W-panel_x-50, 200, "top")
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.3)
    c.drawString(panel_x + 25, 425, "EVENT DESIGN")
    c.setFont("Helvetica", 8.2)
    c.drawString(panel_x + 25, 412, "Fellows Roundtable")
    # Two accompanying cards create a concise design contact sheet.
    small_w = (W-panel_x-44) / 2
    for file, x, kind in [
        ("assets/Travel.png", panel_x+19, "CAMPAIGN"),
        ("assets/YAMME.png", panel_x+25+small_w, "BRAND"),
    ]:
        c.setFillColor(WHITE)
        c.roundRect(x, 205, small_w, 165, 6, stroke=0, fill=1)
        image_crop(c, file, x+5, 232, small_w-10, 128, "top")
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 6.6)
        c.drawString(x+6, 216, kind)
    c.setFillColor(NAVY)
    c.roundRect(panel_x + 19, 150, W-panel_x-38, 29, 14.5, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(panel_x + (W-panel_x)/2, 160, "WEB + DESIGN + SYSTEMS")

    label(c, "Independent creative and developer", M, H-62, BLUE)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(M, H-125, "Adusei")
    c.setFillColor(BLUE)
    c.drawString(M, H-168, "Kenneth.")
    c.setFillColor(colors.HexColor("#D7DEE7"))
    paragraph(c, "I build clear, dependable digital experiences and visual communications that help businesses move forward.", M, H-232, 285, "Helvetica", 13, colors.HexColor("#D7DEE7"), 20)
    rule(c, M, 210, panel_x-27, colors.HexColor("#506276"))
    label(c, "Services", M, 189, BLUE)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 10.4)
    c.drawString(M, 168, "Websites  -  Web applications")
    c.drawString(M, 149, "Brand design  -  Campaign creative")
    c.setFillColor(colors.HexColor("#B8C2D0"))
    c.setFont("Helvetica", 8)
    c.drawString(M, 62, "ACCRA, GHANA  /  AVAILABLE WORLDWIDE")
    c.drawString(M, 45, "hello@aduseimedia.codes  /  +233 55 426 6661")


def services(c):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "01 / What I do", M, H-55)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 30)
    c.drawString(M, H-95, "Useful work, built to last.")
    paragraph(c, "I work across the full path from first idea to launch. That means your message, experience, and technical foundations can stay aligned.", M, H-130, 380, "Helvetica", 11.5, MUTED, 17)
    cards = [
        ("01", "Websites & interfaces", "Responsive, accessible sites and product interfaces with a clear path for your audience."),
        ("02", "Web applications", "Practical tools and workflows that turn manual processes into clear, usable software."),
        ("03", "Backend & data", "APIs, authentication, data models, validation, and the operational layer behind the interface."),
        ("04", "Brand & campaign design", "Visual identity, social assets, promotional graphics, and presentation-ready campaign creative."),
    ]
    card_w, card_h = 248, 145
    for i, (num, title, copy) in enumerate(cards):
        col, row = i % 2, i // 2
        x, y = M + col * (card_w + 15), 398 - row * (card_h + 15)
        c.setFillColor(WHITE); c.roundRect(x, y, card_w, card_h, 5, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.roundRect(x, y, card_w, card_h, 5, stroke=1, fill=0)
        c.setFillColor(RED); c.setFont("Helvetica-Bold", 9); c.drawString(x+17, y+card_h-25, num)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 14); c.drawString(x+17, y+card_h-51, title)
        paragraph(c, copy, x+17, y+card_h-73, card_w-34, "Helvetica", 9.2, MUTED, 13.5)
    c.setFillColor(CREAM); c.roundRect(M, 85, W-2*M, 86, 5, stroke=0, fill=1)
    label(c, "Why work with me", M+17, 147)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 14)
    c.drawString(M+17, 124, "One partner for the thinking, the experience, and the build.")
    c.setFillColor(MUTED); c.setFont("Helvetica", 9.5)
    c.drawString(M+17, 104, "Clear communication, appropriate solutions, clean handover, and support when it counts.")
    footer(c, 2)


def products(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "02 / Digital product work", M, H-55, BLUE)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 30)
    c.drawString(M, H-95, "Designed to be used.")
    paragraph(c, "A selection of live products and web experiences. Each focuses on clarity, practical function, and a thoughtful journey from entry to action.", M, H-130, 410, "Helvetica", 11.5, colors.HexColor("#C8D1DD"), 17)
    works = [
        ("QR Code Scanner", "A browser-based utility for scanning QR codes.", "https://aduseimedia-eng.github.io/qr-scanner/", "assets/site-previews/qr-scanner-home.png"),
        ("Draftly", "A free online CV maker for creating professional CVs.", "https://aduseimedia-eng.github.io/draftly/", "assets/site-previews/draftly-home.png"),
        ("Kudisave", "A live expense-tracking web application.", "https://kudisave.com", "assets/site-previews/kudisave-home.png"),
        ("Aurea Estates", "A refined real-estate website for exceptional homes in Accra.", "https://aduseimedia-eng.github.io/aurea/", "assets/site-previews/aurea-home.png"),
    ]
    card_w, card_h = 248, 194
    for i, (name, copy, url, screenshot) in enumerate(works):
        col, row = i % 2, i // 2
        x, y = M + col * (card_w + 15), 398 - row * (card_h + 15)
        c.setFillColor(colors.HexColor("#294158")); c.roundRect(x, y, card_w, card_h, 5, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor("#506276")); c.roundRect(x, y, card_w, card_h, 5, stroke=1, fill=0)
        # Current homepage preview, framed like a compact browser window.
        c.setFillColor(colors.HexColor("#E9EDF2")); c.roundRect(x+15, y+85, card_w-30, 93, 3, stroke=0, fill=1)
        image_crop(c, screenshot, x+17, y+87, card_w-34, 89, "top")
        c.setFillColor(colors.HexColor("#F7F8F9")); c.rect(x+17, y+166, card_w-34, 10, stroke=0, fill=1)
        for dot_x, dot_color in [(x+23, RED), (x+29, colors.HexColor("#E5A13A")), (x+35, colors.HexColor("#57A574"))]:
            c.setFillColor(dot_color); c.circle(dot_x, y+171, 1.6, stroke=0, fill=1)
        c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 7.2); c.drawString(x+17, y+70, f"0{i+1} / LIVE HOMEPAGE")
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 12.5); c.drawString(x+17, y+51, name)
        paragraph(c, copy, x+17, y+35, card_w-34, "Helvetica", 7.8, colors.HexColor("#C8D1DD"), 10)
        c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 8); c.drawString(x+17, y+16, "VIEW LIVE SITE  ->")
        c.linkURL(url, (x, y, x+card_w, y+card_h), relative=0)
    c.setFillColor(colors.HexColor("#C8D1DD")); c.setFont("Helvetica", 9)
    c.drawString(M, 80, "The project cards above are clickable in the digital PDF.")
    footer(c, 3, dark=True)


def design(c):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "03 / Selected visual work", M, H-55)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 30)
    c.drawString(M, H-95, "Design that carries the message.")
    paragraph(c, "A sample of campaign, promotional, and brand communication work created for clear attention and confident delivery.", M, H-130, 400, "Helvetica", 11.2, MUTED, 16)
    images = [
        ("assets/Travel.png", "Campaign artwork", "Heightlinks Travel & Logistics"),
        ("assets/Fellows ROUNDTABLE-.png", "Event design", "Fellows Roundtable"),
        ("assets/idcard.png", "Identity system", "Staff ID cards"),
        ("assets/smoothie.png", "Promotional design", "Smoothie campaign"),
        ("assets/Kofi tech.png", "Brand communication", "Phone Hub"),
        ("assets/YAMME.png", "Brand communication", "Yamme"),
    ]
    gap, cell_w, cell_h = 10, 161, 175
    for i, (file, kind, title) in enumerate(images):
        col, row = i % 3, i // 3
        x, y = M + col * (cell_w + gap), 350 - row * (cell_h + 37)
        c.setFillColor(WHITE); c.rect(x, y, cell_w, cell_h, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.rect(x, y, cell_w, cell_h, stroke=1, fill=0)
        image_crop(c, file, x+1, y+1, cell_w-2, cell_h-2, "top")
        c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7); c.drawString(x, y-14, kind.upper())
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawString(x, y-27, title)
    footer(c, 4)


def process_contact(c):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "04 / How we can work together", M, H-55)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 30)
    c.drawString(M, H-95, "A straightforward process.")
    steps = [
        ("01", "Discover", "We clarify the goal, audience, constraints, and what success should look like."),
        ("02", "Shape", "I turn the brief into a considered direction, plan, and practical next steps."),
        ("03", "Build", "We develop with feedback loops, so the work stays focused and useful."),
        ("04", "Launch", "You receive a clean handover, full files, and support for what comes next."),
    ]
    x0, y0, sw = M, H-165, 124
    for i, (num, title, copy) in enumerate(steps):
        x = x0 + i * sw
        c.setFillColor(RED); c.setFont("Helvetica-Bold", 8); c.drawString(x, y0, num)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 12); c.drawString(x, y0-24, title)
        paragraph(c, copy, x, y0-42, sw-12, "Helvetica", 8.2, MUTED, 11.5)
    rule(c, M, 435, W-M)
    c.setFillColor(NAVY); c.roundRect(M, 120, W-2*M, 260, 7, stroke=0, fill=1)
    label(c, "Let’s collaborate", M+25, 345, BLUE)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 26)
    c.drawString(M+25, 304, "Have a project in mind?")
    paragraph(c, "Whether you need a brand, a build, or a clearer way forward, I’d love to hear what you are working on.", M+25, 273, 290, "Helvetica", 11, colors.HexColor("#D7DEE7"), 16)
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 12); c.drawString(M+25, 205, "hello@aduseimedia.codes")
    c.setFillColor(WHITE); c.setFont("Helvetica", 10); c.drawString(M+25, 181, "+233 55 426 6661  |  WhatsApp: +233 57 822 4669")
    c.setFillColor(colors.HexColor("#C8D1DD")); c.setFont("Helvetica", 9); c.drawString(M+25, 151, "Accra, Ghana  |  Available worldwide")
    c.linkURL("mailto:hello@aduseimedia.codes", (M+25, 195, M+245, 218), relative=0)
    footer(c, 5, dark=False)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
    c.setTitle("Adusei Kenneth - Client Portfolio")
    c.setAuthor("Adusei Kenneth")
    c.setSubject("Client portfolio: web development, digital products, and visual design")
    for page in (cover, services, products, design, process_contact):
        page(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
