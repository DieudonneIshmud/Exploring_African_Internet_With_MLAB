# this is  ndt7 test data in the table `measurement-lab.ndt.tcpinfo`, using bigquery with a specified UUID
SELECT * FROM `measurement-lab.ndt.tcpinfo`
WHERE UUID = "ndt-q78l5_1589309573_000000000052839D"

..............................................................................................
SOURCE :https://bniajfi.org/2020/09/02/is-baltimore-city-getting-fast-enough-internet-speeds/ .
----------------------------------------------------------------------------------------------
#A query that gives a 'shapefile' of a place (Baltimore city in this case): geaographic infromation file-type that gives the longitude and latitudinal points of the perimeter of an area.When these points are plotted on a map, it will outline the shape of that region

SELECT
place_geom,
place_name
FROM
`bigquery-public-data.geo_us_census_places.places_maryland`
WHERE
place_name Like "Baltimore%"

#Since the above can give as the shape of the specified city, we can query query for just the speed test data within the longitude and latitude points of the shape file.
# We calculate the average speeds for Baltimore City from the M-Lab data using the into query shown below:

WITH
baltimore_city AS(
SELECT
place_geom,
place_name,
internal_point_geom
FROM
`bigquery-public-data.geo_us_census_places.places_maryland`
WHERE
place_name Like "Baltimore%")

SELECT
  AVG(a.MeanThroughputMbps) AS AVG_Mbps,
  baltimore_city.place_name AS city,
FROM
  `measurement-lab.ndt.unified_downloads`,
  baltimore_city
WHERE
  ST_WITHIN( ST_GeogPoint(client.Geo.longitude,
  client.Geo.latitude),
  baltimore_city.place_geom)
GROUP BY
  city
