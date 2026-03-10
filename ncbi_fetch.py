import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json

def search_ncbi_history(db, query, format_choice):
    # Adiciona os parâmetros base
    params = {"db": db, "term": query, "usehistory": "y"}
    
    # Se o utilizador escolheu JSON, avisa o NCBI
    if format_choice == "json":
        params["retmode"] = "json"
        
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)
    response_data = urllib.request.urlopen(url).read()
    
    # Guarda o ficheiro e extrai as chaves dependendo da escolha
    if format_choice == "json":
        with open("history.json", "wb") as f:
            f.write(response_data)
        data = json.loads(response_data.decode("utf-8"))
        return data["esearchresult"]["webenv"], data["esearchresult"]["querykey"]
    else:
        with open("history.xml", "wb") as f:
            f.write(response_data)
        root = ET.fromstring(response_data)
        return root.find("WebEnv").text, root.find("QueryKey").text

def fetch_fasta(db, webenv, query_key):
    # Descarrega as sequências em FASTA e imprime no ecrã (STDOUT)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + \
          urllib.parse.urlencode({"db": db, "WebEnv": webenv, "query_key": query_key, "rettype": "fasta", "retmode": "text"})
    
    fasta_data = urllib.request.urlopen(url).read().decode("utf-8")
    print(fasta_data, end="")

if __name__ == "__main__":
    db = sys.argv[1]
    query = sys.argv[2]
    
    # Lê o 3º argumento (se existir), senão usa "xml" por defeito
    format_choice = sys.argv[3].lower() if len(sys.argv) > 3 else "xml"
    
    # Executa a pesquisa e depois descarrega o FASTA
    webenv, query_key = search_ncbi_history(db, query, format_choice)
    fetch_fasta(db, webenv, query_key)