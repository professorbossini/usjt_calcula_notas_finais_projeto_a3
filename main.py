from collections import defaultdict
import statistics
import csv
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

}

def buildCompleteTeam (linha, qtdeMembros, inicio):
    team = {'alunos': []}
    for j in range(inicio, inicio + 2* qtdeMembros - 1, 2):
        team['alunos'].append({'ra': linha[j+1], 'nome': linha[j].replace('\t', '').strip()})
    team['nomeDoGrupo'] = linha[i['nomeDoGrupo']].replace('\t', '').strip()
    team['tipoProjeto'] = linha[i['tipoProjeto']].replace('\t', '').strip()
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

def calculateAllRasWithGrades ():
    rasWithGrades = []
    with open (r'notas.csv', encoding='utf-8') as file_notas:
        leitor2 = csv.reader(file_notas, delimiter=',')
        for linha2 in leitor2:
            ra = linha2[i['raUnicoComNota']].replace('\t', '').strip()
            for raWithGrade in rasWithGrades:
                if raWithGrade['ra'] == ra:
                    raWithGrade['notas'].append(statistics.mean(map(int,linha2[i['inicioNotas']:i['finalNotas']])))
                    if 'N' in raWithGrade['destaque']:
                        raWithGrade['destaque'] = linha2[i['destaque']]
                    break
            else:
                rasWithGrades.append({
                    'ra': ra, 
                    'notas':[statistics.mean(map(int,linha2[i['inicioNotas']:i['finalNotas']]))],
                    'destaque': linha2[i['destaque']],
                    'nomeDoGrupo':linha2[i['nomeDoGrupoPlanilhaNotas']].replace('\t', '').strip()
                })
    return rasWithGrades
rasWithGrades = calculateAllRasWithGrades()
for r in rasWithGrades:
    print (r['nomeDoGrupo'])
allTeams = sorted(buildAllTeams(), key=lambda x: x['nomeDoGrupo'])


finalGradesPerGroup = []
for team in allTeams:
    for raWithGrade in rasWithGrades:
        #muitos grupos diferentes com nome igual
        #grupos com nome errado (exemplo: Outro)
        #não vai dar para usar na junção
        # if any (map (lambda x: x['ra'] == raWithGrade['ra'], team['alunos'])) and team['nomeDoGrupo'] == raWithGrade['nomeDoGrupo']:
        if any (map (lambda x: x['ra'] == raWithGrade['ra'], team['alunos'])):
            finalGradesPerGroup.append({
                'alunos': team['alunos'],
                'nomeDoGrupo': team['nomeDoGrupo'],
                'tipoProjeto': team['tipoProjeto'],
                'mediaFinal': statistics.mean(map(int, raWithGrade['notas'])),
                'destaque': raWithGrade['destaque']
            })

# for f in finalGradesPerGroup:
#     print (f['nomeDoGrupo'])

arquivoFinal = open ('20212_usjt_expo_notas_finais.csv', 'w', encoding='UTF-8')
arquivoFinal.writelines ('ra,nome,mediaFinal,nomeGrupo,tipoProjeto,Destaque?\n')
for f in finalGradesPerGroup:
    for aluno in f['alunos']:
        resultingString = f'{aluno["ra"]},{aluno["nome"]},{f["mediaFinal"] / 5 * 10:.2f},{f["nomeDoGrupo"]},{f["tipoProjeto"]},{"Sim" if f["mediaFinal"] / 5 * 10 >= 10 and "S" in f["destaque"] else "Não"}'
        print (
            resultingString
        )
        arquivoFinal.writelines(resultingString)
        arquivoFinal.writelines('\n')









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
                   
        
