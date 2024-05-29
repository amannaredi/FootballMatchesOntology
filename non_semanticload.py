import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

fm_ont = Namespace("http://www.semanticweb.org/amannaredi/ontologies/2024/3/footballMatch#")

with open('matches.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    g = Graph()

    for row in reader:
        match_uri = URIRef(fm_ont[row['matchName'].replace(' ', '_')])
        team1_uri = URIRef(fm_ont[row['team1Name'].replace(' ', '_')])
        team2_uri = URIRef(fm_ont[row['team2Name'].replace(' ', '_')])
        stadium_uri = URIRef(fm_ont[row['stadiumName'].replace(' ', '_')])
        competition_uri = URIRef(fm_ont[row['competitionName'].replace(' ', '_')])

        g.add((match_uri, RDF.type, fm_ont.Match))
        g.add((team1_uri, RDF.type, fm_ont.Team))
        g.add((team2_uri, RDF.type, fm_ont.Team))
        g.add((stadium_uri, RDF.type, fm_ont.Stadium))
        g.add((competition_uri, RDF.type, fm_ont.Competition))


        g.add((match_uri, fm_ont.matchName, Literal(row['matchName'])))
        g.add((match_uri, fm_ont.matchDate, Literal(row['MatchDate'], datatype=XSD.dateTime)))
        g.add((match_uri, fm_ont.goalsByTeam1, Literal(int(row['goalsByTeam1']), datatype=XSD.integer)))
        g.add((match_uri, fm_ont.goalsByTeam2, Literal(int(row['goalsByTeam2']), datatype=XSD.integer)))
        g.add((match_uri, fm_ont.matchAttendees, Literal(int(row['matchAttendees']), datatype=XSD.integer)))
        g.add((match_uri, fm_ont.matchClass, Literal(row['matchClass'])))
        g.add((match_uri, fm_ont.winnerTeam, Literal(row['winningTeam'])))
        g.add((match_uri, fm_ont.team1Name, Literal(row['team1Name'])))
        g.add((match_uri, fm_ont.team2Name, Literal(row['team2Name'])))
        g.add((stadium_uri, fm_ont.stadiumCapacity, Literal(int(row['stadiumCapacity']), datatype=XSD.integer)))
        g.add((stadium_uri, fm_ont.stadiumName, Literal(row['stadiumName'])))
        g.add((competition_uri, fm_ont.competitionName, Literal(row['competitionName'])))

        # Object Properties linking individuals
        g.add((match_uri, fm_ont.involvesTeam, team1_uri))
        g.add((match_uri, fm_ont.involvesTeam, team2_uri))
        g.add((match_uri, fm_ont.isHostedBy, stadium_uri))
        g.add((match_uri, fm_ont.partOfCompetition, competition_uri))

rdf_filename = 'footballMatch.rdf'
g.serialize(destination=rdf_filename, format="turtle")  # Turtle is a more readable format
print(f"RDF data generated and saved to '{rdf_filename}'")
