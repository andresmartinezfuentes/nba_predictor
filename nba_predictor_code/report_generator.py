import requests
import pandas as pd
import prediction
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()

def read_config():
    with open('config.txt','r') as file:
        conf = file.readlines()

    for i in range(len(conf)):
        conf[i] = conf[i].split(':')[1][1:-1]
    
    return conf

def extract(conf: list):
    
    data = []

    data.append(requests.request('GET',f'https://api.sportsdata.io/v3/nba/scores/json/Players/{conf[2]}',headers={conf[0]: conf[1]}).json())

    data.append(requests.request('GET',f'https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/{conf[3]}',headers={conf[0]: conf[1]}).json())

    data.append(requests.request('GET',f'https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStatsByTeam/{conf[3]}/{conf[2]}',headers={conf[0]: conf[1]}).json())

    return data

def transform(data):

    df_players = pd.DataFrame(data[0])
    df_stats = pd.DataFrame(data[1])
    df_player_stats = pd.DataFrame(data[2])

    return df_players, df_stats, df_player_stats

def load( df_players, df_stats, df_player_stats, predict, team):
    df_stats = df_stats.loc[df_stats['Team'] == team]

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial','B',25)
    
    titulo = f'{team} Team Report'
    pdf.cell(100,25,align='C',txt=titulo)

    texto = ""

    texto += '\t\tReporte de jugadores del equipo:\n\n'
    for p in df_players.iloc():
        texto += f" Nombre: {p['FirstName']}, Apellido: {p['LastName']}, Número: {p['Jersey']}, Posición: {p['Position']}, Altura: {p['Height']}, Salario: {p['Salary']}\n"

    texto += '\n\n\t\tReporte de estadistica del equipo en su conjunto\n\n'
    for t in df_stats.iloc():
        texto += f"Datos correspondientes a la temporada {t['Season']}, en esta temporada se ha logrado ganar {t['Wins']} partidos contando con un total de derrotas de {t['Losses']} en unos {t['Games']} partidos totales.\n En toda la temporada se ha contado con {t['Possessions']} posesiones, en todos los partidos el porcentaje de acierto en tiros de dos ha sido del {t['TwoPointersPercentage']}% contando además con un porcentaje de triples del {t['ThreePointersPercentage']}%.\n Por último en toda la temporada se han generado {t['Assists']} asistencias, {t['Steals']} robos y {t['Points']} puntos totales.\n\n"

    texto += '\n\t\tReporte de estadisticas por jugador\n\n'
    for p in df_player_stats.iloc():
        texto +=f"Nombre: {p['Name']}, Minutos jugados: {p['Minutes']}, tiros de dos hechos; porcentaje: {p['TwoPointersMade']}; {p['TwoPointersPercentage']}%, triples acertados; porcentaje{p['ThreePointersMade']}; {p['ThreePointersPercentage']}%, robos de balón: {p['Steals']}, porcentaje de tiros hechos: {p['TrueShootingPercentage']}%, rating de eficiencia: {p['PlayerEfficiencyRating']}\n\n"

    pdf.set_font('Arial','',11)
    pdf.set_xy(10,50)
    pdf.multi_cell(0,5,texto)

    pdf.output('report_nba.pdf')

    print(predict)
    
if __name__ == '__main__':
    conf = read_config()
    data = extract(conf)
    df_players, df_stats, df_player_stats = transform(data)
    predict = prediction.make_prediction(conf[2])
    load( df_players, df_stats, df_player_stats, predict, conf[2])
