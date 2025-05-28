# ==========================================
# Script för att skriva ut och spara resultat
# ==========================================
# Detta script används för att läsa in resultaten från chatbotens utvärdering
# som sparats i `evaluation_results.pkl`. Resultaten innehåller både de ställda
# frågorna, chatbotens genererade svar och utvärderingarna av dessa svar.
#
# Scriptet gör två saker:
# 1. Skriver ut utvärderingen i terminalen så att användaren kan se:
#    - Fråga
#    - Svar från chatbot
#    - Utvärdering av svaret
#
# 2. Sparar utvärderingen i ett **Markdown-format** i filen `evaluation_results.md`,
#    vilket gör att användaren kan skapa en rapport eller vidare analysera resultaten.
#
# Detta script är ett hjälpmedel för att analysera chatbotens prestation och få en
# objektiv bedömning av dess svar på ställda frågor, baserat på de önskade svaren.


import pickle

# Läs in resultaten från filen
with open("evaluation_results.pkl", "rb") as f:
    results = pickle.load(f)

# Skriv ut resultaten i terminalen
print("\n*** Utvärdering av Chatbot ***\n")
for result in results:
    print(f"Fråga: {result['fråga']}")
    print(f"Svar från AI: {result['svar']}")
    print(f"Utvärdering:\n{result['utvärdering']}")
    print("=" * 50)

# Spara till Markdown-format
with open("evaluation_results.md", "w", encoding="utf-8") as f:
    f.write("# *** Utvärdering av Chatbot ***\n\n")
    for result in results:
        f.write(f"### Fråga: {result['fråga']}\n")
        f.write(f"**Svar från AI**: {result['svar']}\n")
        f.write(f"**Utvärdering**:\n{result['utvärdering']}\n")
        f.write("=" * 50 + "\n\n")

print("\nResultaten har sparats till evaluation_results.md")
