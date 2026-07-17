import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

# Creiamo l'applicazione server
app = FastAPI()

# Impostiamo la chiave API 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6KLRjuCkD9v8uuJVVlHxvLPxyL1OU18FBlwv1R2WisdjQ")
client = genai.Client(api_key=GEMINI_API_KEY)

# Struttura del messaggio in arrivo
class RichiestaUtente(BaseModel):
    messaggio: str

# Punto di accesso per i tuoi PC
@app.post("/parla-con-agente")
async def rispondi_al_messaggio(richiesta: RichiestaUtente):
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=richiesta.messaggio,
            config=types.GenerateContentConfig(
                system_instruction="Sei l'Agente IA principale di un software gestionale e contabile. Il tuo scopo è aiutare l'utente con fatturazione, calcoli IVA, bilanci, normative fiscali e gestione aziendale. Rispondi in modo rigoroso, professionale e analitico. Rifiutati cortesemente di rispondere a domande non pertinenti all'ambito economico o contabile.",
                temperature=0.7
            )
        )
        return {"risposta_agente": response.text}
        
    except Exception as e:
        return {"errore": f"Si è verificato un problema con Gemini: {str(e)}"}
