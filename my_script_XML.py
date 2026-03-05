import sys
import urllib.request
import xml.etree.ElementTree as ET

def search_ncbi_history(db, query):
    #Faz pesquisa no NCBI, guarda o XML em 'history.xml' e retorna WebEnv e QueryKey.
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + \
          urllib.parse.urlencode({"db": db, "term": query, "usehistory": "y"})
    
    xml_data = urllib.request.urlopen(url).read()
    
    # Guarda o ficheiro XML 
    with open("history.xml", "wb") as f:
        f.write(xml_data)
        
    root = ET.fromstring(xml_data)
    
    return root.find("WebEnv").text, root.find("QueryKey").text

def fetch_fasta(db, webenv, query_key):
    #Download as sequências em FASTA e imprime no ecrã (STDOUT).
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + \
          urllib.parse.urlencode({"db": db, "WebEnv": webenv, "query_key": query_key, "rettype": "fasta", "retmode": "text"})
    
    fasta_data = urllib.request.urlopen(url).read().decode("utf-8")
    print(fasta_data, end="")

if __name__ == "__main__":
    # Lê os argumentos da linha de comandos
    db = sys.argv[1]
    query = sys.argv[2]
    
    # Executa a pesquisa (e guarda o XML) e depois descarrega o FASTA
    webenv, query_key = search_ncbi_history(db, query)
    fetch_fasta(db, webenv, query_key)