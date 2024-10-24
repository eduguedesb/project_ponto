import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDateEdit)
from PyQt5.QtCore import QDate
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# Nome do arquivo JSON
ARQUIVO_JSON = 'registro_ponto.json'

# Carga horária diária esperada
CARGA_HORARIA = timedelta(hours=8, minutes=30)

# Carrega o arquivo JSON ou inicializa um novo
def carregar_dados():
    try:
        with open(ARQUIVO_JSON, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'banco_de_horas': 0, 'registros': [], 'data_reset': None}

# Salva os dados no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_JSON, 'w') as f:
        json.dump(dados, f, indent=4)

# Função para verificar e resetar o banco de horas com base na data
def verificar_reset_banco_horas(dados):
    data_reset = dados.get('data_reset')
    if data_reset:
        data_reset = datetime.strptime(data_reset, '%Y-%m-%d').date()
        if datetime.now().date() >= data_reset:
            dados['banco_de_horas'] = 0
            QMessageBox.information(None, "Banco de Horas", "Banco de horas resetado!")
            dados['data_reset'] = None

# Função para gerar o relatório PDF em formato de tabela
def gerar_relatorio_pdf(dados):
    try:
        # Criar o PDF
        pdf_file = "Relatorio_Ponto.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)

        # Estilos
        estilo_titulo = getSampleStyleSheet()['Title']
        estilo_cabecalho = getSampleStyleSheet()['Heading3']
        estilo_cabecalho.alignment = TA_CENTER

        elementos = []

        # Título
        titulo = Paragraph("Relatório de Registro de Ponto", estilo_titulo)
        elementos.append(titulo)

        # Banco de horas
        banco_de_horas = Paragraph(f"Banco de Horas Atual: {dados['banco_de_horas']} minutos", estilo_cabecalho)
        elementos.append(banco_de_horas)

        # Cabeçalhos da tabela
        data = [['Data', 'Entrada Manhã', 'Saída Manhã', 'Entrada Tarde', 'Saída Tarde', 'Horas Trabalhadas']]

        # Adicionar registros
        for registro in dados['registros']:
            data_formatada = datetime.strptime(registro['data'], '%Y-%m-%d').strftime('%d/%m/%Y')
            entrada_manha = registro.get('entrada_manha', 'N/A')
            saida_manha = registro.get('saida_manha', 'N/A')
            entrada_tarde = registro.get('entrada_tarde', 'N/A')
            saida_tarde = registro.get('saida_tarde', 'N/A')
            horas_trabalhadas = registro.get('horas_trabalhadas', 'N/A')

            data.append([data_formatada, entrada_manha, saida_manha, entrada_tarde, saida_tarde, horas_trabalhadas])

        # Criar tabela
        tabela = Table(data)

        # Estilo da tabela
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Linhas da tabela
        ])

        tabela.setStyle(estilo_tabela)
        elementos.append(tabela)

        # Constrói o PDF
        doc.build(elementos)
        QMessageBox.information(None, "Relatório PDF", "Relatório PDF gerado com sucesso!")
    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro ao gerar relatório: {e}")

# Classe principal da aplicação
class PontoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relógio de Ponto")

        # Carregar dados do JSON
        self.dados = carregar_dados()

        # Verificar se o banco de horas precisa ser resetado
        verificar_reset_banco_horas(self.dados)

        # Labels e campos de entrada para os horários
        self.entrada_manha = QLineEdit(self)
        self.saida_manha = QLineEdit(self)
        self.entrada_tarde = QLineEdit(self)
        self.saida_tarde = QLineEdit(self)

        # Carregar horários já informados para o dia atual
        self.carregar_horarios_dia_atual()

        # Label para exibir o banco de horas
        self.banco_horas_label = QLabel(f"Banco de Horas Atual: {self.dados['banco_de_horas']} minutos")

        # Campo para data de reset do banco de horas com calendário
        self.reset_date_edit = QDateEdit(self)
        self.reset_date_edit.setCalendarPopup(True)
        if self.dados['data_reset']:
            self.reset_date_edit.setDate(QDate.fromString(self.dados['data_reset'], 'yyyy-MM-dd'))
        else:
            self.reset_date_edit.setDate(QDate.currentDate())
        self.reset_date_edit.dateChanged.connect(self.atualizar_data_reset)

        # Botão para registrar o ponto
        self.registrar_ponto_btn = QPushButton("Registrar Ponto")
        self.registrar_ponto_btn.clicked.connect(self.registrar_ponto)

        # Botão para gerar o relatório PDF
        self.gerar_relatorio_btn = QPushButton("Relatório em PDF")
        self.gerar_relatorio_btn.clicked.connect(lambda: gerar_relatorio_pdf(self.dados))

        # Layout principal
        layout = QVBoxLayout()

        # Adiciona os campos de horário ao layout
        layout.addWidget(QLabel("Entrada Manhã (HH:MM):"))
        layout.addWidget(self.entrada_manha)
        layout.addWidget(QLabel("Saída Manhã (HH:MM):"))
        layout.addWidget(self.saida_manha)
        layout.addWidget(QLabel("Entrada Tarde (HH:MM):"))
        layout.addWidget(self.entrada_tarde)
        layout.addWidget(QLabel("Saída Tarde (HH:MM):"))
        layout.addWidget(self.saida_tarde)

        # Adiciona o botão para registrar o ponto
        layout.addWidget(self.registrar_ponto_btn)

        # Adiciona o campo de data de reset com o calendário
        layout.addWidget(QLabel("Data para reset do Banco de Horas:"))
        layout.addWidget(self.reset_date_edit)

        # Adiciona o label do banco de horas
        layout.addWidget(self.banco_horas_label)

        # Adiciona o botão para gerar relatório em PDF
        layout.addWidget(self.gerar_relatorio_btn)

        self.setLayout(layout)

        # Variável para armazenar o tempo excedente do intervalo de almoço
        self.excedente_almoco = timedelta()

    # Função para carregar horários já informados para o dia atual
    def carregar_horarios_dia_atual(self):
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        registro_hoje = None
        for registro in self.dados['registros']:
            if registro['data'] == data_hoje:
                registro_hoje = registro
                break

        # Se houver horários para o dia atual, exibe-os nos campos e bloqueia a edição
        if registro_hoje:
            self.entrada_manha.setText(registro_hoje.get('entrada_manha', ''))
            self.saida_manha.setText(registro_hoje.get('saida_manha', ''))
            self.entrada_tarde.setText(registro_hoje.get('entrada_tarde', ''))
            self.saida_tarde.setText(registro_hoje.get('saida_tarde', ''))

            # Bloquear edição dos horários já preenchidos
            if registro_hoje.get('entrada_manha'):
                self.entrada_manha.setDisabled(True)
            if registro_hoje.get('saida_manha'):
                self.saida_manha.setDisabled(True)
            if registro_hoje.get('entrada_tarde'):
                self.entrada_tarde.setDisabled(True)
            if registro_hoje.get('saida_tarde'):
                self.saida_tarde.setDisabled(True)
        else:
            # Se for um novo dia, limpa os campos
            self.limpar_campos()

    # Função para registrar os horários de ponto
    def registrar_ponto(self):
        data_hoje = datetime.now().strftime('%Y-%m-%d')

        horarios = {
            'entrada_manha': self.entrada_manha.text(),
            'saida_manha': self.saida_manha.text(),
            'entrada_tarde': self.entrada_tarde.text(),
            'saida_tarde': self.saida_tarde.text()
        }

        # Atualiza ou cria o registro do dia atual
        registro_existente = None
        for registro in self.dados['registros']:
            if registro['data'] == data_hoje:
                registro_existente = registro
                break

        if registro_existente:
            registro_existente.update(horarios)
        else:
            registro_existente = {
                'data': data_hoje,
                'entrada_manha': horarios['entrada_manha'],
                'saida_manha': horarios['saida_manha'],
                'entrada_tarde': horarios['entrada_tarde'],
                'saida_tarde': horarios['saida_tarde'],
                'horas_trabalhadas': ''
            }
            self.dados['registros'].append(registro_existente)

        # Salva os dados no JSON antes de qualquer cálculo
        salvar_dados(self.dados)

        # Verifica se todos os horários foram preenchidos para realizar o cálculo
        if all(horarios.values()):
            try:
                entrada_manha = self.converter_para_datetime(horarios['entrada_manha'])
                saida_manha = self.converter_para_datetime(horarios['saida_manha'])
                entrada_tarde = self.converter_para_datetime(horarios['entrada_tarde'])
                saida_tarde = self.converter_para_datetime(horarios['saida_tarde'])
            except ValueError:
                QMessageBox.warning(self, "Erro", "Por favor, insira os horários no formato HH:MM.")
                return

            # Calcula as horas trabalhadas pela manhã e pela tarde
            horas_trabalhadas_manha = saida_manha - entrada_manha
            horas_trabalhadas_tarde = saida_tarde - entrada_tarde
            horas_trabalhadas = horas_trabalhadas_manha + horas_trabalhadas_tarde

            # Verifica o intervalo de almoço
            intervalo_almoco = entrada_tarde - saida_manha
            intervalo_minimo = timedelta(hours=1)

            # Se o intervalo de almoço for maior que 60 minutos, armazena a diferença
            if intervalo_almoco > intervalo_minimo:
                diferenca_intervalo = intervalo_almoco - intervalo_minimo
                self.excedente_almoco = diferenca_intervalo

            # Atualiza o banco de horas
            diferenca = horas_trabalhadas - CARGA_HORARIA
            if diferenca.total_seconds() > 0:
                self.dados['banco_de_horas'] += diferenca.total_seconds() // 60  # converte para minutos
            elif diferenca.total_seconds() < 0:
                self.dados['banco_de_horas'] -= abs(diferenca.total_seconds()) // 60  # converte para minutos

            # Subtrai o excedente do intervalo de almoço do banco de horas (se houver)
            if self.excedente_almoco.total_seconds() > 0:
                self.dados['banco_de_horas'] -= self.excedente_almoco.total_seconds() // 60  # subtrai o excedente em minutos

            # Atualiza o registro com as horas trabalhadas
            registro_existente['horas_trabalhadas'] = str(horas_trabalhadas)

            # Atualiza a exibição do banco de horas e salva os dados
            self.banco_horas_label.setText(f"Banco de Horas Atual: {self.dados['banco_de_horas']} minutos")
            salvar_dados(self.dados)

            QMessageBox.information(self, "Sucesso", "Horários registrados e banco de horas atualizado!")

            # Bloquear campos que foram preenchidos e salvos
            self.bloquear_campos_preenchidos()
        else:
            # Salva parcialmente se nem todos os horários estiverem preenchidos
            salvar_dados(self.dados)
            QMessageBox.information(self, "Horários Salvos", "Horários parciais salvos. O cálculo será feito quando todos os quatro horários forem preenchidos.")

    # Função para converter texto de horário (HH:MM) para datetime
    def converter_para_datetime(self, horario):
        return datetime.strptime(horario, '%H:%M')

    # Função para bloquear os campos de horários que já foram preenchidos
    def bloquear_campos_preenchidos(self):
        if self.entrada_manha.text():
            self.entrada_manha.setDisabled(True)
        if self.saida_manha.text():
            self.saida_manha.setDisabled(True)
        if self.entrada_tarde.text():
            self.entrada_tarde.setDisabled(True)
        if self.saida_tarde.text():
            self.saida_tarde.setDisabled(True)

    # Função para atualizar a data de reset e salvar no arquivo JSON
    def atualizar_data_reset(self):
        nova_data = self.reset_date_edit.date().toString('yyyy-MM-dd')
        self.dados['data_reset'] = nova_data
        salvar_dados(self.dados)
        QMessageBox.information(self, "Data de Reset Atualizada", f"A nova data de reset foi definida para {nova_data}")

    # Função para limpar os campos de entrada de horário
    def limpar_campos(self):
        self.entrada_manha.clear()
        self.saida_manha.clear()
        self.entrada_tarde.clear()
        self.saida_tarde.clear()

        # Habilitar todos os campos ao iniciar um novo dia
        self.entrada_manha.setDisabled(False)
        self.saida_manha.setDisabled(False)
        self.entrada_tarde.setDisabled(False)
        self.saida_tarde.setDisabled(False)

    # Sobrescreve o método closeEvent para salvar os horários atuais ao fechar a aplicação
    def closeEvent(self, event):
        # Atualiza os horários atuais no JSON
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        horarios = {
            'entrada_manha': self.entrada_manha.text(),
            'saida_manha': self.saida_manha.text(),
            'entrada_tarde': self.entrada_tarde.text(),
            'saida_tarde': self.saida_tarde.text()
        }
        registro_existente = None
        for registro in self.dados['registros']:
            if registro['data'] == data_hoje:
                registro_existente = registro
                break

        if registro_existente:
            registro_existente.update(horarios)
        else:
            registro_existente = {
                'data': data_hoje,
                'entrada_manha': horarios['entrada_manha'],
                'saida_manha': horarios['saida_manha'],
                'entrada_tarde': horarios['entrada_tarde'],
                'saida_tarde': horarios['saida_tarde'],
                'horas_trabalhadas': ''
            }
            self.dados['registros'].append(registro_existente)

        salvar_dados(self.dados)
        event.accept()

# Execução do aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PontoApp()
    window.show()
    sys.exit(app.exec_())
