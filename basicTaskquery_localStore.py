import rdflib
from rdflib.graph import Graph, Store, URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin
from SPARQLWrapper import SPARQLWrapper, RDF, JSON, XML

# Load the RDF file into an RDF graph
rdf_file = "footballMatch_DB_Populated.owl"
graph = rdflib.Graph()
graph.parse(rdf_file, format="xml")

# Define a SPARQL query
query = """
PREFIX ex: <http://www.semanticweb.org/amannaredi/ontologies/2024/3/footballMatch#>
SELECT DISTINCT ?match ?matchName ?matchDate ?competitionName ?stadiumName ?team1Name ?team2Name ?goalsByTeam1 ?goalsByTeam2 ?attendees ?stadiumCapacity
WHERE {
    ?match rdf:type ex:Match;
           ex:matchDate ?matchDate;
           ex:matchName ?matchName;
           ex:partOfCompetition ?competition;
           ex:isHostedBy ?stadium;
           ex:involvesTeam ?team1;
           ex:involvesTeam ?team2;
           ex:goalsByTeam1 ?goalsByTeam1;
           ex:goalsByTeam2 ?goalsByTeam2;
           ex:matchAttendees ?attendees;
           ex:team1Name ?team1Name;
           ex:team2Name ?team2Name.

    ?team1 rdf:type ex:Team.

    ?team2 rdf:type ex:Team.

    ?stadium rdf:type ex:Stadium;
             ex:stadiumName ?stadiumName;
             ex:stadiumCapacity ?stadiumCapacity.


    ?competition rdf:type ex:Competition;
                 ex:competitionName ?competitionName.
}
LIMIT 10
"""

# Execute the query and print the results
results = graph.query(query)
print(f"Total records: {len(results)}")

for row in results:
    print("Match ID:", row["match"])
    print("Match Name:", row["matchName"])
    print("Match Date:", row["matchDate"])
    print("Competition:", row["competitionName"])
    print("Stadium:", row["stadiumName"])
    print("Team 1 Name:", row["team1Name"])
    print("Team 2 Name:", row["team2Name"])
    print("Goals by Team 1:", row["goalsByTeam1"])
    print("Goals by Team 2:", row["goalsByTeam2"])
    print("Attendees:", row["attendees"])
    print("Stadium Capacity:", row["stadiumCapacity"])
    print()
