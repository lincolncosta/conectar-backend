from sqlalchemy.orm import Session
from fpdf import FPDF
from datetime import datetime
from pathlib import Path
import uuid
import os

if not os.getenv("DEV_ENV"):
    import boto3
    from botocore.exceptions import ClientError
    import logging

from app.db.pessoa_projeto.schemas import PessoaProjeto
from app.db.pessoa.crud import get_pessoa_by_id
from app.db.projeto.crud import get_projeto
from app.db.tipo_acordo.crud import get_tipo_acordo_by_id

MESES = {1: 'janeiro',  2: 'fevereiro', 3: u'março',    4: 'abril',
         5: 'maio',     6: 'junho',     7: 'julho',     8: 'agosto',
         9: 'setembro', 10: 'outubro',   11: 'novembro',  12: 'dezembro'}

PDF_PATH = "PDF/"
path = Path(PDF_PATH)

path.mkdir(parents=True, exist_ok=True)

def upload_object(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
      
    return True

if not os.getenv("DEV_ENV"):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ID"),
        aws_secret_access_key=os.getenv("AWS_KEY")
    )

def createPDFacordo(db: Session, vaga: PessoaProjeto):
    
    contratado = get_pessoa_by_id(db, vaga.pessoa_id)
    projeto = get_projeto(db, vaga.projeto_id)
    contratante = get_pessoa_by_id(db, projeto.pessoa_id)
    acordo = get_tipo_acordo_by_id(db, vaga.tipo_acordo_id)
    # Observar após refatoração
    if(vaga.papel_id == 1):
        papel = "aliado"
    elif(vaga.papel_id == 2):
        papel = "colaborador"
    elif(vaga.papel_id == 3):
        papel = "idealizador"

    pdf = FPDF()
    pdf.add_page(orientation='P')

    espacamento = 8

    pdf.set_margins(20,20,20)
    pdf.set_font("Arial", 'B', size=16)
    # Espaço de formatação
    pdf.cell(20, 20, txt='', ln=1)
    pdf.cell(175, 12, txt='ACORDO DE PRESTAÇÃO DE SERVIÇOS', ln=1, align="C")
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(175, 12, txt='IDENTIFICAÇÃO DAS PARTES CONTRATANTES', ln=1, align="L")

    # Corpo
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(pdf.get_string_width('CONTRATANTE: '), espacamento, txt='CONTRATANTE: ', align="L")
    pdf.set_font("Arial", size=12)
    w = pdf.get_x()
    pdf.cell(w, espacamento, txt=contratante.nome, ln=1, align="L")
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(pdf.get_string_width('CONTRATADO: '), espacamento, txt='CONTRATADO: ', align="L")
    pdf.set_font("Arial", size=12)
    w = pdf.get_x()
    pdf.cell(w, espacamento, txt=contratado.nome, ln=1, align="L")
    pdf.cell(20, 5, txt='', ln=1)
    pdf.multi_cell(0, espacamento, txt='As partes acima identificadas têm, entre si, justo e acertado o presente Acordo de Prestação de Serviços, que se regerá pelo objeto do acordo pelas condições de remuneração, forma e termo de pagamento descritas no presente.', align="J")
    
    pdf.set_font("Arial", 'B', size=14)
    
    pdf.cell(175, 15, txt='DO OBJETO DE ACORDO', ln=1, align="L")

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, espacamento, txt='É objeto do presente acordo a prestação do serviço no projeto ' + projeto.nome + ' como ' + papel + ' na vaga de ' + vaga.titulo + ' por meio de um contrato como ' + acordo.descricao + '.', align="J")
    
    if(vaga.remunerado):
        pdf.multi_cell(0, espacamento, txt='Esta prestação de serviços será remunerada com valores e pagamentos a serem negociados entre ambas as partes.', align="J")
    else:
        pdf.multi_cell(0, espacamento, txt='Esta prestação de serviços não será remunerada conforme anunciado na plataforma Conectar.', align="J")
    
    pdf.cell(20, 10, txt='', ln=1)

    pdf.multi_cell(0, espacamento, txt='A execução da prestação de serviço aqui acordada será de responsabilidade das partes envolvidas, eximindo da plataforma Conectar de qualquer obrigação com o contratante ou contratado.', align="J")

    hoje = datetime.now()
    data_str = 'Dois Vizinhos, ' + str(hoje.day) + " de " + MESES[hoje.month] + " de " + str(hoje.year)

    pdf.cell(20, 7, txt='', ln=1)
    pdf.cell(200, espacamento, txt=data_str, ln=1, align="L")

    pdf.cell(20, 20, txt='', ln=1)

    pdf.cell(175, espacamento, txt='___________________            ___________________', ln=1, align="C")
    pdf.cell(175, espacamento, txt='Contratante                            Contratado', ln=1, align="C")

    saida = str(uuid.uuid4().hex) + ".pdf"

    pdf.output(PDF_PATH + saida)

    if not os.getenv("DEV_ENV"):
        upload_object(PDF_PATH + saida , 'conectar')
    os.remove(PDF_PATH + saida)        

    

    return saida
