import rdflib
from rdflib.graph import Graph, Store, URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin
from SPARQLWrapper import SPARQLWrapper, RDF, JSON, XML

# Load the RDF file into an RDF graph
rdf_file = "footballMatch_semantic_Populated.owl"
graph = rdflib.Graph()
graph.parse(rdf_file, format="xml")

# Define a SPARQL query
query = """
PREFIX ex: <http://www.semanticweb.org/amannaredi/ontologies/2024/3/footballMatch#>
SELECT DISTINCT ?match ?matchDate ?stadiumName ?stadiumCapacity ?winnerTeam ?matchClass
WHERE {
    ?match rdf:type ex:Match;
           ex:matchDate ?matchDate;
           ex:isHostedBy ?stadium;
           ex:winnerTeam ?winnerTeam;
           ex:matchClass ?matchClass.

    ?match2 rdf:type ex:Match;
           ex:matchDate ?matchDate2;
           ex:isHostedBy ?stadium2;
           ex:winnerTeam ?winnerTeam;
           ex:matchClass ?matchClass.
    

    FILTER(?matchDate = ?matchDate2)

    ?stadium rdf:type ex:Stadium;
             ex:stadiumName ?stadiumName;

    OPTIONAL{
      ?stadium rdf:type ex:Stadium;
             ex:stadiumCapacity ?stadiumCapacity.
             }
             
     ?stadium2 rdf:type ex:Stadium;
             ex:stadiumName ?stadiumName2;

    OPTIONAL{
      ?stadium2 rdf:type ex:Stadium;
             ex:stadiumCapacity ?stadiumCapacity2.
             }
             
    FILTER(?stadiumName = ?stadiumName2)
    
}
LIMIT 10

"""
# Execute the query and print the results
results = graph.query(query)
print(f"Total records: {len(results)}")

for row in results:
    print("Match ID:", row["match"])
    print("Match Date:", row["matchDate"])
    print("Stadium:", row["stadiumName"])
    print("Stadium Capacity:", row["stadiumCapacity"])
    print("Match belongs to class:", row["matchClass"])
    print("Winner Team:",row["winnerTeam"])
    print()



