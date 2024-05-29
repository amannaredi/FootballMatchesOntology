import rdflib
from rdflib.graph import Graph, Store, URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin
from SPARQLWrapper import SPARQLWrapper, RDF, JSON, XML


# # Read existing RDF data from the 'books-final.rdf' file
existing_graph = rdflib.Graph()
existing_graph.parse("footballMatch.owl", format="xml")

# # Set up the DBpedia SPARQL endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(RDF)

sparql.setQuery('''
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://www.semanticweb.org/amannaredi/ontologies/2024/3/footballMatch#>

CONSTRUCT {
    ?match rdf:type ex:Match.
    ?match ex:matchName ?matchName.
    ?match ex:matchDate ?matchDate.
    ?match ex:partOfCompetition ?competition.
    ?match ex:isHostedBy ?stadium.
    ?match ex:involvesTeam ?team1.
    ?match ex:involvesTeam ?team2.
    ?match ex:goalsByTeam1 ?goalsByTeam1.
    ?match ex:goalsByTeam2 ?goalsByTeam2.
    ?match ex:matchAttendees ?attendees.
    ?match ex:team1Name ?team1Name.
    ?match ex:team2Name ?team2Name.

    ?team1 rdf:type ex:Team.
    ?team2 rdf:type ex:Team.

    ?stadium rdf:type ex:Stadium.
    ?stadium ex:stadiumName ?stadiumName.
    ?stadium ex:stadiumCapacity ?stadiumCapacity.

    ?competition rdf:type ex:Competition.
    ?competition ex:competitionName ?competitionName.
}
WHERE {
    ?match a dbo:FootballMatch;
          rdfs:label ?matchName;
          dbo:date ?dateLiteral;
          dbo:team ?team;
          dbp:team1score ?goalsByTeam1;
          dbp:team2score ?goalsByTeam2;
          dbp:attendance ?attendees;
          dbo:location ?stadium;
          foaf:name ?competitionName.
    FILTER (LANG(?matchName) = "en")
    BIND(xsd:dateTime(?dateLiteral) AS ?matchDate)
    BIND(URI(CONCAT("http://www.semanticweb.org/amannaredi/ontologies/2024/3/footballMatch#", ENCODE_FOR_URI(?competitionName))) AS ?competition)

    ?team rdfs:label ?teamName.
    FILTER (LANG(?teamName) = "en")

    ?stadium rdfs:label ?stadiumName.


  OPTIONAL{
        {
        SELECT ?stadium (MAX(?capacity) AS ?stadiumCapacity)
        WHERE {
            ?stadium dbo:seatingCapacity ?capacity.
        }
        GROUP BY ?stadium
    }
    }
      FILTER (LANG(?stadiumName) = "en")
    {
        SELECT DISTINCT ?match ?team1 ?team2 ?team1Name ?team2Name
        WHERE {
            ?match dbo:team ?team1, ?team2.
            ?team1 rdfs:label ?team1Name.
            ?team2 rdfs:label ?team2Name.
            FILTER (?team1 != ?team2)
            FILTER (?team1Name < ?team2Name)  # Ensure team1Name is lexicographically less than team2Name
            FILTER (LANG(?team1Name) = "en")
            FILTER (LANG(?team2Name) = "en")
        }
    }
}
LIMIT 50

''')

rdf_data = sparql.query().convert()

# Load the fetched RDF data into an RDF graph
fetched_graph = rdflib.Graph()
fetched_graph.parse(data=rdf_data.serialize(format="xml"), format="xml")

# Merge the existing graph and fetched graph
merged_graph = existing_graph + fetched_graph

# # Serialize and save the merged graph to the 'footballMatch.owl' file
with open("footballMatch.owl", "wb") as rdf_file:
    rdf_file.write(merged_graph.serialize(format="xml").encode('utf-8'))
    
print("DBpedia succefully added")