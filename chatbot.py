# chatbot_app.py
import streamlit as st
from googletrans import Translator

# -----------------
# Disease Knowledge Base (expandable)
# -----------------
knowledge_base = {
    "dengue": {
        "about": "Dengue is a viral infection transmitted by Aedes mosquitoes.",
        "symptoms": "High fever, severe headache, pain behind eyes, joint pain, rash.",
        "prevention": "Use mosquito nets, wear long clothes, avoid stagnant water.",
        "treatment": "No specific cure. Rest, fluids, and medical supervision are recommended."
    },
    "malaria": {
        "about": "Malaria is caused by Plasmodium parasites spread through Anopheles mosquitoes.",
        "symptoms": "Fever, chills, sweats, headaches, nausea, vomiting.",
        "prevention": "Use insect repellent, mosquito nets, and eliminate stagnant water.",
        "treatment": "Antimalarial medicines prescribed by doctors are effective."
    },
    "covid": {
        "about": "COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus.",
        "symptoms": "Fever, cough, fatigue, loss of taste or smell, breathing difficulties.",
        "prevention": "Wear masks, wash hands, maintain social distancing, get vaccinated.",
        "treatment": "Supportive care, rest, hydration, and prescribed antiviral or oxygen therapy for severe cases."
    },
    "typhoid": {
        "about": "Typhoid is a bacterial infection caused by Salmonella Typhi, spread through contaminated food and water.",
        "symptoms": "Prolonged fever, weakness, stomach pain, headache, constipation or diarrhea.",
        "prevention": "Drink clean water, maintain good sanitation, wash hands, and avoid street food.",
        "treatment": "Antibiotics prescribed by doctors are the main treatment."
    }
}

# -----------------
# Chatbot Logic (improved NLP matching)
# -----------------
def get_response(user_input):
    user_input = user_input.lower()

    for disease, info in knowledge_base.items():
        if disease in user_input:
            if any(word in user_input for word in ["symptom", "symptoms"]):
                return info["symptoms"]
            elif any(word in user_input for word in ["prevent", "prevention", "avoid"]):
                return info["prevention"]
            elif any(word in user_input for word in ["treat", "treatment", "cure", "medicine"]):
                return info["treatment"]
            elif any(word in user_input for word in ["about", "what", "info", "information"]):
                return info["about"]
            else:
                return f"I can tell you about {disease}: symptoms, prevention, or treatment."
    
    return "Sorry, I don’t have information on that. Please try asking about Dengue, Malaria, COVID-19, or Typhoid."

# -----------------
# Multilingual Support
# -----------------
translator = Translator()

def chatbot_reply(user_input, lang="en"):
    response = get_response(user_input)
    if lang != "en":
        try:
            response = translator.translate(response, dest=lang).text
        except Exception:
            response = f"(Translation failed) {response}"
    return response

# -----------------
# Streamlit UI
# -----------------
st.title("🩺 AI-Driven Health Chatbot")
st.write("Ask me about Dengue, Malaria, COVID-19, or Typhoid (symptoms, prevention, treatment).")

# Language selection
lang = st.selectbox(
    "Choose Language",
    ["en", "hi", "ta"],
    format_func=lambda x: {"en": "English", "hi": "Hindi", "ta": "Tamil"}[x]
)

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", "")

if st.button("Ask"):
    if not user_input.strip():
        st.warning("⚠ Please enter a question.")
    else:
        reply = chatbot_reply(user_input, lang)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Chatbot", reply))

# Display chat history
for sender, msg in st.session_state.history:
    if sender == "You":
        st.write(f"🧑 *{sender}:* {msg}")
    else:
        st.success(f"🤖 *{sender}:* {msg}")
