# Visão Geral:
Este script é uma aplicação gráfica de controle de registro de ponto, desenvolvida usando PyQt5 para a interface gráfica e ReportLab para geração de relatórios em PDF. O programa permite registrar horários de entrada e saída (manhã e tarde), calcular automaticamente o tempo de trabalho diário e o banco de horas, além de gerar relatórios de registro de ponto em formato PDF.

# Funcionamento:
Registro de ponto diário: O usuário pode inserir e salvar horários de entrada e saída para manhã e tarde.
<br>
Cálculo de horas trabalhadas: O script calcula o total de horas trabalhadas no dia, comparando com a carga horária esperada (8h30min), e ajusta o banco de horas de acordo.
<br>
Banco de horas: Atualiza o banco de horas com base nas horas trabalhadas a mais ou a menos que a carga horária.
<br>
Reset automático de banco de horas: O banco de horas pode ser resetado em uma data definida pelo usuário.
<br>
Geração de relatórios em PDF: O programa permite gerar relatórios em PDF, contendo os registros de ponto e o banco de horas acumulado.
<br>
Armazenamento de dados: Todos os registros são armazenados em um arquivo JSON para que as informações sejam persistidas entre as execuções.

# Dependências:
PyQt5: Usada para criar a interface gráfica.
<br>
ReportLab: Usada para gerar o relatório em PDF.

# Como Usar:
Execute o script com o seguinte comando: py ponto.py ou python ponto.py.
