import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json
import uuid
import unicodedata
import base64
import xml.etree.ElementTree as ET

# Recherche et chargement du chemin du logo
def find_logo_path():
    for filename in ["Merlin Logo.png", "Merlin Logo.webp", "Merlin Logo.jpg"]:
        if os.path.exists(filename):
            return filename
    return ""

LOGO_PATH = find_logo_path()

# Configuration de la page (avec le logo dans l'onglet du navigateur)
st.set_page_config(
    page_title="Merlin - Gestion des Saisines RH",
    page_icon=LOGO_PATH if LOGO_PATH else "🧙‍♂️",
    layout="wide"
)

# Chargement automatique et conversion du logo en base64 (projet_merlin sur le bureau)
def find_logo_path():
    for filename in ["Merlin Logo.png", "Merlin Logo.webp", "Merlin Logo.jpg"]:
        if os.path.exists(filename):
            return filename
    return ""

LOGO_PATH = find_logo_path()

def get_image_base64(image_path):
    if image_path and os.path.exists(image_path):
        ext = image_path.split(".")[-1]
        if ext == "jpg":
            ext = "jpeg"
        with open(image_path, "rb") as img_file:
            return f"data:image/{ext};base64," + base64.b64encode(img_file.read()).decode('utf-8')
    return ""

logo_b64 = get_image_base64(LOGO_PATH)

# CHARTE GRAPHIQUE ET CORRECTIONS STYLES CSS
st.markdown("""
    <style>
    /* Masquer la barre blanche Streamlit en haut */
    header, #MainMenu, footer {
        visibility: hidden !important;
        height: 0px !important;
    }
    .stAppHeader {
        display: none !important;
    }

    /* Fond principal sombre aux nuances bleu nuit */
    .stApp {
        background-color: #0E131F;
        color: #FFFFFF !important;
    }
    
    /* Textes globaux en blanc */
    p, label, span, div, .stMarkdown, h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Texte noir dans les cases de saisie (y compris champs de date) */
    input, textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* Champ date affiché (date_input) : texte noir sur tout le composant */
    div[data-testid="stDateInput"] *,
    div[data-baseweb="input"] *,
    div[data-baseweb="base-input"] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }

    /* Menus déroulants fermés (Select / Multiselect) */
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    div[data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    /* Listes déroulantes ouvertes + calendriers : fond blanc */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"],
    div[data-baseweb="calendar"],
    div[data-baseweb="datepicker"] {
        background-color: #FFFFFF !important;
    }

    /* Listes déroulantes ouvertes + calendriers : TOUT le texte en noir */
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] *,
    ul[role="listbox"] *,
    div[role="listbox"] *,
    [role="option"],
    [role="option"] *,
    div[data-baseweb="calendar"] *,
    div[data-baseweb="datepicker"] *,
    [role="gridcell"] *,
    [data-testid="stSelectboxVirtualDropdown"] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    div[data-baseweb="popover"] svg,
    div[data-baseweb="calendar"] svg {
        fill: #000000 !important;
    }

    /* Barre latérale (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #161C2E;
        border-right: 1px solid #2A344D;
    }
    
    /* TOUS les boutons : bleu cyan / cyan néon magique */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button,
    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button,
    div[data-testid="stFormSubmitButton"] button,
    button[data-testid^="stBaseButton"],
    form button {
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%) !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 0 12px rgba(0, 198, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button *,
    .stDownloadButton > button *,
    .stFormSubmitButton > button *,
    button[data-testid^="stBaseButton"] * {
        color: #FFFFFF !important;
    }
    
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover,
    button[data-testid^="stBaseButton"]:hover,
    form button:hover {
        background: linear-gradient(135deg, #00E5FF 0%, #0099FF 100%) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.8) !important;
        transform: translateY(-1px) !important;
    }

    /* Corbeille de suppression : juste l'emoji */
    div[class*="st-key-suppr_"] div[data-testid="stButton"] button,
    div[class*="st-key-suppr_"] div[data-testid="stButton"] button:hover,
    div[class*="st-key-suppr_"] div[data-testid="stButton"] button:focus {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        min-height: 0 !important;
        transform: none !important;
        font-size: 1.3rem !important;
    }
    div[class*="st-key-suppr_"] div[data-testid="stButton"] button:hover {
        filter: drop-shadow(0 0 6px rgba(0, 229, 255, 0.9));
    }

    /* Cartes et containers Expanders */
    .streamlit-expanderHeader {
        background-color: #1A2238 !important;
        border-radius: 6px;
        color: #64FFDA !important;
    }
    
    /* Encart d'informations */
    .stAlert {
        background-color: #1E293B;
        border-left: 4px solid #00E5FF;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fichiers de stockage locaux
DATA_FILE = "merlin_saisines.csv"
TEXTES_FILE = "merlin_textes.json"
THEMES_FILE = "merlin_themes.json"
USERS_FILE = "merlin_users.json"
COLLECTIVITES_FILE = "merlin_collectivites.json"
COMMUNES_FILE = "merlin_communes.json"

def amorcer_collectivites():
    deja = []
    if os.path.exists(COLLECTIVITES_FILE):
        with open(COLLECTIVITES_FILE, "r", encoding="utf-8") as f:
            deja = json.load(f)
    if deja:
        return
    communes = []
    if os.path.exists(COMMUNES_FILE):
        with open(COMMUNES_FILE, "r", encoding="utf-8") as f:
            communes = json.load(f)
    with open(COLLECTIVITES_FILE, "w", encoding="utf-8") as f:
        json.dump([{"idc": nom, "agents": []} for nom in communes], f, ensure_ascii=False, indent=4)

def init_data():
    if not os.path.exists(DATA_FILE):
        df_empty = pd.DataFrame(columns=[
            "ID_Fiche", "IDC", "IDAP", "IDAN", "DAS", "OBQ", "QUE", 
            "IDAG", "Mode_Reponse", "REP", "Date_Cloture", "Commentaires", 
            "Themes", "Statut", "Createur"
        ])
        df_empty.to_csv(DATA_FILE, index=False)
    
    if not os.path.exists(THEMES_FILE):
        with open(THEMES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    if not os.path.exists(TEXTES_FILE):
        with open(TEXTES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    if not os.path.exists(USERS_FILE):
        users_defaut = {
            "mduval": {"nom": "Mélanie Duval", "pwd": "mduval000"},
            "vadam": {"nom": "Valentine Adam", "pwd": "vadam000"},
            "nfatoux": {"nom": "Nathan Fatoux", "pwd": "nafatoux000"},
            "pdouliez": {"nom": "Perrine Douliez", "pwd": "pdouliez000"}
        }
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_defaut, f, ensure_ascii=False, indent=4)

    amorcer_collectivites()

def sauver_collectivites(db):
    with open(COLLECTIVITES_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def charger_collectivites():
    with open(COLLECTIVITES_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
    modifie = False
    for c in db:
        c.setdefault("agents", [])
        for a in c["agents"]:
            if not a.get("id"):
                a["id"] = uuid.uuid4().hex[:8]
                modifie = True
    if modifie:
        sauver_collectivites(db)
    return db

def creer_collectivite():
    nom = st.session_state.get("nom_nouvelle_collectivite", "").strip()
    if not nom:
        st.session_state["err_collectivite"] = "Le nom de la collectivité ne peut pas être vide."
        return
    db = charger_collectivites()
    if any(c["idc"].lower() == nom.lower() for c in db):
        st.session_state["err_collectivite"] = "Une collectivité porte déjà ce nom."
        return
    db.append({"idc": nom, "agents": []})
    sauver_collectivites(db)
    st.session_state["coll_choix"] = nom
    st.session_state["msg_collectivite"] = f"Collectivité « {nom} » créée avec succès."

def renommer_collectivite(ancien, cle_input):
    nouveau = st.session_state.get(cle_input, "").strip()
    if not nouveau:
        st.session_state["err_collectivite"] = "Le nom de la collectivité ne peut pas être vide."
        return
    if nouveau == ancien:
        return
    db = charger_collectivites()
    if any(c["idc"].lower() == nouveau.lower() and c["idc"] != ancien for c in db):
        st.session_state["err_collectivite"] = "Une collectivité porte déjà ce nom."
        return
    for c in db:
        if c["idc"] == ancien:
            c["idc"] = nouveau
    sauver_collectivites(db)
    df_s = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    masque = df_s["IDC"].str.lower() == ancien.lower()
    nb = int(masque.sum())
    if nb:
        df_s.loc[masque, "IDC"] = nouveau
        df_s.to_csv(DATA_FILE, index=False)
    st.session_state["coll_choix"] = nouveau
    st.session_state["msg_collectivite"] = f"Collectivité renommée en « {nouveau} »" + (f" ({nb} saisine(s) mise(s) à jour)." if nb else ".")

def cle_tri(nom):
    return unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode().lower()

def nettoyer_utilisateurs():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    propres = {
        k: v for k, v in users.items()
        if "dupont" not in k.lower() and "dupont" not in str(v.get("nom", "")).lower()
    }
    if len(propres) != len(users):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(propres, f, ensure_ascii=False, indent=4)

init_data()
nettoyer_utilisateurs()

def trier_textes(textes):
    def cle(item):
        i, t = item
        niveau = t.get("hierarchie", 99)
        try:
            ordinal = date.fromisoformat(t["date"]).toordinal() if t.get("date") else None
        except ValueError:
            ordinal = None
        if ordinal is not None:
            return (niveau, 0, -ordinal)
        return (niveau, 1, -i)
    return sorted(enumerate(textes), key=cle)

# Authentification
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_username = ""
    st.session_state.user_nom = ""

def check_login(username, password):
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    if username in users and users[username]["pwd"] == password:
        return True, users[username]["nom"]
    return False, ""

# --- PAGE D'IDENTIFICATION ---
if not st.session_state.logged_in:
    if logo_b64:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                <img src="{logo_b64}" width="65" style="border-radius: 8px;">
                <h1 style="margin: 0;">Connexion à Merlin</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Connexion à Merlin")
        
    st.markdown("Veuillez vous identifier pour accéder à l'application.")
    
    with st.form("login_form"):
        username_input = st.text_input("Identifiant")
        password_input = st.text_input("Mot de passe", type="password")
        submit_login = st.form_submit_button("Se connecter")
        
        if submit_login:
            success, nom_complet = check_login(username_input, password_input)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_username = username_input
                st.session_state.user_nom = nom_complet
                st.success(f"Bienvenue {nom_complet} !")
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
    st.stop()

# --- APPLICATION PRINCIPALE ---
gestionnaire_nom = st.session_state.user_nom

# Logo à GAUCHE de Merlin dans l'encart de la barre latérale (sidebar)
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <img src="{logo_b64}" width="40" style="border-radius: 6px;">
            <h2 style="margin: 0; color: #00E5FF; font-size: 1.5rem;">Merlin</h2>
        </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.title("Merlin")

st.sidebar.write(f"Connecté : **{gestionnaire_nom}**")

menu = st.sidebar.radio("Navigation", [
    "1. Saisine",
    "2. Recherche",
    "3. Descripteurs et Textes applicables",
    "4. Fiche collectivité",
    "5. Extraction",
    "6. Mon Compte"
])

# Logo à GAUCHE de Merlin sur les pages principales
if logo_b64:
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
            <img src="{logo_b64}" width="65" style="border-radius: 8px;">
            <h1 style="margin: 0;">Merlin</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("Merlin")

# --- MODULE 1 : SUIVI DES SAISINES ---
if menu == "1. Saisine":
    st.header("Saisine")

    df = pd.read_csv(DATA_FILE, dtype=str).fillna("")

    with open(COLLECTIVITES_FILE, "r", encoding="utf-8") as f:
        collabs_db = json.load(f)

    col_gauche, col_droite = st.columns([1.5, 1])

    with col_gauche:
        st.subheader("Création / Modification d'une Saisine")
        action_fiche = st.radio("Action :", ["Créer une nouvelle saisine", "Modifier / Clôturer une saisine existante"])

        if action_fiche == "Créer une nouvelle saisine":
            if "fiche_courante_id" not in st.session_state:
                st.session_state.fiche_courante_id = None
            if "fiche_is_cloturee" not in st.session_state:
                st.session_state.fiche_is_cloturee = False

            col_reset1, col_reset2 = st.columns(2)
            with col_reset1:
                if st.button("Réinitialiser le formulaire pour une nouvelle saisine"):
                    st.session_state.fiche_courante_id = None
                    st.session_state.fiche_is_cloturee = False
                    st.rerun()
            with col_reset2:
                if st.button("Nouvelle saisine"):
                    st.session_state.fiche_courante_id = None
                    st.session_state.fiche_is_cloturee = False
                    st.session_state.clear()
                    st.session_state.logged_in = True
                    st.session_state.user_username = st.session_state.get("user_username", "")
                    st.session_state.user_nom = gestionnaire_nom
                    st.rerun()

            is_locked = st.session_state.fiche_is_cloturee

            st.markdown("#### A. Identité de la saisine")
            idc_noms = [c["idc"] for c in collabs_db]
            
            recherche_idc_input = st.text_input("Rechercher / Saisir le nom de la collectivité (IDC) *", disabled=is_locked)
            
            selected_idc = ""
            if recherche_idc_input:
                trouvees = [c for c in idc_noms if recherche_idc_input.lower() in c.lower()]
                if trouvees:
                    selected_idc = st.selectbox("Collectivités trouvées :", trouvees, disabled=is_locked)
                else:
                    selected_idc = recherche_idc_input.strip()

            agents_disponibles = []
            if selected_idc:
                for c in collabs_db:
                    if c["idc"].lower() == selected_idc.lower():
                        agents_disponibles = c.get("agents", [])

            st.markdown("#### B. Identité de l'agent")
            
            def_prenom, def_nom, def_poste, def_mail = "", "", "", ""
            if agents_disponibles:
                options_agents = ["-- Nouvel agent ou Saisie libre --"] + [f"{a['prenom']} {a['nom']}" for a in agents_disponibles]
                agent_nom_complet_selected = st.selectbox("Sélectionner un agent pré-enregistré (Autocomplétion) :", options_agents, disabled=is_locked)
                
                if agent_nom_complet_selected != "-- Nouvel agent ou Saisie libre --":
                    for a in agents_disponibles:
                        if f"{a['prenom']} {a['nom']}" == agent_nom_complet_selected:
                            def_prenom = a.get("prenom", "")
                            def_nom = a.get("nom", "")
                            def_poste = a.get("poste", "")
                            def_mail = a.get("mail", "")

            col_a1, col_a2 = st.columns(2)
            with col_a1:
                form_idap = st.text_input("Prénom de l'agent (IDAP)", value=def_prenom, disabled=is_locked)
            with col_a2:
                form_idan = st.text_input("Nom de l'agent (IDAN)", value=def_nom, disabled=is_locked)

            col_a3, col_a4 = st.columns(2)
            with col_a3:
                form_poste = st.text_input("N° de poste", value=def_poste, disabled=is_locked)
            with col_a4:
                form_mail = st.text_input("Adresse mail", value=def_mail, disabled=is_locked)

            st.markdown("#### C. Date et heure de la saisine")
            form_das = st.date_input("Date de la saisine (DAS)", value=datetime.today(), format="DD/MM/YYYY", disabled=is_locked)
            form_heure = datetime.now().strftime("%H:%M")
            st.text(f"Heure automatique : {form_heure}")

            st.markdown("#### D. Objet & Question")
            form_obq = st.text_input("Objet de la saisine (OBQ) *", disabled=is_locked)
            form_que = st.text_area("Question détaillée (QUE) *", disabled=is_locked)

            st.markdown("#### E. Réponse & Gestion")
            st.text(f"Identité du gestionnaire (IDAG) : {gestionnaire_nom}")
            form_b = st.selectbox("Choix de la réponse (Modalité) *", ["B1. Réponse immédiate", "B2. Rappel", "B3. Réponse écrite"], disabled=is_locked)
            form_rep = st.text_area("Réponse apportée (REP)", disabled=is_locked)

            st.markdown("#### Descripteurs & Textes applicables")
            with open(THEMES_FILE, "r", encoding="utf-8") as f:
                themes_dispo = json.load(f)
            
            selected_themes = st.multiselect("Sélectionnez les thèmes pertinents", themes_dispo, disabled=is_locked)

            if selected_themes:
                st.markdown("##### Textes applicables correspondants :")
                with open(TEXTES_FILE, "r", encoding="utf-8") as tf:
                    textes_db = json.load(tf)
                textes_filtres = [t for _, t in trier_textes(textes_db) if t["theme"] in selected_themes]
                if textes_filtres:
                    for t in textes_filtres:
                        pastille_texte = "🔴 Abrogé" if t["abroge"] else "🟢 En vigueur"
                        titre_affiche = f"{t['titre']} — {pastille_texte}"
                        
                        if t.get("url"):
                            with st.expander(f"{t['titre']} — {pastille_texte}"):
                                st.markdown(f"Lien officiel : [{t['url']}]({t['url']})", unsafe_allow_html=True)
                                if t["modificatifs"]:
                                    st.write("Textes modificatifs :")
                                    for mod in t["modificatifs"]:
                                        st.markdown(f"- {mod}")
                        else:
                            with st.expander(titre_affiche):
                                if t["modificatifs"]:
                                    st.write("Textes modificatifs :")
                                    for mod in t["modificatifs"]:
                                        st.markdown(f"- {mod}")
                else:
                    st.info("Aucun texte spécifique associé.")

            st.markdown("#### F. Commentaire")
            form_comm = st.text_area("Commentaire")

            st.markdown("---")
            form_statut = st.selectbox("Statut de la demande", ["En cours", "Traité", "Relancé", "En attente réponse collectivité"], disabled=is_locked)

            if not is_locked:
                if st.session_state.fiche_courante_id is None:
                    if st.button("Créer la saisine"):
                        if not selected_idc or not form_obq or not form_que:
                            st.error("Champs obligatoires manquants (Collectivité, Objet, Question).")
                        else:
                            collec_trouvee = False
                            for c in collabs_db:
                                if c["idc"].lower() == selected_idc.lower():
                                    collec_trouvee = True
                                    if form_idap and form_idan:
                                        agent_existe = any(a["prenom"].lower() == form_idap.lower() and a["nom"].lower() == form_idan.lower() for a in c["agents"])
                                        if not agent_existe:
                                            c["agents"].append({"prenom": form_idap, "nom": form_idan, "poste": form_poste, "mail": form_mail})
                            if not collec_trouvee:
                                nouveaux_agents = [{"prenom": form_idap, "nom": form_idan, "poste": form_poste, "mail": form_mail}] if (form_idap or form_idan) else []
                                collabs_db.append({"idc": selected_idc, "agents": nouveaux_agents})
                            
                            with open(COLLECTIVITES_FILE, "w", encoding="utf-8") as f:
                                json.dump(collabs_db, f, ensure_ascii=False, indent=4)

                            annee_str = str(form_das.year)
                            type_lettre = "T" if "téléphone" in form_b.lower() or "immédiate" in form_b.lower() or "rappel" in form_b.lower() else "E"
                            df_ex = pd.read_csv(DATA_FILE, dtype=str)
                            nb_annee = len(df_ex[df_ex["ID_Fiche"].str.startswith(annee_str, na=False)]) + 1
                            id_fiche = f"{annee_str}-{type_lettre}-{nb_annee:05d}"

                            date_heure_str = f"{form_das.strftime('%d/%m/%Y')} {form_heure}"
                            date_cloture = date_heure_str if form_statut == "Traité" else ""

                            new_row = {
                                "ID_Fiche": id_fiche,
                                "IDC": selected_idc,
                                "IDAP": form_idap,
                                "IDAN": form_idan,
                                "DAS": date_heure_str,
                                "OBQ": form_obq,
                                "QUE": form_que,
                                "IDAG": gestionnaire_nom,
                                "Mode_Reponse": form_b,
                                "REP": form_rep,
                                "Date_Cloture": date_cloture,
                                "Commentaires": f"[{datetime.now().strftime('%d/%m/%Y %H:%M')} - {gestionnaire_nom}] {form_comm}" if form_comm else "",
                                "Themes": ", ".join(selected_themes),
                                "Statut": form_statut,
                                "Createur": gestionnaire_nom
                            }

                            df_new = pd.concat([df_ex, pd.DataFrame([new_row])], ignore_index=True)
                            df_new.to_csv(DATA_FILE, index=False)
                            st.session_state.fiche_courante_id = id_fiche
                            st.success(f"Fiche créée sous le numéro : {id_fiche}")
                            st.rerun()

                else:
                    st.info(f"Fiche active : **{st.session_state.fiche_courante_id}**")
                    col_b1, col_b2 = st.columns(2)
                    
                    with col_b1:
                        if st.button("Modifier la saisine"):
                            df_mod = pd.read_csv(DATA_FILE, dtype=str).fillna("")
                            idx = df_mod[df_mod["ID_Fiche"] == st.session_state.fiche_courante_id].index[0]
                            df_mod.loc[idx, "IDC"] = selected_idc
                            df_mod.loc[idx, "OBQ"] = form_obq
                            df_mod.loc[idx, "QUE"] = form_que
                            df_mod.loc[idx, "REP"] = form_rep
                            df_mod.loc[idx, "Statut"] = form_statut
                            if form_comm:
                                ancien = df_mod.loc[idx, "Commentaires"]
                                df_mod.loc[idx, "Commentaires"] = ancien + f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M')} - {gestionnaire_nom}] {form_comm}"
                            df_mod.to_csv(DATA_FILE, index=False)
                            st.success("Modifications enregistrées.")
                            st.rerun()

                    with col_b2:
                        if st.button("Clôturer la saisine"):
                            if not form_rep or form_rep.strip() == "":
                                st.error("Réponse manquante : Impossible de clôturer la saisine sans avoir renseigné une réponse (REP).")
                            elif not selected_idc or not form_obq or not form_que:
                                st.error("Informations nécessaires manquantes (Collectivité, Objet ou Question).")
                            else:
                                df_mod = pd.read_csv(DATA_FILE, dtype=str).fillna("")
                                idx = df_mod[df_mod["ID_Fiche"] == st.session_state.fiche_courante_id].index[0]
                                df_mod.loc[idx, "REP"] = form_rep
                                df_mod.loc[idx, "Statut"] = "Traité"
                                df_mod.loc[idx, "Date_Cloture"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                                df_mod.to_csv(DATA_FILE, index=False)
                                st.session_state.fiche_is_cloturee = True
                                st.success("Saisine clôturée définitivement.")
                                st.rerun()

            else:
                st.warning("Cette fiche est désormais clôturée et verrouillée.")
                if form_comm and st.button("Enregistrer le commentaire uniquement"):
                    df_mod = pd.read_csv(DATA_FILE, dtype=str).fillna("")
                    idx = df_mod[df_mod["ID_Fiche"] == st.session_state.fiche_courante_id].index[0]
                    ancien = df_mod.loc[idx, "Commentaires"]
                    df_mod.loc[idx, "Commentaires"] = ancien + f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M')} - {gestionnaire_nom}] {form_comm}"
                    df_mod.to_csv(DATA_FILE, index=False)
                    st.success("Commentaire ajouté.")
                    st.rerun()

        else:
            df_mod = pd.read_csv(DATA_FILE, dtype=str).fillna("")
            if df_mod.empty:
                st.info("Aucune saisine en base.")
            else:
                fiches_ids = df_mod["ID_Fiche"].tolist()
                choix_fiche = st.selectbox("Sélectionner la fiche par son numéro unique", fiches_ids)
                fiche_ligne = df_mod[df_mod["ID_Fiche"] == choix_fiche].iloc[0]
                is_clot = (fiche_ligne["Statut"] == "Traité")

                ed_idc = st.text_input("Collectivité (IDC)", value=fiche_ligne["IDC"], disabled=is_clot)
                ed_obq = st.text_input("Objet (OBQ)", value=fiche_ligne["OBQ"], disabled=is_clot)
                ed_que = st.text_area("Question (QUE)", value=fiche_ligne["QUE"], disabled=is_clot)
                ed_rep = st.text_area("Réponse apportée (REP)", value=fiche_ligne["REP"], disabled=is_clot)
                nouveau_comm = st.text_area("Ajouter un commentaire")
                
                st.markdown("---")
                ed_statut = st.selectbox("Statut", ["En cours", "Traité", "Relancé", "En attente réponse collectivité"], index=["En cours", "Traité", "Relancé", "En attente réponse collectivité"].index(fiche_ligne["Statut"]) if fiche_ligne["Statut"] in ["En cours", "Traité", "Relancé", "En attente réponse collectivité"] else 0, disabled=is_clot)

                if not is_clot:
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("Modifier la saisine"):
                            idx = df_mod[df_mod["ID_Fiche"] == choix_fiche].index[0]
                            df_mod.loc[idx, "IDC"] = ed_idc
                            df_mod.loc[idx, "OBQ"] = ed_obq
                            df_mod.loc[idx, "QUE"] = ed_que
                            df_mod.loc[idx, "REP"] = ed_rep
                            df_mod.loc[idx, "Statut"] = ed_statut
                            if nouveau_comm:
                                df_mod.loc[idx, "Commentaires"] = fiche_ligne["Commentaires"] + f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M')} - {gestionnaire_nom}] {nouveau_comm}"
                            df_mod.to_csv(DATA_FILE, index=False)
                            st.success("Mise à jour effectuée.")
                            st.rerun()

                    with col_btn2:
                        if st.button("Clôturer la saisine"):
                            if not ed_rep or ed_rep.strip() == "":
                                st.error("Réponse manquante : Impossible de clôturer la saisine sans réponse (REP).")
                            elif not ed_idc or not ed_obq or not ed_que:
                                st.error("Informations nécessaires manquantes.")
                            else:
                                idx = df_mod[df_mod["ID_Fiche"] == choix_fiche].index[0]
                                df_mod.loc[idx, "REP"] = ed_rep
                                df_mod.loc[idx, "Statut"] = "Traité"
                                df_mod.loc[idx, "Date_Cloture"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                                df_mod.to_csv(DATA_FILE, index=False)
                                st.success("Fiche clôturée.")
                                st.rerun()
                else:
                    st.warning("Cette fiche est clôturée et verrouillée.")
                    if nouveau_comm and st.button("Enregistrer le commentaire"):
                        idx = df_mod[df_mod["ID_Fiche"] == choix_fiche].index[0]
                        df_mod.loc[idx, "Commentaires"] = fiche_ligne["Commentaires"] + f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M')} - {gestionnaire_nom}] {nouveau_comm}"
                        df_mod.to_csv(DATA_FILE, index=False)
                        st.success("Commentaire enregistré.")
                        st.rerun()

    with col_droite:
        st.subheader("Dernières saisines")
        collec_actuelle = selected_idc if 'selected_idc' in locals() and selected_idc else ""
        
        if collec_actuelle:
            st.write(f"Affichage pour : **{collec_actuelle}**")
            df_col = df[df["IDC"].str.lower() == collec_actuelle.lower()]
            if not df_col.empty:
                df_col = df_col.sort_values(by="ID_Fiche", ascending=False)
                for idx, row in df_col.iterrows():
                    statut = row["Statut"]
                    pastille = "🟢" if statut == "Traité" else ("🟠" if statut == "En cours" else ("🔴" if statut == "Relancé" else "🟣"))
                    
                    titre_expand = f"{pastille} [{row['ID_Fiche']}] Objet : {row['OBQ']}"
                    with st.expander(titre_expand):
                        st.write(f"**Date de saisine :** {row['DAS']}")
                        st.write(f"**Date de réponse :** {row['Date_Cloture'] if row['Date_Cloture'] else row['DAS'] + ' (En attente)'}")
                        st.write(f"**Gestionnaire ayant répondu :** {row['IDAG'] if row['IDAG'] else 'Non renseigné'}")
                        st.write(f"**Agent :** {row['IDAP']} {row['IDAN']}")
                        st.write(f"**Question :** {row['QUE']}")
                        st.write(f"**Réponse :** {row['REP'] if row['REP'] else 'Pas encore de réponse'}")
                        if row["Commentaires"]:
                            st.info(f"**Commentaires :**\n{row['Commentaires']}")
            else:
                st.info(f"Aucune saisine pour '{collec_actuelle}'.")
        else:
            st.info("Renseignez le champ IDC à gauche pour afficher les dernières saisines de la collectivité.")

# --- MODULE 2 : RECHERCHE ---
elif menu == "2. Recherche":
    st.header("Recherche")
    st.caption(
        "Sans guillemets : Recherche multicritère tous les mots.\n"
        "Avec guillemets : Recherche d'expression exacte.\n"
        "Majuscules et accents sont ignorés."
    )

    with st.form(key="advanced_search_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            f_idr = st.text_input("Référence question (IDR)")
            f_csr = st.text_input("Conseiller (IDAG)")
        with col2:
            f_obq = st.text_input("Objet (OBQ)")
            f_que = st.text_input("Question (QUE)")
        with col3:
            f_rep = st.text_input("Réponse (REP)")
            f_his = st.text_input("Collectivité (HIS)")

        f_all = st.text_input("Recherche libre (dans tous les champs ci-dessus)")

        st.markdown("---")
        f_activer_date_precise = st.checkbox("Activer la date précise")
        col_dp1, _ = st.columns(2)
        with col_dp1:
            f_date_precise = st.date_input("Date précise (DQU)", value=None, format="DD/MM/YYYY")

        st.markdown("---")
        f_activer_periode = st.checkbox("Activer la restriction par période")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            f_date_debut = st.date_input("Date de début", value=None, format="DD/MM/YYYY")
        with col_d2:
            f_date_fin = st.date_input("Date de fin", value=None, format="DD/MM/YYYY")

        submitted = st.form_submit_button(label="Exécuter la requête")

        if submitted:
            st.session_state["search_executed"] = True
            st.session_state["f_idr"] = f_idr
            st.session_state["f_csr"] = f_csr
            st.session_state["f_obq"] = f_obq
            st.session_state["f_que"] = f_que
            st.session_state["f_rep"] = f_rep
            st.session_state["f_his"] = f_his
            st.session_state["f_all"] = f_all
            st.session_state["f_activer_date_precise"] = f_activer_date_precise
            st.session_state["f_date_precise"] = f_date_precise
            st.session_state["f_activer_periode"] = f_activer_periode
            st.session_state["f_date_debut"] = f_date_debut
            st.session_state["f_date_fin"] = f_date_fin

    if st.session_state.get("search_executed", False):
        df_search = pd.read_csv(DATA_FILE, dtype=str).fillna("")

        if df_search.empty:
            st.info("Aucune saisine enregistrée.")
        else:
            res = df_search.copy()
            f_idr_val = st.session_state.get("f_idr", "").lower()
            f_csr_val = st.session_state.get("f_csr", "").lower()
            f_obq_val = st.session_state.get("f_obq", "").lower()
            f_que_val = st.session_state.get("f_que", "").lower()
            f_rep_val = st.session_state.get("f_rep", "").lower()
            f_his_val = st.session_state.get("f_his", "").lower()
            f_all_val = st.session_state.get("f_all", "").lower()

            if f_idr_val:
                res = res[res["ID_Fiche"].str.lower().str.contains(f_idr_val, na=False)]
            if f_csr_val:
                res = res[res["IDAG"].str.lower().str.contains(f_csr_val, na=False)]
            if f_obq_val:
                res = res[res["OBQ"].str.lower().str.contains(f_obq_val, na=False)]
            if f_que_val:
                res = res[res["QUE"].str.lower().str.contains(f_que_val, na=False)]
            if f_rep_val:
                res = res[res["REP"].str.lower().str.contains(f_rep_val, na=False)]
            if f_his_val:
                res = res[res.apply(lambda r: f_his_val in (r["IDC"] + " " + r["Commentaires"]).lower(), axis=1)]

            if f_all_val:
                res = res[res.apply(lambda r: f_all_val in (r["ID_Fiche"] + " " + r["IDC"] + " " + r["IDAG"] + " " + r["OBQ"] + " " + r["QUE"] + " " + r["REP"]).lower(), axis=1)]

            st.markdown(f"### Résultats validés : {len(res)} fiches correspondantes")

            if len(res) > 0:
                repartition = res["IDAG"].value_counts()
                st.caption("Répartition par conseiller : " + " · ".join(f"{k} ({v})" for k, v in repartition.items()))

            st.markdown("---")

            for _, row in res.iterrows():
                statut = row["Statut"]
                pastille = "🟢" if statut == "Traité" else ("🟠" if statut == "En cours" else ("🔴" if statut == "Relancé" else "🟣"))
                
                with st.expander(f"{pastille} Fiche : {row['ID_Fiche']} | Collectivité : {row['IDC']} | Conseiller : {row['IDAG']} | Date : {row['DAS']} | Objet : {row['OBQ']}"):
                    st.write(f"**Date de saisine :** {row['DAS']}")
                    st.write(f"**Date de réponse :** {row['Date_Cloture'] if row['Date_Cloture'] else 'En attente'}")
                    st.write(f"**Objet (OBQ) :** {row['OBQ']}")
                    st.write(f"**Question (QUE) :** {row['QUE']}")
                    st.write(f"**Réponse (REP) :** {row['REP']}")
                    if row['Commentaires']:
                        st.info(f"**Commentaires :**\n{row['Commentaires']}")
    else:
        st.info("Renseigne tes critères de recherche ci-dessus et clique sur **Exécuter la requête**.")

# --- MODULE 3 : DESCRIPTEURS ET TEXTES APPLICABLES ---
elif menu == "3. Descripteurs et Textes applicables":
    st.header("Descripteurs et Textes applicables")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Thèmes / Descripteurs")
        with open(THEMES_FILE, "r", encoding="utf-8") as f:
            themes_actuels = json.load(f)
        nouveau_theme = st.text_input("Nouveau thème")
        if st.button("Ajouter le thème"):
            if nouveau_theme and nouveau_theme not in themes_actuels:
                themes_actuels.append(nouveau_theme)
                with open(THEMES_FILE, "w", encoding="utf-8") as f:
                    json.dump(themes_actuels, f, ensure_ascii=False, indent=4)
                st.success("Thème ajouté.")
                st.rerun()
        for th in themes_actuels:
            st.markdown(f"- {th}")

    with col_t2:
        st.subheader("Textes Applicables")
        with open(TEXTES_FILE, "r", encoding="utf-8") as tf:
            textes_actuels = json.load(tf)
        with open(THEMES_FILE, "r", encoding="utf-8") as f:
            th_list = json.load(f)

        nouveau_titre = st.text_input("Intitulé du texte")
        nouveau_url = st.text_input("URL du texte (lien vers la version en vigueur)")
        nouveau_theme_assoc = st.selectbox("Thème associé", th_list) if th_list else st.text_input("Thème associé")
        niveau_h = st.number_input("Niveau hiérarchie", min_value=1, max_value=10, value=2)
        date_texte = st.date_input("Date du texte (pour tri du plus récent au plus ancien)", value=date.today(), format="DD/MM/YYYY")
        abro = st.checkbox("Abrogé ?")
        modifs = st.text_input("Textes modificatifs (séparés par virgule)")

        if st.button("Ajouter le texte"):
            if nouveau_titre:
                modifs_list = [m.strip() for m in modifs.split(",")] if modifs else []
                textes_actuels.append({
                    "titre": nouveau_titre, 
                    "url": nouveau_url,
                    "hierarchie": int(niveau_h),
                    "date": date_texte.isoformat(),
                    "theme": nouveau_theme_assoc, 
                    "abroge": abro, 
                    "modificatifs": modifs_list
                })
                with open(TEXTES_FILE, "w", encoding="utf-8") as tf:
                    json.dump(textes_actuels, tf, ensure_ascii=False, indent=4)
                st.success("Texte ajouté.")
                st.rerun()

        for idx, t in trier_textes(textes_actuels):
            stat = "🔴 Abrogé" if t["abroge"] else "🟢 En vigueur"
            url_display = f" - [Lien]({t['url']})" if t.get("url") else ""
            date_aff = f" (Date : {t.get('date', 'N/C')})" if t.get('date') else ""
            st.markdown(f"- [Niveau {t.get('hierarchie', 'N/C')}] **{t['titre']}** ({t['theme']}){date_aff} [{stat}]{url_display}")

# --- MODULE 4 : FICHE COLLECTIVITÉ ---
elif menu == "4. Fiche collectivité":
    st.header("Fiche collectivité et gestion des agents")
    
    db_collabs = charger_collectivites()
    noms_collabs = sorted([c["idc"] for c in db_collabs], key=cle_tri)

    if "coll_choix" not in st.session_state or st.session_state["coll_choix"] not in noms_collabs:
        st.session_state["coll_choix"] = noms_collabs[0] if noms_collabs else ""

    col_Sel, col_Nouv = st.columns([2, 1])
    with col_Sel:
        coll_selectionnee = st.selectbox("Sélectionner une collectivité existante :", noms_collabs, key="coll_choix")
    with col_Nouv:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.popover("➕ Créer une nouvelle collectivité"):
            st.text_input("Nom de la nouvelle collectivité", key="nom_nouvelle_collectivite")
            st.button("Valider la création", on_click=creer_collectivite)

    if "msg_collectivite" in st.session_state:
        st.success(st.session_state["msg_collectivite"])
        del st.session_state["msg_collectivite"]
    if "err_collectivite" in st.session_state:
        st.error(st.session_state["err_collectivite"])
        del st.session_state["err_collectivite"]

    if coll_selectionnee:
        st.markdown("---")
        st.subheader(f"Gestion de la collectivité : {coll_selectionnee}")

        with st.form(key=f"form_renommer_{coll_selectionnee}"):
            nouveau_nom_input = st.text_input("Modifier le nom de la collectivité", value=coll_selectionnee)
            if st.form_submit_button("Enregistrer le nouveau nom"):
                renommer_collectivite(coll_selectionnee, f"Form_{coll_selectionnee}")
                st.rerun()

        collec_obj = next((c for c in db_collabs if c["idc"] == coll_selectionnee), None)
        agents = collec_obj.get("agents", []) if collec_obj else []

        st.markdown("#### Agents rattachés :")
        if agents:
            for idx_a, ag in enumerate(agents):
                with st.expander(f"{ag.get('prenom', '')} {ag.get('nom', '')} (Poste : {ag.get('poste', 'N/C')})"):
                    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
                    with col_e1:
                        new_p = st.text_input("Prénom", value=ag.get('prenom', ''), key=f"ag_p_{ag['id']}")
                    with col_e2:
                        new_n = st.text_input("Nom", value=ag.get('nom', ''), key=f"ag_n_{ag['id']}")
                    with col_e3:
                        new_po = st.text_input("N° de poste", value=ag.get('poste', ''), key=f"ag_po_{ag['id']}")
                    with col_e4:
                        new_m = st.text_input("Mail", value=ag.get('mail', ''), key=f"ag_m_{ag['id']}")

                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        if st.button("Mettre à jour l'agent", key=f"btn_upd_ag_{ag['id']}"):
                            ag['prenom'] = new_p
                            ag['nom'] = new_n
                            ag['poste'] = new_po
                            ag['mail'] = new_m
                            sauver_collectivites(db_collabs)
                            st.success("Agent mis à jour.")
                            st.rerun()
                    with col_m2:
                        if st.button("🗑 Supprimer l'agent", key=f"btn_del_ag_{ag['id']}setItem"):
                            agents.pop(idx_a)
                            sauver_collectivites(db_collabs)
                            st.success("Agent supprimé.")
                            st.rerun()
        else:
            st.info("Aucun agent enregistré pour cette collectivité.")

        st.markdown("#### Ajouter un nouvel agent :")
        with st.form("form_ajout_agent_collec"):
            ap_prenom = st.text_input("Prénom de l'agent")
            ap_nom = st.text_input("Nom de l'agent")
            ap_poste = st.text_input("N° de poste")
            ap_mail = st.text_input("Adresse mail")
            if st.form_submit_button("Ajouter l'agent à la collectivité"):
                if ap_prenom or ap_nom:
                    agents.append({
                        "id": uuid.uuid4().hex[:8],
                        "prenom": ap_prenom,
                        "nom": ap_nom,
                        "poste": ap_poste,
                        "mail": ap_mail
                    })
                    sauver_collectivites(db_collabs)
                    st.success("Agent ajouté avec succès.")
                    st.rerun()
                else:
                    st.error("Veuillez renseigner au moins le prénom ou le nom de l'agent.")

# --- MODULE 5 : EXTRACTION ---
elif menu == "5. Extraction":
    st.header("Extraction XML")
    
    df_ex_base = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    if df_ex_base.empty:
        st.info("Aucune saisine en base pour l'extraction.")
    else:
        type_ext = st.radio("Critère d'extraction XML :", ["Extraction globale", "Par collectivité (IDC)", "Par conseiller (IDAG)"])
        df_cible = df_ex_base.copy()

        if type_ext == "Par collectivité (IDC)":
            collabs_list = sorted(df_ex_base["IDC"].unique().tolist())
            choix_c = st.selectbox("Sélectionner la collectivité :", collabs_list)
            if choix_c:
                df_cible = df_cible[df_cible["IDC"] == choix_c]
        elif type_ext == "Par conseiller (IDAG)":
            conseillers_list = sorted(df_ex_base["IDAG"].unique().tolist())
            choix_con = st.selectbox("Sélectionner le conseiller :", conseillers_list)
            if choix_con:
                df_cible = df_cible[df_cible["IDAG"] == choix_con]

        st.write(f"Nombre de fiches à exporter : **{len(df_cible)}**")

        root = ET.Element("SaisinesMerlin")
        for _, row in df_cible.iterrows():
            fiche_elem = ET.SubElement(root, "Fiche")
            for col in df_cible.columns:
                child = ET.SubElement(fiche_elem, col)
                child.text = str(row[col])
        
        xml_data = ET.tostring(root, encoding="utf-8", method="xml")

        st.download_button(
            label="Télécharger le fichier XML",
            data=xml_data,
            file_name="extraction_merlin.xml",
            mime="application/xml"
        )

# --- MODULE 6 : MON COMPTE ---
else:
    st.header("Mon Compte")
    st.write(f"Connecté en tant que : **{gestionnaire_nom}** (`{st.session_state.user_username}`)")

    with st.form("form_change_pwd"):
        st.subheader("Modifier mon mot de passe")
        old_pwd = st.text_input("Ancien mot de passe", type="password")
        new_pwd = st.text_input("Nouveau mot de passe", type="password")
        confirm_pwd = st.text_input("Confirmer le nouveau mot de passe", type="password")
        submit_pwd = st.form_submit_button("Modifier le mot de passe")

        if submit_pwd:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
            
            current_user_key = st.session_state.user_username
            if users[current_user_key]["pwd"] == old_pwd:
                if new_pwd == confirm_pwd and new_pwd.strip() != "":
                    users[current_user_key]["pwd"] = new_pwd
                    with open(USERS_FILE, "w", encoding="utf-8") as f:
                        json.dump(users, f, ensure_ascii=False, indent=4)
                    st.success("Mot de passe modifié avec succès.")
                else:
                    st.error("Les nouveaux mots de passe ne correspondent pas ou sont vides.")
            else:
                st.error("L'ancien mot de passe est incorrect.")

    if st.button("Se déconnecter"):
        st.session_state.logged_in = False
        st.session_state.user_username = ""
        st.session_state.user_nom = ""
        st.rerun()
