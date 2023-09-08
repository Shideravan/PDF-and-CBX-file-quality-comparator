import os
import zipfile
import rarfile
import time
from PIL import Image
from pypdf import PdfReader

def generate_report(dir1='.', dir2=None):
    report = []
    
    dir1 = input("Digite o nome do primeiro diretório: ")
    dir2 = input("Digite o nome do segundo diretório (ou deixe em branco para usar apenas o primeiro): ")
    max_attempts = 3 # Número máximo de tentativas para renomear cada arquivo
    retry_delay = 10 # Tempo em segundos para esperar antes de tentar novamente

    print ('\n\n\tVerificando: ' + dir1 + ' e ' + dir2 +'\n\n')
    
    for dir in [dir1, dir2]:
        if not dir:
            continue
        for file in os.listdir(dir):
            file_pathh = os.path.join(dir, file)
            
            if file.endswith('.cbr') or file.endswith('.cbz'):
                archive = None
                if file.endswith('.cbr'):
                    archive = rarfile.RarFile(file_pathh)
                else:
                    archive = zipfile.ZipFile(file_pathh)
                first_image = archive.namelist()[0]
                with archive.open(first_image) as f:
                    image = Image.open(f)
                    width, height = image.size
                size = os.path.getsize(file_pathh) / (1024 * 1024)
                num_pages = len(archive.namelist())
                report.append({
                    'file_name': file,
                    'dir': dir,
                    'resolution': f'{width} x {height}',
                    'size': f'{size:.2f} MB',
                    'num_pages': num_pages
                })
                
            if file.endswith('.pdf'):
                with open(file_pathh, 'rb') as f:
                    pdf = PdfReader(f)
                    num_pages = len(pdf.pages)
                    page = pdf.pages[0]
                    width = int(round(page.mediabox.width))
                    height = int(round(page.mediabox.height))
                    size = os.path.getsize(file_pathh) / (1024 * 1024)
                    report.append({
                        'file_name': file,
                        'dir': dir,
                        'resolution': f'{width} x {height}',
                        'size': f'{size:.2f} MB',
                        'num_pages': num_pages
                    })            
                    
    report.sort(key=lambda x: x['file_name'])
    groups = {}
    
    for entry in report:
        group_key = entry['file_name'][:33]
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(entry)
        
    with open('relatorio.txt', 'w') as f:
        for group_key, group_entries in groups.items():
            if len(group_entries) > 1:
            
                f.write(f"---------------------------------------------\n")
                f.write(f"Grupo: {group_key}\n")
                f.write(f"---------------------------------------------\n\n")
                
                max_size = max(float(x['size'].split()[0]) for x in group_entries)
                max_size_entries = [x for x in group_entries if float(x['size'].split()[0]) == max_size]
                
                max_res = max(int(x['resolution'].split()[0]) * int(x['resolution'].split()[2]) for x in group_entries)
                max_res_entries = [x for x in group_entries if int(x['resolution'].split()[0]) * int(x['resolution'].split()[2]) == max_res]

                
                max_pages = max(int(x['num_pages']) for x in group_entries)
                max_pages_entries = [x for x in group_entries if int(x['num_pages']) == max_pages]
                
                for entry in group_entries:
                    folder_path = entry['dir']
                    filename = entry['file_name']
                    file_path = os.path.join(folder_path, filename)
                    
                    new_tag = ""

                    if entry in max_size_entries:
                        f.write("[TAMANHO] ")  
                        new_tag += " (T)"            
                        
                                    
                    if entry in max_res_entries:
                        f.write("[RESOLUÇÃO] ")
                        new_tag += " (R)" 
                                    
                    if entry in max_pages_entries:
                        f.write("[PÁGINAS] ")
                        new_tag += " (P)" 

                                    
                    if new_tag == "":                  
                        f.write("[nada] ")
                        new_tag = " (nada)"
                        
                    if os.path.isfile(file_path):
                        name, extension = os.path.splitext(filename)
                        new_name = name + new_tag + extension
                        new_file_path = os.path.join(folder_path, new_name)
                                
                        attempts = 0
                        while attempts < max_attempts:
                            try:
                                os.rename(file_path, new_file_path)
                                break
                            except PermissionError:
                                attempts += 1
                                print (f"Tentativa {attempts} de renomear {entry['file_name']}")
                                time.sleep(retry_delay)
                                if attempts == max_attempts:
                                    print(f'Não foi possível renomear {file_path} após {max_attempts} tentativas.')
                                    f.write(f"Não renomeou\n")
                                    
                    f.write(f"\n\t{filename}\n")
                    f.write(f"\tLocal: {folder_path}\n")
                    f.write(f"\t{entry['resolution']}\n")
                    f.write(f"\t{entry['size']}\n")
                    f.write(f"\t{entry['num_pages']} páginas\n\n")
                    print(f"Processou: {entry['file_name']}\n")                     

        
                f.write("\n")
            else:
                entry = group_entries[0]
                f.write(f"---------------------------------------------\n")
                f.write(f"Arquivo simples\n")
                f.write(f"---------------------------------------------\n")
                f.write(f"\n\t{entry['file_name']}\n")
                f.write(f"\tLocal: {entry['dir']}\n")
                f.write(f"\t{entry['resolution']}\n")
                f.write(f"\t{entry['size']}\n")
                f.write(f"\t{entry['num_pages']} páginas\n")
                folder_path = entry['dir']
                filename = entry['file_name']
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    
                    name, extension = os.path.splitext(filename)
                    new_name = name + ' (único)' + extension
                    new_file_path = os.path.join(folder_path, new_name)
                    
                    attempts = 0
                    while attempts < max_attempts:
                        try:
                            os.rename(file_path, new_file_path)
                            break
                        except PermissionError:
                            attempts += 1
                            print (f"Tentativa {attempts} de renomear {entry['file_name']}")
                            time.sleep(retry_delay)
                    if attempts == max_attempts:
                        print(f'Não foi possível renomear {file_path} após {max_attempts} tentativas.')
                        f.write(f"\nNão renomeou este arquivo único\n")
                        
                    print(f"Processou: {entry['file_name']}\n")           
                f.write(f"\n\n")
generate_report('.', '..')
