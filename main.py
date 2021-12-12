from collections import defaultdict
import statistics
import csv
import re

i = {
    'qtdeMembros': 20,
    'inicio1Membros': 21,
    'inicio2Membros': 23,
    'inicio3Membros': 27,
    'inicio4Membros': 33,
    'inicio5Membros': 41,
    'inicio6Membros': 51,
    'inicio7Membros': 63,
    'inicio8Membros': 77,
    'tipoProjeto':7,
    'raUnicoComNota': 3,
    'nomeDoGrupo': 9,
    'inicioNotas': 7,
    'finalNotas': 14,
    'destaque': 15,
    'nomeDoGrupoPlanilhaNotas': 5,
    'campus': 2,
    'turno': 5

}

def buildCompleteTeam (linha, qtdeMembros, inicio):
    team = defaultdict(list)
    for j in range(inicio, inicio + 2* qtdeMembros - 1, 2):
        team['alunos'].append({'ra': re.findall('[0-9]+',linha[j+1])[0], 'nome': linha[j].replace('\t', '').strip()})
    team['nomeDoGrupo'] = linha[i['nomeDoGrupo']].replace('\t', '').strip()
    team['tipoProjeto'] = linha[i['tipoProjeto']].replace('\t', '').strip()
    team['campus'] = linha[i['campus']].replace('\t', '').strip()
    team['turno'] = linha[i['turno']].replace('\t', '').strip()
    return team

def buildAllTeams ():
    teams = []
    with open(r'ras_de_todos_os_membros.csv', encoding='utf-8') as file_ras_de_todos_os_membros:
        leitor = csv.reader(file_ras_de_todos_os_membros, delimiter=',')
        for linha in leitor:
            team = buildCompleteTeam(linha, int(linha[i['qtdeMembros']]), i[f'inicio{linha[i["qtdeMembros"]]}Membros'])
            if all(map(lambda x: x['nomeDoGrupo'].replace('\t', '').strip() != linha[i['nomeDoGrupo']].replace('\t', '').strip(), teams)):
                teams.append(team)
        teams = sorted(teams, key=lambda x: x['nomeDoGrupo'].replace('\t', '').strip())
    return teams

def calculateAllRasWithGrades (allTeams):
    with open (r'notas.csv', encoding='utf-8') as file_notas:
        leitor2 = csv.reader(file_notas, delimiter=',')
        for linha2 in leitor2:
            ra = linha2[i['raUnicoComNota']].replace('\t', '').strip()
            teamItBelongsTo = None
            for team in allTeams:
                for aluno in team['alunos']:
                    if aluno['ra'] == ra:
                        teamItBelongsTo = team
                        teamItBelongsTo['notas'].append(
                            statistics.mean([int(a) for a in linha2[i['inicioNotas']:i['finalNotas']]])
                        )
                        if 'N' in teamItBelongsTo['destaque'] or teamItBelongsTo['destaque'] == []:
                            teamItBelongsTo['destaque'] = linha2[i['destaque']]
                        break
    #calcular medias finais
    for team in allTeams:
        team['mediaFinal'] = 0 if len(team['notas']) <= 0 else statistics.mean(team['notas'])
allTeams = sorted(buildAllTeams(), key=lambda x: x['nomeDoGrupo'])

calculateAllRasWithGrades(allTeams)
# for t in allTeams:
#     print (t['nomeDoGrupo'], t['notas'], t['mediaFinal'])


arquivoFinal = open ('20212_usjt_expo_notas_finais.csv', 'w', encoding='UTF-8')
arquivoFinal.writelines ('ra,nome,mediaFinal,campus,turnonomeGrupo,tipoProjeto,Destaque?\n')
for t in allTeams:
    for a in t['alunos']:
        resultingString = f'{a["ra"]},{a["nome"]},{t["mediaFinal"] * 2},{t["campus"]},{t["turno"]},{t["nomeDoGrupo"].replace(",","")},{t["tipoProjeto"].replace(",","")},{0 if t["destaque"] == [] else t["destaque"]}'
        print(resultingString)
        arquivoFinal.writelines(resultingString)
        arquivoFinal.writelines('\n')
    




# for f in finalGradesPerGroup:
#     print (f['nomeDoGrupo'])











# def pertenceAoTime (ra, team):
#     return any(map(lambda x:  x['ra'] == ra, team['alunos']))

# with open(r'ras_de_todos_os_membros.csv', encoding='utf-8') as file_ras_de_todos_os_membros:
#     cont = 0
#     leitor = csv.reader(file_ras_de_todos_os_membros, delimiter=',')
#     for linha in leitor:
#         team = buildCompleteTeam(linha, int(linha[i['qtdeMembros']]), i[f'inicio{linha[i["qtdeMembros"]]}Membros'])
#         with open (r'notas.csv', encoding='utf-8') as file_notas:
#             leitor2 = csv.reader(file_notas, delimiter=',')
#             notasAvaliadores = []
#             for linha2 in leitor2:
#                 if  pertenceAoTime(linha2[i['raUnicoComNota']], team):
#                     notasAvaliadores.append(statistics.mean(map(int,linha2[i['inicioNotas']:i['finalNotas']])))
                   
        
