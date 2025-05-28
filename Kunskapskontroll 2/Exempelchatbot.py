# =======================================
# Exempel på chatbot med Gemini
# =======================================
#
# Detta är ett testexempel för att verifiera om chattbotten fungerar korrekt
# och om API-nyckeln är korrekt laddad.
# 
# Syftet med koden är att:
# - Verifiera att chattbotten kan generera svar från Google Gemini
# - Testa om API-nyckeln är korrekt inställd via .env-filen
#
# Denna version är ett enkelt exempel för att testa om kommunikationen
# med Gemini fungerar och om chatbotten kan svara på frågor från användaren.
#
# Användaren kan skriva en fråga eller skriva "<q>" för att avsluta chatten.


import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Huvudfunktion för chatt
def main():
    print("*** Exampel chattbot med Gemini ***")
    print("Skriv en fråga eller <q> för att avsluta.")

    while True:
        user_input = input("Du: ")
        if user_input.lower() == "q":
            break

        try:
            response = genai.generate_content(
                model="gemini-1.5-flash",  
                contents=user_input
            )
            print("Gemini:", response.text)
        except Exception as e:
            print("Fel vid generering:", e)

if __name__ == "__main__":
    main()



