<p align="center">
  <a href="https://epsg.io/api">official page →</a><br>
  <img src="static/img/maptiler-logo.png" width="400px">
</p>

<p align="center" style="color: #AAA">
  Search and transform coordinate systems from all over the world. Created and maintained by the <a href="https://www.maptiler.com/">MapTiler team</a>.
</p>

<p align="center">
  <img src="https://img.shields.io/twitter/follow/maptiler?style=social"></img>
</p>

# What and why?
The [EPSG.io](https://epsg.io/) service allows you to discover and transform coordinate systems from all over the world. 

To provide you with scalable, high-quality service for developers, we decided to build a dedicated API.

With the new MapTiler Cloud Coordinates API, you can **search for any coordinate system** and **transform coordinates** directly from your JavaScript application, software written in Python or any other modern language, or use the transformation in web map libraries like MapTiler SDK or OpenLayers. 

For details on how to use it with various technologies, use the links below: 

* API Client JavaScript: https://docs.maptiler.com/client-js/coordinates/ 
* OpenLayers: https://openlayers.org/en/latest/apidoc/module-ol_proj_proj4.html#.epsgLookupMapTiler 

# Install
Use the command below to install the Coordinates API Clients JS.

```shell
npm install --save @maptiler/client
```

# API documentation
For more details, additional examples, and a complete reference, visit the [Coordinates API documentation page](https://docs.maptiler.com/cloud/api/coordinates/) and [Coordinates Clients JS](https://docs.maptiler.com/client-js/coordinates/).

## Search 
The `search` lets you perform a free form query to find coordinate systems.

```shell
// in an async function, or as a 'thenable':
const result = await maptilerClient.coordinates.search('mercator');
```

Search for coordinate reference systems (CRS) in the specified country:
```shell
// in an async function, or as a 'thenable':
const result = await maptilerClient.coordinates.search('United Kingdom');
```

Search by EPSG code:
```shell
// in an async function, or as a 'thenable':
const result = await maptilerClient.coordinates.search('code:4326');
```

## Transform
The `transform` allows you to transform coordinates from one system to another.

If not provided, both the source (`sourceCrs`) and the destination (`targetCrs`) are default to **EPSG:4326** (in other words, [WGS84](https://epsg.io/4326)). Here is how to use this feature:

```shell
// in an async function, or as a 'thenable'
const result = await maptilerClient.coordinates.search('pseudo-mercator');

// Providing one coordinate to transform, with a target CRS being EPSG:9793 (RGF93 v2 / Lambert-93, France official CRS)
const resultA = await maptilerClient.coordinates.transform([1, 45], {targetCrs: 9793})

// Using the same logic, we can pass up to 50 coordinates to be transformed
const resultB = await maptilerClient.coordinates.transform([[10, 48], [1, 45]], {targetCrs: 9793})
```

Transforming from ED50 31N to ETRS89 31N:
```shell
// in an async function, or as a 'thenable':
const results = await coordinates.transform({lng: 432648.873, lat: 4624697.432}, {sourceCrs: 23031, targetCrs: 25831});
 ```