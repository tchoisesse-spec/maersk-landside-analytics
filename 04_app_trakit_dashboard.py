from dash import Dash, dcc, html, dash_table, Input, Output, callback
import pandas as pd
import plotly.express as px

# 1. Préparation des données simulées (enrichies pour la démonstration)
tracking_data = [
    {"Conteneur": "MSKU9482011", "Axe": "Lomé - Ouagadougou", "Dernier_Jalon": "Transit Start", "Statut": "Normal"},
    {"Conteneur": "MAEU3849202", "Axe": "Lomé - Niamey", "Dernier_Jalon": "Border Crossing", "Statut": "Urgence / En Panne"},
    {"Conteneur": "MSKU1102934", "Axe": "Lomé - Cinkassé", "Dernier_Jalon": "Customs Clearance", "Statut": "Retard Modéré"},
    {"Conteneur": "MSKU7730192", "Axe": "Lomé - Ouagadougou", "Dernier_Jalon": "Destination Arrival", "Statut": "Normal"},
    {"Conteneur": "MAEU9928110", "Axe": "Lomé - Niamey", "Dernier_Jalon": "Transit Start", "Statut": "Normal"},
    {"Conteneur": "MSKU5540293", "Axe": "Lomé - Cinkassé", "Dernier_Jalon": "Border Crossing", "Statut": "Retard Modéré"},
    {"Conteneur": "MAEU2239102", "Axe": "Lomé - Ouagadougou", "Dernier_Jalon": "Customs Clearance", "Statut": "Urgence / En Panne"},
    {"Conteneur": "MSKU8830194", "Axe": "Lomé - Bamako", "Dernier_Jalon": "Transit Start", "Statut": "Normal"},
]

df_original = pd.DataFrame(tracking_data)

# 2. Initialisation de l'application Dash
app = Dash(__name__)

# 3. Structure de la page (Layout) avec design Maersk
app.layout = html.Div(
    style={"fontFamily": "Segoe UI, Arial, sans-serif", "padding": "30px", "backgroundColor": "#f8f9fa"},
    children=[
        
        # En-tête (Header)
        html.Div(
            style={"borderBottom": "4px solid #00abcd", "paddingBottom": "15px", "marginBottom": "30px"},
            children=[
                html.H1(
                    "Maersk Landside Operations - Simulation TrakIT",
                    style={"color": "#002b49", "margin": "0", "fontSize": "32px", "fontWeight": "bold"},
                ),
                html.P(
                    "Suivi en temps réel, indicateurs de performance logistique et gestion dynamique des anomalies.",
                    style={"color": "#555", "marginTop": "5px", "fontSize": "16px"},
                ),
            ]
        ),
        
        # SECTION 1 : Cartes d'indicateurs (KPIs)
        html.Div(
            style={"display": "flex", "justifyContent": "space-between", "marginBottom": "30px", "gap": "20px"},
            children=[
                # Carte Total
                html.Div(
                    style={"flex": "1", "backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.08)", "borderLeft": "6px solid #002b49", "textAlign": "center"},
                    children=[
                        html.H4("TOTAL EN ROUTE", style={"margin": "0", "color": "#777", "fontSize": "14px", "letterSpacing": "1px"}),
                        html.Div(id="kpi-total", style={"fontSize": "36px", "fontWeight": "bold", "color": "#002b49", "marginTop": "10px"})
                    ]
                ),
                # Carte Urgences
                html.Div(
                    style={"flex": "1", "backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.08)", "borderLeft": "6px solid #ffcccc", "textAlign": "center"},
                    children=[
                        html.H4("URGENCES / PANNES", style={"margin": "0", "color": "#cc0000", "fontSize": "14px", "letterSpacing": "1px"}),
                        html.Div(id="kpi-urgences", style={"fontSize": "36px", "fontWeight": "bold", "color": "#cc0000", "marginTop": "10px"})
                    ]
                ),
                # Carte Retards
                html.Div(
                    style={"flex": "1", "backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.08)", "borderLeft": "6px solid #ffe5cc", "textAlign": "center"},
                    children=[
                        html.H4("RETARDS MODÉRÉS", style={"margin": "0", "color": "#cc6600", "fontSize": "14px", "letterSpacing": "1px"}),
                        html.Div(id="kpi-retards", style={"fontSize": "36px", "fontWeight": "bold", "color": "#cc6600", "marginTop": "10px"})
                    ]
                ),
            ]
        ),
        
        # SECTION 2 : Filtres Interactifs
        html.Div(
            style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.08)", "marginBottom": "30px"},
            children=[
                html.H3("Filtres de recherche", style={"color": "#002b49", "marginTop": "0", "marginBottom": "15px", "fontSize": "18px"}),
                html.Div(
                    style={"display": "flex", "gap": "20px"},
                    children=[
                        # Filtre par Axe
                        html.Div(
                            style={"flex": "1"},
                            children=[
                                html.Label("Sélectionner l'Axe :", style={"fontWeight": "bold", "color": "#333", "display": "block", "marginBottom": "8px"}),
                                dcc.Dropdown(
                                    id="filter-axe",
                                    options=[{"label": "Tous les axes", "value": "ALL"}] + [{"label": i, "value": i} for i in df_original["Axe"].unique()],
                                    value="ALL",
                                    clearable=False,
                                    style={"width": "100%"}
                                )
                            ]
                        ),
                        # Filtre par Statut
                        html.Div(
                            style={"flex": "1"},
                            children=[
                                html.Label("Sélectionner le Statut :", style={"fontWeight": "bold", "color": "#333", "display": "block", "marginBottom": "8px"}),
                                dcc.Dropdown(
                                    id="filter-statut",
                                    options=[{"label": "Tous les statuts", "value": "ALL"}] + [{"label": i, "value": i} for i in df_original["Statut"].unique()],
                                    value="ALL",
                                    clearable=False,
                                    style={"width": "100%"}
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        
        # SECTION 3 : Contenu Principal (Tableau à gauche, Graphique à droite)
        html.Div(
            style={"display": "flex", "gap": "30px", "alignItems": "flex-start"},
            children=[
                
                # Tableau de données interactif
                html.Div(
                    style={"flex": "1.5", "backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.08)"},
                    children=[
                        html.H3("Statut des conteneurs actifs", style={"color": "#002b49", "marginTop": "0", "marginBottom": "15px", "fontSize": "18px"}),
                        dash_table.DataTable(
                            id="tracking-table",
                            columns=[{"name": i, "id": i} for i in df_original.columns],
                            style_cell={"textAlign": "center", "padding": "12px", "fontFamily": "Segoe UI, Arial"},
                            style_header={
                                "backgroundColor": "#002b49",
                                "color": "white",
                                "fontWeight": "bold",
                            },
                            style_data_conditional=[
                                {
                                    "if": {
                                        "column_id": "Statut",
                                        "filter_query": "{Statut} eq 'Urgence / En Panne'",
                                    },
                                    "backgroundColor": "#ffcccc",
                                    "color": "#cc0000",
                                    "fontWeight": "bold",
                                },
                                {
                                    "if": {
                                        "column_id": "Statut",
                                        "filter_query": "{Statut} eq 'Retard Modéré'",
                                    },
                                    "backgroundColor": "#ffe5cc",
                                    "color": "#cc6600",
                                    "fontWeight": "bold",
                                },
                                {
                                    "if": {
                                        "column_id": "Statut",
                                        "filter_query": "{Statut} eq 'Normal'",
                                    },
                                    "backgroundColor": "#e5ffcc",
                                    "color": "#006600",
                                    "fontWeight": "bold",
                                },
                            ],
                        )
                    ]
                ),
                
                # Graphique de répartition
                html.Div(
                    style={"flex": "1", "backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.08)"},
                    children=[
                        html.H3("Répartition analytique des statuts", style={"color": "#002b49", "marginTop": "0", "marginBottom": "15px", "fontSize": "18px"}),
                        dcc.Graph(id="status-chart", config={"displayModeBar": False})
                    ]
                )
            ]
        )
    ]
)

# 4. Logique de filtrage et mise à jour (Callback globale)
@callback(
    Output("tracking-table", "data"),
    Output("kpi-total", "children"),
    Output("kpi-urgences", "children"),
    Output("kpi-retards", "children"),
    Output("status-chart", "figure"),
    Input("filter-axe", "value"),
    Input("filter-statut", "value")
)
def update_dashboard(selected_axe, selected_statut):
    # Cloner les données d'origine
    df_filtered = df_original.copy()
    
    # Appliquer le filtre de l'Axe si sélectionné
    if selected_axe != "ALL":
        df_filtered = df_filtered[df_filtered["Axe"] == selected_axe]
        
    # Appliquer le filtre du Statut si sélectionné
    if selected_statut != "ALL":
        df_filtered = df_filtered[df_filtered["Statut"] == selected_statut]
        
    # Recalculer les indicateurs clés (KPIs)
    total_containers = len(df_filtered)
    urgences_count = len(df_filtered[df_filtered["Statut"] == "Urgence / En Panne"])
    retards_count = len(df_filtered[df_filtered["Statut"] == "Retard Modéré"])
    
    # Générer le graphique Plotly interactif
    # On calcule les proportions réelles basées sur la sélection filtrée
    df_counts = df_filtered["Statut"].value_counts().reset_index()
    df_counts.columns = ["Statut", "Nombre"]
    
    # Palette de couleur harmonisée avec les alertes
    color_map = {
        "Normal": "#a3e635",          # Vert doux
        "Urgence / En Panne": "#fca5a5", # Rouge doux
        "Retard Modéré": "#fdbb2d"      # Orange/Jaune doux
    }
    
    fig = px.bar(
        df_counts,
        x="Nombre",
        y="Statut",
        orientation="h",
        color="Statut",
        color_discrete_map=color_map,
        category_orders={"Statut": ["Normal", "Retard Modéré", "Urgence / En Panne"]}
    )
    
    # Personnalisation de l'esthétique du graphique
    fig.update_layout(
        margin={"t": 10, "b": 10, "l": 10, "r": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis={"title": "Nombre de conteneurs", "gridcolor": "#f0f0f0", "dtick": 1},
        yaxis={"title": ""},
        height=300
    )
    
    return df_filtered.to_dict("records"), total_containers, urgences_count, retards_count, fig

# 5. Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True, port=8050)