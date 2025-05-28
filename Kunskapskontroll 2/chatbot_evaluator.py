# ======================================
# Evaluator: Bedöm AI-svar med Gemini eller egen chatbot
# ======================================
# Denna utvärdering hjälper till att mäta chatbotens förmåga att korrekt hämta och sammanställa
# information från en extern källa (examensarbete) på ett interaktivt sätt. 
# Genom att jämföra genererade svar med ideal-svar, kan vi se hur väl chatbotten förstår och
# relaterar till det specifika innehållet i dokumentet. 
# Detta ger oss möjlighet att objektivt bedöma chatbotens prestanda och identifiera 
# områden för förbättring, vilket är avgörande för att skapa effektiva och pålitliga AI-drivna 
# verktyg för informationshämtning och användarinteraktion.


import os
from dotenv import load_dotenv
import google.generativeai as genai
import pickle
from pdf_rag_chatbot import generate_answer

# Ladda API-nyckel och konfigurera Gemini
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Exempelfrågor och ideal-svar (valideringsdata)
validation_data = [
    {
        "question": "Vad handlar examensarbetet om?",
        "ideal_answer": "Examensarbetet handlar om att avgöra om utdatan från en algoritm är ett heltal eller inte. Ett exempel på en sådan algoritm är en hiss som åker till olika våningsplan. Arbetet undersöker även samhälliga och etiska aspekter av algoritmer och deras betydelse i olika sammanhang, såsom självkörande bilar, optimering av poliskontroller och sökresultat. En viktig aspekt är också kontrollen av korrektheten av resultaten och resursanvändning vid körning av algoritmer."
    },
    {
        "question": "Vilken metod användes?",
        "ideal_answer": "En metod som användes var att lagra en lång lista med slumptal i spelets minne. En annan, bättre metod var att använda en algoritm som använder sin utdatan som indata."
    },
    {
        "question": "Vad är slutsatsen i arbetet?",
        "ideal_answer": "Det vet jag inte. Texten beskriver arbetets innehåll och struktur, men presenterar inte någon slutsats."
    }
]

# System-prompt för utvärdering med betyg 0-10
evaluation_system_prompt = """
Du är ett intelligent utvärderingssystem vars uppgift är att utvärdera en AI-assistents svar på en fråga.

- Om svaret är perfekt, relevant och komplett: sätt poängen 10.
- Om svaret är bra men har små brister: 7–9.
- Om det är delvis rätt eller otydligt: 4–6.
- Om det är dåligt, felaktigt eller svårbegripligt: 1–3.
- Om det är helt fel eller inte besvarar frågan: 0.

Motivera betyget i 1–2 meningar.
"""

# === AI-genererat svar från min chattbot ===
def generate_response(question):
    return generate_answer(question)

# === EVALUATOR: Jämför svaret med ideal och sätt betyg ===
def evaluate_response(generated, ideal, question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    evaluation_prompt = f"""
Fråga: {question}
AI-assistentens svar: {generated}
Önskat svar: {ideal}
"""
    response = model.generate_content(
        contents=evaluation_system_prompt + evaluation_prompt
    )
    return response.text

# === Kör testfall och summera betyg ===
total_score = 0
score_count = 0
results = []

for data in validation_data:
    print("====================")
    print("Fråga:", data["question"])
    generated = generate_response(data["question"])
    print("Svar från AI:", generated)
    print("---")
    print("Utvärdering:")
    result = evaluate_response(generated, data["ideal_answer"], data["question"])
    print(result)
    results.append({"fråga": data["question"], "svar": generated, "utvärdering": result})

    for line in result.split("\n"):
        if "Poäng" in line:
            try:
                score = float(line.split(":")[1].strip())
                total_score += score
                score_count += 1
            except:
                pass
    print("====================\n")

if score_count > 0:
    average = round(total_score / score_count, 2)
    print(f"\nGenomsnittligt betyg för chatbotten: {average} av 10")
else:
    print("\nInga giltiga poång kunde tolkas.")

# === Spara resultat till fil ===
with open("evaluation_results.pkl", "wb") as f:
    pickle.dump(results, f)
print("\nResultat sparade i evaluation_results.pkl")