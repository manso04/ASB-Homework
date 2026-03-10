# NCBI Sequence Fetcher

## Program usage

```
python3 ncbi_fetch.py «arg1» «arg2» «arg3»
```

`arg3` is optional and can be either `xml` or `json`.
If no format is provided, the default is `xml`.

---

## Description

This project provides a small non-interactive command-line tool that retrieves biological sequences from the NCBI Entrez API.

The program performs a search query in an NCBI database using the Entrez `ESearch` utility with the `usehistory` option enabled. This allows the program to store the results on the Entrez History server and retrieve them later using `WebEnv` and `QueryKey`.

After the search step, the script uses the `EFetch` utility to download the corresponding sequences in **FASTA format**.

The script allows the user to choose whether the `ESearch` response is retrieved and parsed in **XML** or **JSON** format.

The resulting FASTA sequences are written directly to **STDOUT**, allowing the output to be redirected to a file if desired.

---

## Requirements

* Python 3.x
* No external libraries required (only Python standard library is used)

---

## Arguments

* `arg1` – Target NCBI database (e.g., `nucleotide`, `protein`, `gene`)
* `arg2` – Entrez search query string
* `arg3` *(optional)* – Format used to retrieve and parse the ESearch response (`xml` or `json`). Default is `xml`.

---

## Output

The program writes the retrieved sequences in **FASTA format** to standard output (`STDOUT`).

This allows the output to be redirected to a file:

```
python3 ncbi_fetch.py nucleotide "query" xml > sequences.fasta
```

or

```
python3 ncbi_fetch.py nucleotide "query" json > sequences.fasta
```

If the format argument is omitted, XML is used by default:

```
python3 ncbi_fetch.py nucleotide "query" > sequences.fasta
```

---

## Example

Retrieve sequences for the Cytochrome b gene from the western lowland gorilla and save them to a file:

```
python3 ncbi_fetch.py nucleotide "Gorilla gorilla gorilla[organism] AND cytb[gene]" json > gorilla_cytb.fasta
```

---

## Program structure

The script is organized into independent functions.

### `search_ncbi_history(db, query, format_choice)`

Performs a search request to the NCBI Entrez API using `ESearch`.

Responsibilities:

* Sends the search query to NCBI
* Enables the Entrez history feature (`usehistory=y`)
* Retrieves the response in XML or JSON depending on the user choice
* Saves the response locally (`history.xml` or `history.json`)
* Extracts and returns:

  * `WebEnv`
  * `QueryKey`

These identifiers are required to retrieve the results from the Entrez history server.

---

### `fetch_fasta(db, webenv, query_key)`

Retrieves sequences using the `EFetch` utility.

Responsibilities:

* Uses the `WebEnv` and `QueryKey` obtained from the previous step
* Requests sequence data in FASTA format
* Prints the result to STDOUT

---

### `main`

Handles command-line arguments and orchestrates the workflow:

1. Reads `arg1` (database) and `arg2` (query)
2. Reads the optional `arg3` (response format: `xml` or `json`)
3. Calls `search_ncbi_history`
4. Calls `fetch_fasta`

---

## Files generated

Depending on the format selected:

* `history.json` – stored search results in JSON format
* `history.xml` – stored search results in XML format

These files contain the response from the NCBI `ESearch` request and are saved in the current working directory.

---

## Entrez API

This script uses the **NCBI Entrez Programming Utilities (E-utilities)**.

Relevant endpoints:

* `ESearch` – perform database searches
* `EFetch` – retrieve full records

Documentation:
https://www.ncbi.nlm.nih.gov/books/NBK25501/

---

## Repository

This project is delivered through a public Git repository.

---

## License

This project is licensed under the **MIT License**.
See the `LICENSE` file for full details.

---

## Group members

* Afonso Manso (202300125)
* Diogo Mota (202300409)
* Filipa Sousa (2024106384)

