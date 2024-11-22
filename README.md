> [!WARNING]
> EPSG.io is transitioning to the [MapTiler Coordinates API](https://documentation.maptiler.com/hc/en-us/articles/16551987730193-Coordinates-API) for `search` and `transform` endpoints, providing a more secure, robust, and scalable solution.
>
> Migrate your search & transform API calls before **1st of February 2025** to avoid interruption of your services. This change has no impact on epsg.io website.
>
> **[Read how to migrate](https://epsg.io/docs#migration)**

# EPSG.io 

![EPSG logo](./static/img/epsg-logo-small.png)

[EPSG.io](https://epsg.io/) is a tool for discovering and accessing global coordinate systems, finding their parameters, and selecting relevant transformations. Created and maintained by the [MapTiler team](https://www.maptiler.com/), it serves as a _custom_ interface to the [EPSG database](https://en.wikipedia.org/wiki/EPSG_Geodetic_Parameter_Dataset).

The service offers a list of projections, coordinate systems, bounding boxes, and transformation options for improved precision in coordinate transformations.

For detailed documentation, visit [epsg.io/docs](https://epsg.io/docs).

## Discovering coordinate systems, ellipsoids, transformations, units
Coordinate systems, ellipsoids, transformations, and units can be discovered directly via the search field at [EPSG.io](https://epsg.io/). The interface supports searching by EPSG codes (e.g., `3857`) or by part of the system's name (e.g., `pseudo-mercator`). Try [epsg.io/2056](https://epsg.io/2056) as an example.

## Export formats for all software
[EPSG.io](https://epsg.io/) offers coordinate reference system definitions in formats compatible with a wide range of geospatial software, including PROJ, GeoServer, Proj4.js, PostGIS, ESRI ArcGIS, and OGC WKT. For example, see [epsg.io/2056-1676.wkt2](https://epsg.io/2056-1676.wkt2).

## EPSG.io endpoints
Using [EPSG.io](https://epsg.io/) endpoints allows users to discover coordinate systems, ellipsoids, units, and other objects, and retrieve specific coordinate definitions in various formats. For more details, visit [epsg.io/docs](https://epsg.io/docs).

## Coordinates API 

![MapTiler logo](./static/img/maptiler-logo-small.png) 

**EPSG.io** is a custom, open service provided by [MapTiler](https://www.maptiler.com/), free of charge. The **Coordinate transformation and search service** is powered by the [MapTiler Coordinates API](https://documentation.maptiler.com/hc/en-us/articles/16551987730193-Coordinates-API). In addition to being compatible with EPSG.io, it introduces the [/transform](https://docs.maptiler.com/cloud/api/coordinates/#transform-coordinates) endpoint for coordinate transformations and [/search](https://docs.maptiler.com/cloud/api/coordinates/#search-coordinate-systems) endpoint for searching through coordinate systems and its components.

The **Coordinates API** from MapTiler offers:
* API for **coordinate transformations**
* API for **searching** and **discovering** coordinate reference systems
* **Stable, reliable service** for integration into applications
* Option to use a dedicated MapTiler API key, enabling cost management across **multiple apps**
* **Batch transformations** for up to 50 points

For detailed API documentation, visit [docs.maptiler.com/cloud/api/coordinates/](https://docs.maptiler.com/cloud/api/coordinates/).

## Migration endpoints from EPSG.io to MapTiler Coordinates API
EPSG.io  is transitioning to the [MapTiler Coordinates API](https://documentation.maptiler.com/hc/en-us/articles/16551987730193-Coordinates-API) for `search` and `transform` services, providing a more secure, robust, and scalable solution.

### Old endpoints:

Search: `https://epsg.io/?q=swiss&format=json`

Transform: `https://epsg.io/trans?data=7.457914,46.948563&s_srs=4326&t_srs=2056`

### New endpoints:

Search: `https://api.maptiler.com/coordinates/search/swiss.json?key=MapTiler-key`

Transform: `https://api.maptiler.com/coordinates/transform/7.457914,46.948563.json?s_srs=4326&t_srs=2056&key=MapTiler-key`

For more details on migration, including JSON response changes and how to get your MapTiler key, read the [migration guide](https://documentation.maptiler.com/hc/en-us/articles/360020950098-How-to-migrate-from-EPSG-io-to-MapTiler-Coordinates-API).
