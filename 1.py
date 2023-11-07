from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Завантажити рдф-граф через ttl-файл
g = Graph()
g.parse("countries_info.ttl")

# Підготовка query для пошуку
query = prepareQuery(
    """
    PREFIX : <http://example.com/demo/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?country ?countryName ?largestNeighbor ?largestNeighborName ?largestNeighborArea
    WHERE {
        ?country a :Country .
        ?country :country_name ?countryName .
        ?country :part_of_continent ?continent_nsEU .
        ?country :has_country_neighbour ?neighbor .
        ?neighbor :country_neighbour_value ?largestNeighbor .
        ?largestNeighbor :country_name ?largestNeighborName .
        ?largestNeighbor :area_in_sq_km ?largestNeighborArea .
        FILTER (?country != ?largestNeighbor)
    }
    ORDER BY DESC(?largestNeighborArea)
    """
)

# Виконання SPARQL query
results = g.query(query)

# Створення змінної для збереження найбільшої сусідньої країни для кожної країни
largest_neighbor_dict = {}

# Збереження найбільшої країни-сусіда для кожної країни
for row in results:
    country = row.countryName
    largest_neighbor = row.largestNeighborName
    largest_neighbor_area = row.largestNeighborArea

    if country not in largest_neighbor_dict or largest_neighbor_area > largest_neighbor_dict[country][1]:
        largest_neighbor_dict[country] = (largest_neighbor, largest_neighbor_area)

# Виведення результатів
for country, (largest_neighbor, largest_neighbor_area) in largest_neighbor_dict.items():
    print(f"Country: {country}")
    print(f"Largest Neighbor: {largest_neighbor}")
    print(f"Largest Neighbor Area: {largest_neighbor_area} sq. km")
    print()
