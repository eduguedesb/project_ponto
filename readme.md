Este script é uma aplicação gráfica de controle de registro de ponto, desenvolvida usando PyQt5 para a interface gráfica e ReportLab para geração de relatórios em PDF. O programa permite registrar horários de entrada e saída (manhã e tarde), calcular automaticamente o tempo de trabalho diário e o banco de horas, além de gerar relatórios de registro de ponto em formato PDF.

Registro de ponto diário: O usuário pode inserir e salvar horários de entrada e saída para manhã e tarde.
Cálculo de horas trabalhadas: O script calcula o total de horas trabalhadas no dia, comparando com a carga horária esperada (8h30min), e ajusta o banco de horas de acordo.
Banco de horas: Atualiza o banco de horas com base nas horas trabalhadas a mais ou a menos que a carga horária.
Reset automático de banco de horas: O banco de horas pode ser resetado em uma data definida pelo usuário.
Geração de relatórios em PDF: O programa permite gerar relatórios em PDF, contendo os registros de ponto e o banco de horas acumulado.
Armazenamento de dados: Todos os registros são armazenados em um arquivo JSON para que as informações sejam persistidas entre as execuções.

Dependências:
PyQt5: Usada para criar a interface gráfica.
ReportLab: Utilizada para gerar o relatório em PDF.
Mutagen: Utilizada para manipular o arquivo JSON de registros.
JSON: Utilizado para armazenar dados de ponto e banco de horas.

Como usar:
Insira os horários de entrada e saída no formato HH:MM para manhã e tarde.
Clique no botão Registrar Ponto para salvar os horários e atualizar o banco de horas.
Para resetar o banco de horas, selecione uma data usando o campo de calendário.
O botão Relatório em PDF gera um relatório de todos os registros de ponto em um arquivo PDF.

Observações:
O programa verifica automaticamente o banco de horas e reseta na data definida, se aplicável.
Todos os registros e o banco de horas são salvos em um arquivo JSON (registro_ponto.json).
Para fechar o programa, os horários inseridos são salvos automaticamente.
