# PDF-and-CBX-file-quality-comparator

Este projeto visa criar uma aplicação em Python que compare arquivos .pdf, .cbr e .cbz e determine parâmetros entre eles (resolução, tamanho do arquivo e número de páginas). 
Ele agrupa arquivos que tenha nomes com n carateres iguais no início do nome do arquivo. Ele permite acrescentar tags como "(T)" (tamanho), "(R)" (resolução) e "(P)" (número de páginas) para os arquivos que sejam maiores nesses parâmetros.
Cria um relatório detalhado com as propriedades dos arquivos e comparações feitas.
Permite que sejam usadas mais de uma pasta para comparar a qualidade dos arquivos.

Com isso é possível ter uma ferramenta que compare arquivos de scan de publicações e determine mais facilmente quais deles possuem melhor qualidade.

Para utilizar será necessário uma versão recente do Python instalada (3.0 ou maior)
Execute no terminal com:

``python file_comparator.py``
