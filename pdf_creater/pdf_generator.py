

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import qrcode
from PIL import Image
from tempfile import NamedTemporaryFile
from random_vin import gen_vin
import PyPDF2
import os 

class PDFGenerator:
    def __init__(self, filename="output.pdf"):
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4 #(595.2755905511812, 841.8897637795277)
        pdfmetrics.registerFont(TTFont("FreeSans", "FreeSans.ttf"))

    def add_text(self, text, x, y, font="Helvetica", size=12):
        self.canvas.setFont(font, size)
        self.canvas.drawString(x, y, text)

    def add_text_list(self):
        texts = [
            "Здравствуйте, студенты!",
            "Помогите нашему проекту по HTR.",
            "Вам предложена случайная последовательность символов",
            "и области для заполнения рукописным текстом.",
            "Что нужно сделать:",
            "1. Заполните любое количество полей на ваше усмотрение.",
            "2. Если все поля заполнены, сфотографируйте листочек и отправьте фото в телеграм-бот,",
            "используя QR-код в правом верхнем углу.",
            "3. После этого можете выбросить листочек.",
            "Спасибо за помощь!"
        ]
        for i,text in enumerate(texts):
            self.add_text(text, 20, 810-i*10, font="FreeSans", size=10)




    def add_qrcode(self, data, x, y, size=100):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill="black", back_color="white").convert("RGB")
        
        with NamedTemporaryFile(suffix=".png") as tmpfile:
            img.save(tmpfile, format="PNG")
            tmpfile.flush()  # Ensure all data is written
            self.canvas.drawImage(tmpfile.name, x, y, width=size, height=size)

    def add_rectangle(self, x, y, width, height, color=colors.black, fill=False):
        self.canvas.setStrokeColor(color)
        if fill:
            self.canvas.setFillColor(color)
            self.canvas.rect(x, y, width, height, fill=1)
        else:
            self.canvas.rect(x, y, width, height, fill=0)


    def add_square(self, x, y, size, color=colors.black, fill=False):
        self.add_rectangle(x, y, size, size, color=color, fill=fill)

    def save(self):
        self.canvas.save()



def concatenate_pdfs(path_in, path_out):
    pdf_writer = PyPDF2.PdfWriter()
    for pdf_file in os.listdir(path_in):
        with open(f'{path_in}/{pdf_file}', "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
    with open(path_out, "wb") as output_file:
        pdf_writer.write(output_file)


def clean(path_in):
    for pdf_file in os.listdir(path_in):
        os.remove(f'{path_in}/{pdf_file}')
    os.rmdir(path_in)


def generate_ocr(count, path_in, path_out):
    pdf_ids_vins_map = dict()
    pages =[]
    clean(path_in)
    os.mkdir(path_in)
    for id_pdf in range(count):
        pdf = PDFGenerator(f"{path_in}/page{id_pdf}.pdf")
        pdf.add_text("ITMO HTR", 20, 820, font="Helvetica", size=18)
        pdf.add_text(str(id_pdf), 400, 820, font="Helvetica", size=18)
        pdf.add_text_list()
        pdf.add_qrcode("https://t.me/itmo_htr_bot", 500, 760, size=80)
        start_pos = 710
        wight = 400
        shift = 40
        vins = gen_vin(18)
        for i,vin in enumerate(vins):
            for j,a in enumerate(vin):
                pdf.add_text(a, 27+wight/17*j, start_pos-i*shift, font="FreeSans", size=10)
                pdf.add_square(20+wight/17*j, start_pos-25-i*shift, wight/17, color=colors.black, fill=False)
        pdf.save()
        pdf_ids_vins_map[id_pdf] = vins
    concatenate_pdfs(path_in, path_out)
    clean(path_in)

    return pdf_ids_vins_map
