# Importo il modulo sqlite3, già incluso in Python,
# che serve per lavorare con i database SQLite
import sqlite3

# Apro il collegamento al file del database.
# Se "preparatore.db" non esiste, viene creato.
# Salvo il collegamento nella variabile conn ("connection")
conn = sqlite3.connect("preparatore.db")

# Creo il cursore: è lo strumento che esegue i comandi SQL.
# conn = il quaderno aperto, cur = la penna
cur = conn.cursor()

# Creo la tabella "argomenti", solo se non esiste già.
# Ha due colonne:
#   id   -> numero intero, chiave primaria: unico per ogni riga,
#           SQLite lo assegna da solo (1, 2, 3...)
#   nome -> testo, obbligatorio (NOT NULL = non può essere vuoto)
cur.execute("CREATE TABLE IF NOT EXISTS argomenti (id INTEGER PRIMARY KEY, nome TEXT NOT NULL)")

# Inserisco due righe nella tabella, riempiendo solo la colonna "nome".
# L'id non lo scrivo: lo mette SQLite.
# Il testo dentro SQL va tra apici singoli ' '
# perché le virgolette doppie " " delimitano già la stringa Python
cur.execute("INSERT INTO argomenti (nome) VALUES ('SQL')")
cur.execute("INSERT INTO argomenti (nome) VALUES ('Java OOP')")

# Salvo davvero le modifiche nel file del database.
# Senza commit, le righe inserite andrebbero perse alla chiusura
conn.commit()

# Chiedo al database tutte le righe della tabella, colonne id e nome
cur.execute("SELECT id, nome FROM argomenti")

# Prendo tutti i risultati della SELECT.
# fetchall() restituisce una lista; ogni riga è una tupla, es. (1, 'SQL')
righe = cur.fetchall()

# Ciclo for: per ogni riga nella lista "righe", la stampo.
# Lo spazio prima di print (indentazione) indica che è DENTRO il ciclo
for riga in righe:
    print(riga)

# Chiudo il collegamento al database: ho finito
conn.close()