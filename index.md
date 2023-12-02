---
layout: default
title: Ed's Work
---
# Quick Links
- [2022 NDVI for Marina, Mission, North Beach](#2022-ndvi-for-popular-neighborhoods-in-san-francisco)
- [Fire Density in California Watersheds](#fire-density-in-california-watersheds)
- [Vegetation Recovery after the Caldor Fire](#vegetation-recovery-after-the-caldor-fire)
- [Flood Frequency Analysis of Penn State](#flood-frequency-analysis-of-penn-state)
- [San Francisco Average Temperatures](#san-francisco-average-temperatures)
- [About Me](#about-me)

***
# 2022 NDVI for Popular Neighborhoods in San Francisco
2022 NDVI statistics were calculated for three popular neighborhoods (Marina, Mission, North Beach) in San Francisco to assess the greenness and overall suitability for living in each neighborhood. Presidio was added as a benchmark. Nothing conclusive, but it's fun to just look from this perspective!
[<sub><sup>Interactive HTML</sup></sub>](https://eggvoice.github.io/notebooks/san-francisco-multispectral.html)
[<sub><sup>Source Code</sup></sub>](https://github.com/eggvoice/eggvoice.github.io/blob/main/notebooks/san-francisco-multispectral.ipynb)\
![San Francisco Chloropleth Table](img/sfo_chloropleth_table.png)\
![San Francisco Chloropleth](img/sfo_chloropleth.png)
##### Data Source:
[San Francisco Open Data](https://data.sfgov.org/Geographic-Locations-and-Boundaries/SF-Find-Neighborhoods/pty2-tcw4)\
[San Francisco 2022 NAIP](https://naip-usdaonline.hub.arcgis.com/)

# Fire Density in California Watersheds
Increasing both numbers and sizes of wildfire in California Watersheds.\
In the case of Sacremento, fire size is increasing in recent times.
[<sub><sup>Interactive HTML</sup></sub>](https://eggvoice.github.io/notebooks/wildfire-fire-density.html)\
![CA Watersheds - Fire Density 1992-2020](img/ca_fire_density_sorted.png)
![CA Watersheds - Fire Density Chloropleth Plot](img/fire_density_chloropleth_plot.png)
![Sacremento - Fire Occurrence and Size](img/larger_fires_in_sacremento.png)

# Vegetation Recovery after the Caldor Fire
Plotting dNDVI before and after the Caldor Fire suggests recovery in vegetation after two years.\
[<sub><sup>Interactive HTML</sup></sub>](https://eggvoice.github.io/notebooks/modis-ndvi-caldor-fire.html)
![Caldor Fire Boundary](img/caldor_fire_boundary.png)
![Caldor Fire - Change in NDVI between 2020 and 2023](img/caldor_change_in_ndvi_spatial.png)
![Caldor Fire - Difference in NDVI inside and outside Caldor Fire boundary](img/caldor_change_in_ndvi_numeric.png)

##### Python Libraries: 
[`earthpy`](https://github.com/earthlab/earthpy), [`folium`](https://github.com/python-visualization/folium), [`geopandas`](https://github.com/geopandas/geopandas), [`matplotlib`](https://github.com/matplotlib/matplotlib), [`pandas`](https://github.com/pandas-dev/pandas), [`rioxarray`](https://github.com/corteva/rioxarray), [`xarray`](https://github.com/pydata/xarray)

##### Data Source:
* [WFIGS Interagency Perimeters > Filter (poly_IncidentName=Caldor)](https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-interagency-fire-perimeters/api)
* NDVI dataset at https://appeears.earthdatacloud.nasa.gov/task/area \
(NASA Earthdata account required)
  * Check out [the list of APPEEARS datasets](https://appeears.earthdatacloud.nasa.gov/products)
 
##### Citation: 
* National Interagency Fire Center [The NIFC Org]. (2021). *Wildland Fire Interagency Geospatial Services (WFIGS) Interagency Fire Perimeters.* National Interagency Fire Center ArcGIS Online Organization. Accessed 2023-10-01 from https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-interagency-fire-perimeters/api
* Didan, K. (2021). *MODIS/Aqua Vegetation Indices 16-Day L3 Global 250m SIN Grid V061* [250m 16 days NDVI]. NASA EOSDIS Land Processes Distributed Active Archive Center. Accessed 2023-10-01 from https://doi.org/10.5067/MODIS/MYD13Q1.061

# Flood Frequency Analysis of Penn State
Plotting water time series data (1985-2022) suggests 2004 being the worst flooding year (a 38-year flood event) in the Penn State region in recent times.
[<sub><sup>Interactive HTML</sup></sub>](https://eggvoice.github.io/notebooks/usgs-nwis-time-series-flood-analysis.html)
[<sub><sup>Source Code</sup></sub>](https://github.com/eggvoice/eggvoice.github.io/blob/main/notebooks/usgs-nwis-time-series-flood-analysis.ipynb)
![PSU Daily Streamflow Average](img/psu_daily_streamflow_average.png)
![PSU Streamflow Annual Maxima](img/psu_streamflow_annual_max.png)
![PSU Flood Return Periods](img/psu_flood_return_period.png)

##### Python Libraries: 
[`folium`](https://github.com/python-visualization/folium), [`pandas`](https://github.com/pandas-dev/pandas), [`hvplot`](https://github.com/holoviz/hvplot), [`requests`](https://github.com/psf/requests)

##### Data Source:
[USGS National Water Dashboard > State College, PA > USGS 01546400 (Surface Water, Stream) > Data (Daily Data)](https://waterdata.usgs.gov/nwis/inventory?site_no=01546400)

##### Citation: 
U.S. Geological Survey, 2023, National Water Information System data available on the World Wide Web (USGS Water Data for the Nation), accessed [September 19, 2023], at URL [http://waterdata.usgs.gov/nwis/](http://waterdata.usgs.gov/nwis/)

##### Fun Read:
* [Stationarity is Undead - Risk communication under nonstationarity: a farewell to return period?](https://www.sciencedirect.com/science/article/pii/S0309170815000020?ref=pdf_download&fr=RR-2&rr=8096f5b969a41f3d#s0020)
* [Stationarity is Dead](https://www.law.berkeley.edu/files/CLEE/Milly_2008_Science_StationarityIsDead.pdf)
* ["100-year floods can happen 2 years in a row"](https://www.usgs.gov/special-topics/water-science-school/science/100-year-flood)

# San Francisco Average Temperatures
A upward trend over the observed years (1946-2022)
[<sub><sup>Interactive HTML</sup></sub>](https://eggvoice.github.io/notebooks/ncei_tavg_san_francisco.html)
[<sub><sup>Source Code</sup></sub>](https://github.com/eggvoice/eggvoice.github.io/blob/main/notebooks/ncei_tavg_san_francisco.ipynb)
![San Francisco Average Temperatures](img/san_francisco_tavg_trend.png)

##### Python Libraries: 
[`pandas`](https://github.com/pandas-dev/pandas), [`hvplot`](https://github.com/holoviz/hvplot), [`holoviews`](https://github.com/holoviz/holoviews), [`numpy`](https://github.com/numpy/numpy)

##### Data Source:
[Climate at a Glance > City > Time Series > San Francisco (Average Temperature, 12-Month, December)](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/city/time-series/USW00023174/tavg/12/12/1945-2022.csv)

##### Citation: 
NOAA National Centers for Environmental information, Climate at a Glance: City Time Series, published August 2023, retrieved on September 7, 2023 from [https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/city/time-series](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/city/time-series)

##### Fun Fact:
* Climate at a Glance is created from [NOAAGlobalTemp](https://www.ncei.noaa.gov/products/land-based-station/noaa-global-temp) dataset which includes land surface air (LSAT) temperature from the [Global Historical Climatology Network monthly (GHCNm)](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly) and sea surface temperature (SST) from [Extended Reconstructed SST (ERSST)](https://www.ncei.noaa.gov/products/extended-reconstructed-sst).
* According to this [paper](https://journals.ametsoc.org/view/journals/clim/33/4/jcli-d-19-0395.1.xml), \"LSAT has been measured by meteorological stations since the late 1600s, and SST has been measured by commercial ships since the early 1700s and by moored and drifting buoy floats since the 1970s.\"
* There is a weather station in San Francisco Downtown.\
Topography Description: `IN CENTRAL SAN FRANCISCO ON MINT HILL (ON SITE U.S. MINT) AT THE CORNER OF HERMANN AND BUCHANAN). DOWNTOWN AREA NE THROUGH E.` from [NCDC](https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USW00023272/detail).\
Latitude/Longitude: `37.7705°, -122.4269°` (Plug that into Google Maps!)

***

# About Me:
![Ed's Bio Picture](img/bio.jpg)
> [We came all this way to explore the moon, and the most important thing is that we discovered the Earth.](https://www.nasa.gov/pdf/323298main_CelebrateApolloEarthRise.pdf)

<sup>William Anders, Apollo 8 Astronaut</sup>

Hey there! It's Ed. I am a technical consultant by trade. Having witnessed the [Orange Skies Day](https://en.wikipedia.org/wiki/Orange_Skies_Day) in 2020 when I was living in [Emeryville](https://en.wikipedia.org/wiki/Emeryville,_California) (San Francisco East Bay), I want to find ways to equip ourselves to respond and adapt to this new world we live in. While having a general interest in the space industry, I didn’t always have a strong interest in earth data science until my recent experience at [GNSS+R 2023](https://igs.org/event/ieee-gnssr-2023/) and [ESIP 2023 Summer Meeting](https://www.esipfed.org/meetings). Space up, space down, so to speak. Right now, I am learning geoprocessing with Python at CU Boulder. I am excited to find out where I fit and how I can contribute with my skills. I am the happiest with my little cup of expresso. Open to connect!

**Likes**\
Expresso :coffee:\
Board games :game_die:\
Books :books:

**Interests**\
Climbing\
Python\
California's Geology

**Education**\
MSc Space Studies, [International Space University](https://www.isunet.edu/) (2021)\
BS Information Systems Design and Development, [Penn State](https://www.psu.edu/) (2015)

**Find Me Online**\
Blog: [eggvoice.com](https://eggvoice.com)\
GitHub: [eggvoice](https://github.com/eggvoice)\
Twitter: [myeggvoice](https://twitter.com/myeggvoice)\
LinkedIn: [Edward Chan](https://www.linkedin.com/in/edward6chan/)
