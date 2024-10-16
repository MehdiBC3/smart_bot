import streamlit as st
# import os
from mistralai import Mistral



# Définition de l'API key et du modèle que l'on veut utiliser
api_key = st.secrets["Mistral"]["mistral_api_key"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

# Définition de la fonction qui génère la réponse du modèle
def generate_response(user_input):
    """
    Fonction qui envoie l'entrée utilisateur au modèle de langage Mistral et retourne la réponse du modèle.
    """
    chat_response = client.chat.complete(
        model = model,
        messages = [    
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    # Retourner le contenu de la première réponse du modèle
    return chat_response.choices[0].message.content

# Configuration de l'interface utilisateur avec Streamlit
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions !")

# Initialisation de l'historique de conversation si elle n'existe pas encore dans la session
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Création du formulaire pour soumettre une question à l'IA
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Vous :", key="input")
    submit_button = st.form_submit_button(label='Envoyer')


# Si le bouton est cliqué et qu'il y a une entrée utilisateur
if submit_button and user_input:
    # Génération de la réponse à partir de l'entrée utilisateur
    response = generate_response(user_input)
    # Ajouter l'entrée utilisateur et la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Affichage de l'historique des messages dans la conversation
for sender, message in st.session_state.chat_history:
    if sender == "Vous":
        st.write(f"{sender}: {message}")
    else:
        st.write(f"{sender}: {message}")
