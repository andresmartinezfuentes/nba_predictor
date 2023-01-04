from bs4 import BeautifulSoup
import requests

NOMBRES ={
    'ATL': 'Atlanta Hawks',
    'BKN': 'Brooklyn Nets',
    'BOS': 'Boston Celtics',
    'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GS': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NO': 'New Orleans Pelicans',
    'NY': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SA': 'San Antonio Spurs',
    'SAC': 'Sacramento Kings',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'}

def make_prediction(team):
    r_1 = requests.get('https://www.sportytrader.es/ajax/pronostics1x2/baloncesto/competition-306/1/')
    r_2 = requests.get('https://www.sportytrader.es/ajax/pronostics1x2/baloncesto/competition-306/2/')
    soup_1 = BeautifulSoup(r_1.text, 'lxml')
    soup_2 = BeautifulSoup(r_2.text, 'lxml')

    predictions_1 = soup_1.find_all('div',id='1x2wrap')
    predictions_2 = soup_2.find_all('div',id='1x2wrap')

    steams_1 = predictions_1[0].find_all('div',class_="w-1/2 text-center break-word p-1 dark:text-white")
    steams_2 = predictions_2[0].find_all('div',class_="w-1/2 text-center break-word p-1 dark:text-white")

    teams_1 = []
    for el in steams_1:
        teams_1.append(el.text)

    teams_2 = []
    for el in steams_2:
        teams_2.append(el.text)

    str_nombre = f'\n{NOMBRES[team]}\n'
    
    if str_nombre in teams_1:
        pred = predictions_1[0].find_all('div',class_="flex flex-col xl:flex-row justify-center items-center border-2 border-primary-grayborder rounded-lg p-2 my-4")[int(teams_1.index(str_nombre))//2]
        pred = pred.find_all('div',class_="w-full xl:w-2/5 flex justify-center items-center py-4")[0]
        pred = pred.find_all('span', class_="flex justify-center items-center h-7 w-6 rounded-md font-semibold bg-primary-green text-white mx-1")[0].text
        odd = int(pred)
        predict = {}

        if odd == 1:
            predict['winner'] = teams_1[2*(int(teams_1.index(str_nombre))//2)]
            predict['loser'] = teams_1[2*(int(teams_1.index(str_nombre))//2)+1]
        elif odd == 2:
            predict['winner'] = teams_1[2*(int(teams_1.index(str_nombre))//2)+1]
            predict['loser'] = teams_1[2*(int(teams_1.index(str_nombre))//2)]
    elif str_nombre in teams_2:
        pred = predictions_2[0].find_all('div',class_="h-14 flex justify-center items-center w-full xl:w-2/5 mt-1")[int(teams_2.index(str_nombre))//2]
    
        odd = int(pred[int(teams_1.index(str_nombre))//2].find_all('div',class_="flex justify-center items-center h-7 w-6 rounded-md font-semibold bg-primary-green text-white mx-1")[0].attrs)
        predict = {}

        if odd == 1:
            predict['winner'] = teams_1[2*(int(teams_1.index(str_nombre))//2)]
            predict['loser'] = teams_1[2*(int(teams_1.index(str_nombre))//2)+1]
        elif odd == 2:
            predict['winner'] = teams_1[2*(int(teams_1.index(str_nombre))//2)+1]
            predict['loser'] = teams_1[2*(int(teams_1.index(str_nombre))//2)]
        
    text = '\t\t PREDICCIÓN DE GANADOR\n\n'
    text += f"EL ganador del proximo partido de {NOMBRES[team]} será: {predict['winner']}y el perdedor será: {predict['loser']}"

    return text
