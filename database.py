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

# Accendo il controllo delle chiavi esterne.
# SQLite per default NON le controlla: senza questa riga
# potrei inserire una domanda con un argomento che non esiste.
# Va ripetuto ogni volta che apro un collegamento
cur.execute("PRAGMA foreign_keys = ON")

# Creo la tabella "argomenti", solo se non esiste già.
# Ha due colonne:
#   id   -> numero intero, chiave primaria: unico per ogni riga,
#           SQLite lo assegna da solo (1, 2, 3...)
#   nome -> testo, obbligatorio (NOT NULL = non può essere vuoto)
#           e UNIQUE (non possono esserci due argomenti uguali)
cur.execute("CREATE TABLE IF NOT EXISTS argomenti (id INTEGER PRIMARY KEY, nome TEXT NOT NULL UNIQUE)")

# Creo la tabella "domande", solo se non esiste già.
# Le tre virgolette """ permettono di scrivere il comando su più righe.
# Colonne:
#   id                -> chiave primaria, assegnata da SQLite
#   argomento_id      -> l'id dell'argomento a cui appartiene la domanda
#   testo             -> la domanda, obbligatoria e UNIQUE (niente domande doppie)
#   risposta_corretta -> obbligatoria ma NON unica: due domande diverse
#                        possono avere la stessa risposta
# FOREIGN KEY: argomento_id deve corrispondere a un id che esiste
# nella tabella argomenti (integrità referenziale)
cur.execute("""
    CREATE TABLE IF NOT EXISTS domande (
        id INTEGER PRIMARY KEY,
        argomento_id INTEGER NOT NULL,
        testo TEXT NOT NULL UNIQUE,
        risposta_corretta TEXT NOT NULL,
        FOREIGN KEY (argomento_id) REFERENCES argomenti(id)
    )
""")

# Inserisco due argomenti, riempiendo solo la colonna "nome".
# L'id non lo scrivo: lo mette SQLite (SQL = 1, Java OOP = 2).
# OR IGNORE: se l'argomento esiste già, lo salta senza errore.
# Il testo dentro SQL va tra apici singoli ' '
# perché le virgolette doppie " " delimitano già la stringa Python
cur.execute("INSERT OR IGNORE INTO argomenti (nome) VALUES ('SQL')")
cur.execute("INSERT OR IGNORE INTO argomenti (nome) VALUES ('Java OOP')")

# Inserisco tre domande. Per ognuna scrivo l'argomento (con il suo id),
# il testo e la risposta corretta.
# Il comando SQL può andare a capo, ma ogni testo tra apici
# va scritto su una riga sola, altrimenti gli a capo finiscono nel database.
# OR IGNORE: se la domanda esiste già (stesso testo), la salta.
# Attenzione: OR IGNORE scarta in silenzio, senza segnalare nulla
cur.execute("""
    INSERT OR IGNORE INTO domande (argomento_id, testo, risposta_corretta)
    VALUES (1, 'cosa fa una inner join?',
    'una INNER JOIN restituisce le righe che hanno una corrispondenza in entrambe le tabelle'
    )
""")
cur.execute("""
    INSERT OR IGNORE INTO domande (argomento_id, testo, risposta_corretta)
    VALUES (1, 'left join?',
    'prende tutte le righe della tabella di sinistra, anche quelle senza corrispondenza, e mette NULL dove a destra manca il dato'
    )
""")
cur.execute("""
    INSERT OR IGNORE INTO domande (argomento_id, testo, risposta_corretta)
    VALUES (2, 'hashmap?',
    'una struttura dati di Java che salva coppie chiave-valore: ogni chiave è unica e permette di ritrovare velocemente il suo valore'
    )
""")

# Salvo davvero le modifiche nel file del database.
# Senza commit, le righe inserite andrebbero perse alla chiusura
conn.commit()

# Leggo tutte le domande insieme al nome del loro argomento.
# JOIN unisce le due tabelle: a ogni domanda aggancia la riga di
# argomenti il cui id è uguale ad argomento_id.
# domande.testo = colonna testo della tabella domande
# argomenti.nome = colonna nome della tabella argomenti
cur.execute("""
    SELECT domande.testo, argomenti.nome
    FROM domande
    JOIN argomenti ON domande.argomento_id = argomenti.id
""")

# Prendo tutti i risultati della SELECT.
# fetchall() restituisce una lista; ogni riga è una tupla,
# es. ('cosa fa una inner join?', 'SQL')
righe = cur.fetchall()

# Ciclo for: per ogni riga nella lista "righe", la stampo.
# Lo spazio prima di print (indentazione) indica che è DENTRO il ciclo
for riga in righe:
    print(riga)

# Chiudo il collegamento al database: ho finito
conn.close()