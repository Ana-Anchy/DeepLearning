
# ==========================================
# PDF RAG-Chatbot med Gemini Kunskapskontroll2
# ==========================================
#
# Denna chatbot är skapad som en del av min kunskapskontroll2. Chatbotten använder
# RAG-teknik (Retrieval-Augmented Generation) för att svara på frågor baserat på
# innehållet i ett PDF-dokument, i detta fall ett examensarbete från:
# **Charmlers tekniska högskola, Göteborgs universitet**
# Examensarbetets namn: **"Hur vet vi att ett datorprogram gör vad det säger
# att det gör?Formell verifiering av hypergeometriska rekursionsrelationer
# med polynomkoefficienter"**
#
# Syftet med denna chatbot är att ge användare möjlighet att snabbt få svar
# på frågor om ett specifikt ämne, i detta fall ett examensarbete. Detta gör 
# det till ett kraftfullt verktyg för att förstå och bearbeta komplexa texter
# på ett effektivt sätt. Användaren kan ställa frågor om exempelvis 
# arbetets metod, resultat och slutsatser, och chatbotten kommer att generera svar 
# baserat på relevant text från PDF-dokumentet.
#
# **Tillämpningar i verkligheten**:
# - Chatbotten kan användas inom utbildning, där studenter kan interagera med
#   akademiska artiklar och examensarbeten för att snabbt förstå relevanta 
#   delar av ett arbete, såsom metod och resultat.
# - Den kan även användas inom forskning för att analysera stora mängder textdata
#   och extrahera specifik information utan att behöva läsa igenom hela dokumenten.
#
# Chatbotten använder Google Gemini för att hämta och generera svar utifrån 
# semantisk sökning i PDF-filen, vilket gör att svaren alltid är kontextuellt relevanta 
# för den aktuella frågan.
#
# Exempel på frågor som kan ställas till chatbotten:
# - Vad handlar examensarbetet om?
# - Vad är syftet med arbetet?
# - Vilken metod användes?
# - Vad är slutsatsen i arbetet?

# ==========================================
# Fördjupad och Kritisk Diskussion
# ==========================================
# **Affärsmässiga möjligheter**:
# - För företag och organisationer kan denna typ av chatbot användas för att 
#   effektivt bearbeta stora mängder data och ge svar på kundfrågor eller 
#   interna analyser.
# - Chatbotten kan användas för att bygga intelligenta assistenter som kan 
#   kommunicera med kunder om tekniska eller komplexa produkter.
#
# **Etiska perspektiv och potentiella utmaningar**:
# - En utmaning kan vara att chatbotten inte alltid ger korrekta eller tillräckliga
#   svar om den inte har tillgång till rätt data eller om den är tränad på otillräcklig
#   information.
# - Det finns också etiska frågor kring **datasäkerhet** och **integritet**, eftersom
#   chatbotten kan ha tillgång till känslig information beroende på dess tillämpning.
# - Det kan även finnas en risk för att chatbotten missförstår användarens frågor om
#   den inte är tillräckligt tränad på relevanta domäner eller är beroende av externa
#   källor som kan vara osäkra.
#
# **Framtida möjligheter**:
# - Förbättringar kan göras genom att träna modellen på fler domäner för att utöka
#   dess användningsområden och förbättra svarens kvalitet.


#TERMINAL COMMAND PROMPT CMD

import os
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
import pickle
from pypdf import PdfReader

# Ladda API-nyckel från .env
# === STEG 1: Ladda miljövariabler och konfigurera Gemini ===
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# === STEG 2: Extrahera text från PDF ===
pdf_path = "examensarbete.pdf"
reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

# === STEG 3: Dela upp text i chunks ===
chunk_size = 1000
overlap = 200
chunks = []

for i in range(0, len(full_text), chunk_size - overlap):
    chunk = full_text[i:i + chunk_size]
    chunks.append(chunk)

# Spara chunks till fil
with open("pdf_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

# === STEG 4: Skapa eller ladda embeddings ===
if os.path.exists("pdf_embeddings.pkl"):
    print("Laddar embeddings från cache...")
    with open("pdf_embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)
else:
    print("Skapar embeddings... detta tar lite tid...")
    embeddings = []
    for chunk in chunks:
        try:
            emb = genai.embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="RETRIEVAL_QUERY"
            )
            embeddings.append(emb["embedding"])
        except Exception as e:
            print("Fel vid embedding:", e)
            embeddings.append([0.0] * 768)

    with open("pdf_embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

# === STEG 5: Semantisk sökning ===
def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def semantic_search(query, chunks, embeddings, k=5):
    query_emb = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="RETRIEVAL_QUERY"
    )["embedding"]

    likhet = [(i, cosine_similarity(query_emb, emb)) for i, emb in enumerate(embeddings)]
    likhet.sort(key=lambda x: x[1], reverse=True)
    top_chunks = [chunks[i] for i, _ in likhet[:k]]
    return top_chunks

# === STEG 6: Generera svar ===
def generate_answer(query):
    context = semantic_search(query, chunks, embeddings)
    prompt = f"Besvara frågan nedan baserat enbart på kontexten. Om det inte finns information, säg 'Det vet jag inte'.\n\nKONEXT:\n{''.join(context)}\n\nFRÅGA: {query}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# === STEG 7: Terminalbaserad chatt ===
def main():
    print("*** PDF RAG-CHATTBOT ***")
    print("Ställ en fråga om innehållet i PDF:en (skriv <q> för att avsluta)")

    while True:
        query = input("Du: ")
        if query.lower() == "q":
            break
        svar = generate_answer(query)
        print("Gemini:", svar)

if __name__ == "__main__":
    main()