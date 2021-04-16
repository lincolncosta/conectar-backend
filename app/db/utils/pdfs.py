from sqlalchemy.orm import Session
from fastapi import HTTPException
from fpdf import FPDF
from datetime import datetime
from pathlib import Path

from app.db.pessoa_projeto.schemas import PessoaProjeto
from app.db.pessoa.crud import get_pessoa
from app.db.projeto.crud import get_projeto
from app.db.tipo_acordo.crud import get_tipo_acordo

FULL_MONTHS = {1: 'janeiro',  2: 'fevereiro', 3: u'março',    4: 'abril',
               5: 'maio',     6: 'junho',     7: 'julho',     8: 'agosto',
               9: 'setembro', 10: 'outubro',   11: 'novembro',  12: 'dezembro'}

path = Path("PDF/")

path.mkdir(parents=True, exist_ok=True)


class PDF(FPDF):

    def header(self):
        self.set_margins(20, 20, 20)
        self.image('app/db/utils/logoConectar.png', x=20, y=15, w=50)
        self.set_font("Arial", size=28)

    def footer(self):

        hoje = datetime.now()
        data_str = str(hoje.day) + " de " + \
            FULL_MONTHS[hoje.month] + ", " + str(hoje.year)

        self.cell(20, 175, txt='', ln=1)
        self.cell(175, 10, txt=data_str, ln=1, align="C")


def createPDF(db: Session, vaga: PessoaProjeto):

    colab = get_pessoa(db, vaga.pessoa_id)
    projeto = get_projeto(db, vaga.projeto_id)
    idealizador = get_pessoa(db, projeto.pessoa_id)
    acordo = get_tipo_acordo(db, vaga.tipo_acordo_id)

    pdf = PDF()
    pdf.add_page()

    # Espaço de formatação
    pdf.cell(20, 20, txt='', ln=1)
    pdf.cell(175, 10, txt=projeto.nome, ln=1, align="C")
    pdf.set_font("Arial", size=16)
    pdf.cell(175, 10, txt=idealizador.nome, ln=1, align="C")

    # Corpo
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=colab.nome, ln=1, align="L")
    # Observar após refatoração
    if(vaga.papel_id == 1):
        pdf.cell(200, 10, txt="Aliado", ln=1, align="L")
    elif(vaga.papel_id == 2):
        pdf.cell(200, 10, txt="Colaborador", ln=1,  align="L")
    pdf.cell(200, 10, txt=vaga.titulo, ln=1, align="L")
    pdf.cell(200, 10, txt=acordo.descricao, ln=1, align="L")

    saida = "PDF/acordo" + str(vaga.id) + str(colab.id) + \
        str(idealizador.id) + ".pdf"
    pdf.output(saida)

    return saida
