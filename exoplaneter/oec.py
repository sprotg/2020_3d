import csv

#Denne funktion udregner den gennemsnitlige masse for alle exoplaneterne
def getAverageMass():
    totalMass = 0
    numberOfPlanets = 0

    #for-løkken gennemløber hele datasættet
    for row in data:
        #Den kolonne der hedder "PlanetaryMassJpt" indeholde massen, målt i enheden "jupitermasser".
        #Hvis massen ikke findes i datasættet får m værdien '' (En tom streng).
        #Derfor er vi nødt til at undersøge om m har en gyldig værdi,
        #før vi tæller planeten med:
        if row['PlanetaryMassJpt'] != '':
            m = float(row['PlanetaryMassJpt'])
            numberOfPlanets += 1
            totalMass += m


    #Nu kan gennemsnittet udregnes:
    return totalMass/numberOfPlanets



#Her åbnes filen med data
infile = open('oec.csv', mode='r')
#CSV-data læses
reader = csv.DictReader(infile)
#og konverteres til en liste:
data = list(reader)

cmd = ''

while not cmd.startswith('q'):
    cmd = input('Skriv en kommando > ')

    if cmd.startswith('header'):
        print(reader.fieldnames)

    if cmd.startswith('avg mass'):
        print(getAverageMass())
