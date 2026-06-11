import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="DataViz Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 2px;
    }
    .quantitative { background: #e3f2fd; color: #1565c0; }
    .qualitative { background: #fce4ec; color: #c62828; }
    .date { background: #e8f5e9; color: #2e7d32; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FONCTIONS DE DETECTION DES TYPES
# ============================================================

def detect_variable_types(df):
    """Detecte automatiquement le type de chaque variable"""
    types_dict = {}

    for col in df.columns:
        series = df[col]

        # Verifier si c'est une date
        if pd.api.types.is_datetime64_any_dtype(series):
            types_dict[col] = "Date"
            continue

        # Essayer de convertir en datetime
        try:
            converted = pd.to_datetime(series, errors='coerce')
            if converted.notna().sum() / len(series) > 0.8:
                types_dict[col] = "Date"
                continue
        except:
            pass

        # Verifier si numerique
        if pd.api.types.is_numeric_dtype(series):
            n_unique = series.nunique()
            n_total = len(series.dropna())

            if n_unique <= 10 and n_unique / n_total < 0.1:
                types_dict[col] = "Qualitative"
            else:
                types_dict[col] = "Quantitative"
        else:
            n_unique = series.nunique()
            n_total = len(series.dropna())

            if n_unique <= 15 or (n_unique / n_total < 0.3 and n_unique < 50):
                types_dict[col] = "Qualitative"
            else:
                types_dict[col] = "Qualitative"

    return types_dict

def get_type_color(vtype):
    colors = {"Quantitative": "🔵", "Qualitative": "🔴", "Date": "🟢"}
    return colors.get(vtype, "⚪")

# ============================================================
# FONCTIONS DE VISUALISATION
# ============================================================

def create_bar_chart(df, x_col, y_col=None, title=""):
    """Graphique en barres"""
    if y_col and y_col in df.columns:
        fig = px.bar(df, x=x_col, y=y_col, title=title, 
                     color=x_col, template="plotly_white")
    else:
        counts = df[x_col].value_counts().reset_index()
        counts.columns = [x_col, 'Count']
        fig = px.bar(counts, x=x_col, y='Count', title=title,
                     color=x_col, template="plotly_white")
    fig.update_layout(showlegend=False)
    return fig

def create_histogram(df, col, title=""):
    """Histogramme"""
    fig = px.histogram(df, x=col, title=title, 
                       nbins=20, template="plotly_white",
                       color_discrete_sequence=['#1f77b4'])
    fig.update_layout(showlegend=False)
    return fig

def create_scatter(df, x_col, y_col, title=""):
    """Nuage de points"""
    fig = px.scatter(df, x=x_col, y=y_col, title=title,
                     template="plotly_white", opacity=0.7,
                     color_discrete_sequence=['#e74c3c'])
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    return fig

def create_boxplot(df, x_col, y_col, title=""):
    """Boite a moustaches"""
    fig = px.box(df, x=x_col, y=y_col, title=title,
                 template="plotly_white", color=x_col)
    fig.update_layout(showlegend=False)
    return fig

def create_line_chart(df, x_col, y_col=None, title=""):
    """Graphique lineaire temporel"""
    df_temp = df.copy()
    df_temp[x_col] = pd.to_datetime(df_temp[x_col])

    if y_col and y_col in df_temp.columns:
        fig = px.line(df_temp.sort_values(x_col), x=x_col, y=y_col, 
                      title=title, template="plotly_white",
                      markers=True)
    else:
        counts = df_temp.groupby(x_col).size().reset_index(name='Count')
        fig = px.line(counts.sort_values(x_col), x=x_col, y='Count',
                      title=title, template="plotly_white",
                      markers=True)
    return fig

def create_pie_chart(df, col, title=""):
    """Graphique circulaire"""
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, 'Count']
    fig = px.pie(counts, names=col, values='Count', title=title,
                 template="plotly_white", hole=0.4)
    return fig

def create_heatmap_corr(df, num_cols, title=""):
    """Heatmap de correlation"""
    corr = df[num_cols].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto",
                    title=title, template="plotly_white",
                    color_continuous_scale="RdBu_r")
    return fig

# ============================================================
# INTERFACE PRINCIPALE
# ============================================================

st.markdown('<div class="main-header">📊 DataViz Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyse & Visualisation Automatique de Donnees</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📁 Import des Donnees")

    uploaded_file = st.file_uploader(
        "Charger un fichier (CSV, Excel)",
        type=['csv', 'xlsx', 'xls']
    )

    st.markdown("---")
    st.info("💡 **Limite :** 100 lignes x 20 colonnes max")

    use_demo = st.checkbox("📋 Utiliser donnees de demonstration", value=not uploaded_file)

    if use_demo and not uploaded_file:
        st.success("✅ Mode demo active")

# ============================================================
# CHARGEMENT DES DONNEES
# ============================================================

df = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success(f"✅ Fichier charge : {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f"❌ Erreur : {e}")

elif use_demo:
    np.random.seed(42)
    n = 100

    df = pd.DataFrame({
        'Date_Vente': pd.date_range('2024-01-01', periods=n, freq='D'),
        'Produit': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones'], n),
        'Categorie': np.random.choice(['Electronics', 'Accessories'], n),
        'Prix_Unitaire': np.random.uniform(50, 1500, n).round(2),
        'Quantite': np.random.randint(1, 20, n),
        'Region': np.random.choice(['Nord', 'Sud', 'Est', 'Ouest'], n),
        'Satisfaction_Client': np.random.choice(['Faible', 'Moyen', 'Eleve'], n),
        'Remise_%': np.random.uniform(0, 30, n).round(1),
        'Frais_Livraison': np.random.uniform(5, 50, n).round(2),
        'Mois': np.random.choice(['Jan', 'Fev', 'Mar', 'Avr', 'Mai'], n)
    })

    df['Chiffre_Affaires'] = (df['Prix_Unitaire'] * df['Quantite'] * (1 - df['Remise_%']/100)).round(2)
    df['Profit'] = (df['Chiffre_Affaires'] * 0.25).round(2)

# ============================================================
# AFFICHAGE DU DASHBOARD
# ============================================================

if df is not None:

    if len(df) > 100:
        st.warning(f"⚠️ Dataset trop grand ({len(df)} lignes). Tronque a 100 lignes.")
        df = df.head(100)

    if len(df.columns) > 20:
        st.warning(f"⚠️ Trop de colonnes ({len(df.columns)}). Garde les 20 premieres.")
        df = df.iloc[:, :20]

    var_types = detect_variable_types(df)

    quant_cols = [c for c, t in var_types.items() if t == "Quantitative"]
    qual_cols = [c for c, t in var_types.items() if t == "Qualitative"]
    date_cols = [c for c, t in var_types.items() if t == "Date"]

    # BARRE DE METRIQUES
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Lignes", len(df))
    with col2:
        st.metric("📋 Colonnes", len(df.columns))
    with col3:
        st.metric("🔵 Quantitatives", len(quant_cols))
    with col4:
        st.metric("🔴 Qualitatives", len(qual_cols))
    with col5:
        st.metric("🟢 Dates", len(date_cols))

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📋 Apercu des Donnees", "🔍 Analyse Auto", "🎨 Visualisation Libre"])

    # ==========================
    # TAB 1: APERCU
    # ==========================
    with tab1:
        st.subheader("📋 Apercu des Donnees")

        st.markdown("**🔧 Filtre rapide :**")
        filter_cols = st.multiselect("Colonnes a afficher", df.columns.tolist(), default=df.columns.tolist()[:8])

        if filter_cols:
            st.dataframe(df[filter_cols], use_container_width=True, height=400)

        st.subheader("🔍 Types de Variables Detectes")

        cols_display = st.columns(3)

        with cols_display[0]:
            st.markdown("**🔵 Quantitatives**")
            for c in quant_cols:
                st.markdown(f'<span class="type-badge quantitative">{c}</span>', unsafe_allow_html=True)

        with cols_display[1]:
            st.markdown("**🔴 Qualitatives**")
            for c in qual_cols:
                st.markdown(f'<span class="type-badge qualitative">{c}</span>', unsafe_allow_html=True)

        with cols_display[2]:
            st.markdown("**🟢 Dates**")
            for c in date_cols:
                st.markdown(f'<span class="type-badge date">{c}</span>', unsafe_allow_html=True)

        st.subheader("📊 Statistiques Descriptives")
        st.dataframe(df.describe(include='all').T, use_container_width=True)

    # ==========================
    # TAB 2: ANALYSE AUTO
    # ==========================
    with tab2:
        st.subheader("🤖 Analyse Automatique des Variables")

        selected_var = st.selectbox("**Choisir une variable a analyser :**", df.columns)
        vtype = var_types[selected_var]

        st.info(f"**Type detecte :** {get_type_color(vtype)} **{vtype}**")

        st.markdown("---")
        st.markdown("**🎚️ Filtres :**")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            if qual_cols:
                filter_qual = st.selectbox("Filtrer par variable qualitative", ["Aucun"] + qual_cols)
                if filter_qual != "Aucun":
                    filter_val = st.multiselect(f"Valeurs de {filter_qual}", 
                                                df[filter_qual].unique().tolist(),
                                                default=df[filter_qual].unique().tolist())
                    df_filtered = df[df[filter_qual].isin(filter_val)]
                else:
                    df_filtered = df.copy()
            else:
                df_filtered = df.copy()

        with filter_col2:
            if quant_cols:
                filter_quant = st.selectbox("Filtrer par variable quantitative", ["Aucun"] + quant_cols)
                if filter_quant != "Aucun":
                    min_val, max_val = float(df[filter_quant].min()), float(df[filter_quant].max())
                    range_val = st.slider(f"Plage de {filter_quant}", min_val, max_val, (min_val, max_val))
                    df_filtered = df_filtered[(df_filtered[filter_quant] >= range_val[0]) & 
                                               (df_filtered[filter_quant] <= range_val[1])]

        n_rows = len(df_filtered)
        title = f"Analyse de '{selected_var}' ({vtype}) — {n_rows} observations"

        st.markdown(f"<h3 style='text-align:center; color:#1f77b4;'>{title}</h3>", unsafe_allow_html=True)

        if vtype == "Qualitative":
            col_left, col_right = st.columns(2)
            with col_left:
                fig = create_bar_chart(df_filtered, selected_var, title=f"Distribution de {selected_var}")
                st.plotly_chart(fig, use_container_width=True)
            with col_right:
                fig2 = create_pie_chart(df_filtered, selected_var, title=f"Repartition de {selected_var}")
                st.plotly_chart(fig2, use_container_width=True)

        elif vtype == "Quantitative":
            col_left, col_right = st.columns(2)
            with col_left:
                fig = create_histogram(df_filtered, selected_var, title=f"Distribution de {selected_var}")
                st.plotly_chart(fig, use_container_width=True)
            with col_right:
                fig2 = px.box(df_filtered, y=selected_var, title=f"Boite a moustaches de {selected_var}",
                             template="plotly_white", color_discrete_sequence=['#27ae60'])
                st.plotly_chart(fig2, use_container_width=True)

        elif vtype == "Date":
            fig = create_line_chart(df_filtered, selected_var, title=f"Evolution temporelle de {selected_var}")
            st.plotly_chart(fig, use_container_width=True)

    # ==========================
    # TAB 3: VISUALISATION LIBRE
    # ==========================
    with tab3:
        st.subheader("🎨 Createur de Graphiques")

        col_x, col_y, col_chart = st.columns(3)

        with col_x:
            x_var = st.selectbox("**Variable X**", df.columns, index=0)
            x_type = var_types[x_var]
            st.caption(f"Type: {get_type_color(x_type)} {x_type}")

        with col_y:
            y_var = st.selectbox("**Variable Y (optionnel)**", ["Aucune"] + df.columns.tolist(), index=0)
            if y_var != "Aucune":
                y_type = var_types[y_var]
                st.caption(f"Type: {get_type_color(y_type)} {y_type}")

        with col_chart:
            chart_options = [
                "🤖 Auto (recommande)",
                "📊 Bar Chart",
                "📈 Histogramme",
                "🔵 Scatter Plot",
                "📦 Boxplot",
                "📉 Line Chart",
                "🥧 Pie Chart",
                "🔥 Heatmap Correlations"
            ]
            chart_type = st.selectbox("**Type de graphique**", chart_options)

        st.markdown("---")
        st.markdown("**🎚️ Filtres du Dashboard :**")

        filt_col1, filt_col2, filt_col3 = st.columns(3)

        df_viz = df.copy()

        with filt_col1:
            if qual_cols:
                dash_filter = st.selectbox("Filtrer par", ["Aucun"] + qual_cols, key="dash_filter")
                if dash_filter != "Aucun":
                    vals = st.multiselect("Valeurs", df[dash_filter].unique().tolist(),
                                          default=df[dash_filter].unique().tolist(), key="dash_vals")
                    df_viz = df_viz[df_viz[dash_filter].isin(vals)]

        with filt_col2:
            if quant_cols:
                range_filter = st.selectbox("Plage sur", ["Aucun"] + quant_cols, key="range_f")
                if range_filter != "Aucun":
                    mn, mx = float(df[range_filter].min()), float(df[range_filter].max())
                    rg = st.slider("Plage", mn, mx, (mn, mx), key="range_sl")
                    df_viz = df_viz[(df_viz[range_filter] >= rg[0]) & (df_viz[range_filter] <= rg[1])]

        with filt_col3:
            if date_cols:
                date_filter = st.selectbox("Periode", ["Aucun"] + date_cols, key="date_f")
                if date_filter != "Aucun":
                    df_viz[date_filter] = pd.to_datetime(df_viz[date_filter])
                    min_d, max_d = df_viz[date_filter].min().date(), df_viz[date_filter].max().date()
                    d_range = st.date_input("Intervalle", (min_d, max_d), key="date_r")
                    if len(d_range) == 2:
                        df_viz = df_viz[(df_viz[date_filter].dt.date >= d_range[0]) & 
                                        (df_viz[date_filter].dt.date <= d_range[1])]

        n_obs = len(df_viz)
        if y_var == "Aucune":
            dyn_title = f"{x_var} — {n_obs} observations"
        else:
            dyn_title = f"{y_var} vs {x_var} — {n_obs} observations"

        st.markdown(f"<h3 style='text-align:center; color:#e74c3c;'>📊 {dyn_title}</h3>", 
                    unsafe_allow_html=True)

        fig = None

        if chart_type == "🤖 Auto (recommande)":
            x_type = var_types[x_var]
            y_type = var_types[y_var] if y_var != "Aucune" else None

            if y_var == "Aucune":
                if x_type == "Qualitative":
                    fig = create_bar_chart(df_viz, x_var, title=f"Distribution de {x_var}")
                elif x_type == "Quantitative":
                    fig = create_histogram(df_viz, x_var, title=f"Distribution de {x_var}")
                elif x_type == "Date":
                    fig = create_line_chart(df_viz, x_var, title=f"Evolution de {x_var}")
            else:
                if x_type == "Quantitative" and y_type == "Quantitative":
                    fig = create_scatter(df_viz, x_var, y_var, title=f"{y_var} vs {x_var}")
                elif (x_type == "Qualitative" and y_type == "Quantitative") or \
                     (x_type == "Quantitative" and y_type == "Qualitative"):
                    if x_type == "Qualitative":
                        fig = create_boxplot(df_viz, x_var, y_var, title=f"{y_var} par {x_var}")
                    else:
                        fig = create_boxplot(df_viz, y_var, x_var, title=f"{x_var} par {y_var}")
                elif x_type == "Date":
                    fig = create_line_chart(df_viz, x_var, y_var, title=f"Evolution de {y_var}")
                elif x_type == "Qualitative" and y_type == "Qualitative":
                    crosstab = pd.crosstab(df_viz[x_var], df_viz[y_var])
                    fig = px.imshow(crosstab, text_auto=True, aspect="auto",
                                    title=f"Tableau croise {x_var} x {y_var}",
                                    template="plotly_white")
                else:
                    fig = create_bar_chart(df_viz, x_var, y_var, title=f"{y_var} par {x_var}")

        elif chart_type == "📊 Bar Chart":
            fig = create_bar_chart(df_viz, x_var, y_var if y_var != "Aucune" else None, 
                                   title=f"Bar Chart: {x_var}")

        elif chart_type == "📈 Histogramme":
            fig = create_histogram(df_viz, x_var, title=f"Histogramme: {x_var}")

        elif chart_type == "🔵 Scatter Plot":
            if y_var != "Aucune":
                fig = create_scatter(df_viz, x_var, y_var, title=f"Scatter: {y_var} vs {x_var}")
            else:
                st.warning("⚠️ Scatter Plot necessite une variable Y")

        elif chart_type == "📦 Boxplot":
            if y_var != "Aucune":
                fig = create_boxplot(df_viz, x_var, y_var, title=f"Boxplot: {y_var} vs {x_var}")
            else:
                st.warning("⚠️ Boxplot necessite une variable Y")

        elif chart_type == "📉 Line Chart":
            fig = create_line_chart(df_viz, x_var, y_var if y_var != "Aucune" else None,
                                    title=f"Line Chart: {x_var}")

        elif chart_type == "🥧 Pie Chart":
            fig = create_pie_chart(df_viz, x_var, title=f"Pie Chart: {x_var}")

        elif chart_type == "🔥 Heatmap Correlations":
            if len(quant_cols) >= 2:
                fig = create_heatmap_corr(df_viz, quant_cols, title="Matrice de Correlation")
            else:
                st.warning("⚠️ Necessite au moins 2 variables quantitatives")

        if fig:
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                csv = df_viz.to_csv(index=False).encode('utf-8')
                st.download_button("💾 Telecharger les donnees filtrees (CSV)", 
                                   csv, "donnees_filtrees.csv", "text/csv")
            with col_exp2:
                st.info("📊 Graphique interactif — survolez pour plus de details")

else:
    st.info("👆 **Veuillez charger un fichier ou activer le mode demo dans la barre laterale.**")

    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.markdown("""
        ### 📤 Upload
        - CSV (.csv)
        - Excel (.xlsx, .xls)
        - Max 100 lignes x 20 colonnes
        """)
    with col_d2:
        st.markdown("""
        ### 🤖 Auto-detection
        - Variables Quantitatives
        - Variables Qualitatives  
        - Variables Temporelles
        """)
    with col_d3:
        st.markdown("""
        ### 📊 Visualisations
        - Bar Chart / Pie Chart
        - Histogramme / Boxplot
        - Scatter Plot / Line Chart
        """)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#999;'>📊 DataViz Intelligence — Developpe avec Streamlit & Plotly</p>", 
            unsafe_allow_html=True)
