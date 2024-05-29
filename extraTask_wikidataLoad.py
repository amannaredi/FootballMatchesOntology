import rdflib
from rdflib.graph import Graph, Store, URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin
from SPARQLWrapper import SPARQLWrapper, RDF, JSON, XML

existing_graph = rdflib.Graph()
existing_graph.parse("footballMatch_DB_Populated.owl", format="xml")

# Set up the wikida SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(RDF)

sparql.setQuery('''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://www.semanticweb.org/amannaredi/ontologies/2024/3/footballMatch#>
CONSTRUCT {
  ?match rdf:type ex:Match.
    ?match ex:matchName ?matchName.
    ?match ex:matchDate ?matchDate.
    ?match ex:matchClass ?classLabel.
    ?match ex:partOfCompetition ?competition.
    ?match ex:isHostedBy ?stadium.
    ?match ex:involvesTeam ?team1.
    ?match ex:involvesTeam ?team2.
    ?match ex:matchAttendees ?matchAttendees.
    ?match ex:winnerTeam ?winnerTeamName.

    ?stadium rdf:type ex:Stadium.
    ?stadium ex:stadiumName ?stadiumName.
    ?stadium ex:stadiumCapacity ?stadiumCapacity.

    ?competition rdf:type ex:Competition.
    ?competition ex:competitionName ?competitionName.

}
WHERE {
  ?match wdt:P31 wd:Q17315159; # Instance of a match
         wdt:P2094 ?class;
         wdt:P276 ?stadium;
         wdt:P179 ?competition;
         wdt:P585 ?matchDate;
         wdt:P1346 ?winner;
         wdt:P1110 ?matchAttendees.

  ?stadium wdt:P1083 ?stadiumCapacity;
           wdt:P1705 ?stadiumName.

  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
    ?match rdfs:label ?matchName.
    ?class rdfs:label ?classLabel.
    ?competition rdfs:label ?competitionName.
    ?winner rdfs:label ?winnerTeamName.
  }
}
LIMIT 50
'''
)
print("done")
rdf_data = sparql.query().convert()

# Load the fetched RDF data into an RDF graph
fetched_graph = rdflib.Graph()
fetched_graph.parse(data=rdf_data.serialize(format="xml"), format="xml")

# Merge the existing graph and fetched graph
merged_graph = existing_graph + fetched_graph

# # Serialize and save the merged graph to the 'footballMatch_DB_Populated.owl' file
with open("footballMatch_DB_Populated.owl", "wb") as rdf_file:
    rdf_file.write(merged_graph.serialize(format="xml").encode('utf-8'))

print("Wikidata succefully added")