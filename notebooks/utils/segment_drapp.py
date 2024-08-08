import earthpy.spatial as es
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union
from skimage import io, color
from skimage.segmentation import quickshift
from sklearn.cluster import KMeans
from tqdm import tqdm


def generate_binary_gdf(tilepath, n_clusters=2):
    # Load the image and bands
    tile = rasterio.open(tilepath)

    red = tile.read(1).astype(float)
    green = tile.read(2).astype(float)
    blue = tile.read(3).astype(float)
    nir = tile.read(4).astype(float)

    # Get image bounding box info
    sr = tile.crs
    bounds = tile.bounds
    affine = tile.transform

    # Segment the image using quickshift
    # Quickshift Segmentation: Segment the image using the quickshift algorithm to create superpixels
    img = io.imread(tilepath)
    img = img[:, :, :3]
    segments = quickshift(img, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5).astype('int32')
    print("Quickshift number of segments: %d" % len(np.unique(segments)))

    # Convert segments to vector features
    polys = []
    for shp, value in tqdm(shapes(segments, transform=affine), desc="Converting segments to vector features"):
        polys.append(shp)

    # Compute mean values for each band in each segment
    bands = np.stack([red, green, blue, nir], axis=-1)
    mean_vals = []
    for shp in tqdm(polys, desc="Computing mean values for each band"):
        mask = rasterio.features.geometry_mask([shp], transform=affine, invert=True, out_shape=bands.shape[:2])
        mean_vals.append(bands[mask].mean(axis=0))

    mean_vals = np.array(mean_vals)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(mean_vals)
    labels = kmeans.labels_

    # Create GeoDataFrame with segments and their cluster labels
    geom = [shape(i) for i in polys]
    gdf = gpd.GeoDataFrame({'geometry': geom, 'cluster': labels}, crs=sr)

    # Assuming cluster 0 is 'not tree' and cluster 1 is 'tree' (this can vary based on the data)
    if mean_vals[labels == 0, 3].mean() > mean_vals[labels == 1, 3].mean():
        gdf['class'] = gdf['cluster']
    else:
        gdf['class'] = 1 - gdf['cluster']

    # Dissolve polygons by 'class' to merge connected polygons
    dissolved_gdfs = []
    for cls in tqdm(gdf['class'].unique(), desc="Dissolving polygons by class"):
        class_gdf = gdf[gdf['class'] == cls]
        dissolved_gdf = class_gdf.dissolve()
        dissolved_gdf['class'] = cls
        dissolved_gdfs.append(dissolved_gdf)

    # Combine the dissolved GeoDataFrames
    dissolved_gdf = gpd.GeoDataFrame(pd.concat(dissolved_gdfs, ignore_index=True), crs=sr)

    return dissolved_gdf



    # Load the image and bands
    tile = rasterio.open(tilepath)

    red = tile.read(1).astype(float)
    nir = tile.read(4).astype(float)

    # Get image bounding box info
    sr = tile.crs
    bounds = tile.bounds
    affine = tile.transform

    # Compute NDVI
    ndvi = (nir - red) / (nir + red)

    # Segment the NDVI image using quickshift
    img = io.imread(tilepath)
    img_ndvi = np.expand_dims(ndvi, axis=2).astype(np.float32)
    segments = quickshift(img_ndvi, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5).astype('int32')
    print("Quickshift number of segments: %d" % len(np.unique(segments)))

    # Convert segments to vector features
    polys = []
    for shp, value in tqdm(shapes(segments, transform=affine), desc="Converting segments to vector features"):
        polys.append(shp)

    # Compute mean NDVI for each segment
    mean_ndvi_vals = []
    for shp in tqdm(polys, desc="Computing mean NDVI values"):
        mask = rasterio.features.geometry_mask([shp], transform=affine, invert=True, out_shape=ndvi.shape)
        mean_ndvi_vals.append(ndvi[mask].mean())

    mean_ndvi_vals = np.array(mean_ndvi_vals).reshape(-1, 1)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(mean_ndvi_vals)
    labels = kmeans.labels_

    # Create GeoDataFrame with segments and their cluster labels
    geom = [shape(i) for i in polys]
    gdf = gpd.GeoDataFrame({'geometry': geom, 'cluster': labels}, crs=sr)

    # Assuming cluster 0 is 'not tree' and cluster 1 is 'tree' (this can vary based on the data)
    if mean_ndvi_vals[labels == 0].mean() > mean_ndvi_vals[labels == 1].mean():
        gdf['class'] = gdf['cluster']
    else:
        gdf['class'] = 1 - gdf['cluster']

    # Dissolve polygons by 'class' to merge connected polygons
    dissolved_gdfs = []
    for cls in tqdm(gdf['class'].unique(), desc="Dissolving polygons by class"):
        class_gdf = gdf[gdf['class'] == cls]
        dissolved_gdf = class_gdf.dissolve()
        dissolved_gdf['class'] = cls
        dissolved_gdfs.append(dissolved_gdf)

    # Combine the dissolved GeoDataFrames
    dissolved_gdf = gpd.GeoDataFrame(pd.concat(dissolved_gdfs, ignore_index=True), crs=sr)

    return dissolved_gdf



    # Load the image and bands
    tile = rasterio.open(tilepath)
    red = tile.read(1).astype(float)
    nir = tile.read(4).astype(float)

    # Get image bounding box info
    sr = tile.crs
    bounds = tile.bounds
    affine = tile.transform

    # Compute NDVI using earthpy.spatial.normalized_diff
    ndvi = es.normalized_diff(nir, red)

    # Handle NaN values
    ndvi = np.where(np.isnan(ndvi), 0, ndvi)

    # Segment the NDVI image using quickshift
    img = io.imread(tilepath)
    img_ndvi = np.expand_dims(ndvi, axis=2).astype(np.float32)
    segments = quickshift(img_ndvi, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5).astype('int32')
    print("Quickshift number of segments: %d" % len(np.unique(segments)))

    # Convert segments to vector features
    polys = []
    for shp, value in tqdm(shapes(segments, transform=affine), desc="Converting segments to vector features"):
        polys.append(shp)

    # Compute mean NDVI for each segment
    mean_ndvi_vals = []
    for shp in tqdm(polys, desc="Computing mean NDVI values"):
        mask = rasterio.features.geometry_mask([shp], transform=affine, invert=True, out_shape=ndvi.shape)
        mean_ndvi_vals.append(ndvi[mask].mean())

    mean_ndvi_vals = np.array(mean_ndvi_vals).reshape(-1, 1)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(mean_ndvi_vals)
    labels = kmeans.labels_

    # Create GeoDataFrame with segments and their cluster labels
    geom = [shape(i) for i in polys]
    gdf = gpd.GeoDataFrame({'geometry': geom, 'cluster': labels}, crs=sr)

    # Assuming cluster 0 is 'not tree' and cluster 1 is 'tree' (this can vary based on the data)
    if mean_ndvi_vals[labels == 0].mean() > mean_ndvi_vals[labels == 1].mean():
        gdf['class'] = gdf['cluster']
    else:
        gdf['class'] = 1 - gdf['cluster']

    # Dissolve polygons by 'class' to merge connected polygons
    dissolved_gdfs = []
    for cls in tqdm(gdf['class'].unique(), desc="Dissolving polygons by class"):
        class_gdf = gdf[gdf['class'] == cls]
        dissolved_gdf = class_gdf.dissolve()
        dissolved_gdf['class'] = cls
        dissolved_gdfs.append(dissolved_gdf)

    # Combine the dissolved GeoDataFrames
    dissolved_gdf = gpd.GeoDataFrame(pd.concat(dissolved_gdfs, ignore_index=True), crs=sr)

    return dissolved_gdf


def generate_binary_gdf_ndvi(tilepath, n_clusters=2, plot_segments=False, plot_path=None):
    # Load the image and bands
    tile = rasterio.open(tilepath)
    red = tile.read(1).astype(float)
    nir = tile.read(4).astype(float)

    # Get image bounding box info
    sr = tile.crs
    bounds = tile.bounds
    affine = tile.transform

    # Compute NDVI using earthpy.spatial.normalized_diff
    ndvi = es.normalized_diff(nir, red)

    # Handle NaN values
    ndvi = np.where(np.isnan(ndvi), 0, ndvi)

    # Segment the NDVI image using quickshift
    img = io.imread(tilepath)
    img_ndvi = np.expand_dims(ndvi, axis=2).astype(np.float32)
    rgb_img = img[:, :, :3]
    segments = quickshift(img_ndvi, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5).astype('int32')
    print("Quickshift number of segments: %d" % len(np.unique(segments)))

    # Plot Segments
    if plot_segments:
        fig, ax = plt.subplots(1, 2, figsize=(5, 10))

        # Original Pixels
        ax[0].imshow(rgb_img)
        ax[0].set_title("Original Pixels")
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        ax[0].set_xticklabels([])
        ax[0].set_yticklabels([])
        ax[0].tick_params(axis='both', which='both', length=0)

        # Quickshift Segments
        ax[1].imshow(color.label2rgb(segments, rgb_img, bg_label=0))
        ax[1].set_title("Quickshift Segments")
        ax[1].set_xticks([])
        ax[1].set_yticks([])
        ax[1].set_xticklabels([])
        ax[1].set_yticklabels([])
        ax[1].tick_params(axis='both', which='both', length=0)

        if plot_path:
            plt.savefig(plot_path)
        plt.show()

    # Convert segments to vector features
    polys = []
    for shp, value in tqdm(shapes(segments, transform=affine), desc="Converting segments to vector features"):
        polys.append(shp)

    # Compute mean NDVI for each segment
    mean_ndvi_vals = []
    for shp in tqdm(polys, desc="Computing mean NDVI values"):
        mask = rasterio.features.geometry_mask([shp], transform=affine, invert=True, out_shape=ndvi.shape)
        # by indexes instead of co-ordinates
        # by segments instead of polys 
        # zip them later
        ## have both steps dependent to segments
        mean_ndvi_vals.append(ndvi[mask].mean())

    mean_ndvi_vals = np.array(mean_ndvi_vals).reshape(-1, 1)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(mean_ndvi_vals)
    labels = kmeans.labels_

    # Create GeoDataFrame with segments and their cluster labels
    geom = [shape(i) for i in polys]
    gdf = gpd.GeoDataFrame({'geometry': geom, 'cluster': labels}, crs=sr)

    # Determine which cluster corresponds to 'tree' based on NDVI values
    cluster_mean_ndvi = [mean_ndvi_vals[labels == i].mean() for i in range(n_clusters)]
    tree_cluster_idx = np.argmax(cluster_mean_ndvi)

    # Test
    print("Cluster mean NDVI values:", cluster_mean_ndvi)
    print("Index of tree cluster:", tree_cluster_idx)

    # Assign class labels based on the cluster with higher NDVI being 'tree'
    gdf['class'] = gdf['cluster'].apply(lambda x: 1 if x == tree_cluster_idx else 0)

    # Dissolve polygons by 'class' to merge connected polygons
    dissolved_gdfs = []
    for cls in tqdm(gdf['class'].unique(), desc="Dissolving polygons by class"):
        class_gdf = gdf[gdf['class'] == cls]
        dissolved_gdf = class_gdf.dissolve()
        dissolved_gdf['class'] = cls
        dissolved_gdfs.append(dissolved_gdf)

    # Combine the dissolved GeoDataFrames
    dissolved_gdf = gpd.GeoDataFrame(pd.concat(dissolved_gdfs, ignore_index=True), crs=sr)

    return dissolved_gdf


def generate_binary_gdf_ndvi_v2(tilepath, n_clusters=2, plot_segments=False, plot_path=None):
    # Load the image and bands
    tile = rasterio.open(tilepath)
    red = tile.read(1).astype(float)
    nir = tile.read(4).astype(float)

    # Get image bounding box info
    sr = tile.crs
    bounds = tile.bounds
    affine = tile.transform

    # Compute NDVI using earthpy.spatial.normalized_diff
    ndvi = es.normalized_diff(nir, red)

    # Calculate the total number of pixels in the NDVI array
    total_pixels = ndvi.size
    print(f"Total number of pixels in the NDVI array: {total_pixels}")

    # Handle NaN values
    ndvi = np.where(np.isnan(ndvi), 0, ndvi)

    # Segment the NDVI image using quickshift
    img = io.imread(tilepath)
    img_ndvi = np.expand_dims(ndvi, axis=2).astype(np.float32)
    rgb_img = img[:, :, :3]
    segments = quickshift(img_ndvi, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5).astype('int32')
    print("Quickshift number of segments: %d" % len(np.unique(segments)))

    if plot_segments and plot_path:
        # Plot Original Pixels
        plt.imshow(rgb_img)
        plt.title("Original Pixels")
        plt.axis('off')
        plt.savefig(f"{plot_path}_original_pixels.png")
        plt.close()

        # Plot NDVI
        plt.imshow(ndvi, cmap='RdYlGn')
        plt.title("NDVI")
        plt.axis('off')
        plt.savefig(f"{plot_path}_ndvi.png")
        plt.close()

        # Plot Quickshift Segments
        plt.imshow(color.label2rgb(segments, rgb_img, bg_label=0))
        plt.title("Quickshift Segments")
        plt.axis('off')
        plt.savefig(f"{plot_path}_quickshift_segments.png")
        plt.close()

        # Plot NDVI Mean by Segments
        segment_means = np.zeros_like(ndvi)
        for seg_val in np.unique(segments):
            segment_means[segments == seg_val] = ndvi[segments == seg_val].mean()
        plt.imshow(segment_means, cmap='RdYlGn')
        plt.title("NDVI Mean by Segments")
        plt.axis('off')
        plt.savefig(f"{plot_path}_ndvi_mean_by_segments.png")
        plt.close()

        # Convert segments to vector features
        polys = []
        for shp, value in tqdm(shapes(segments, transform=affine), desc="Converting segments to vector features"):
            polys.append(shp)

        # Compute mean NDVI for each segment
        mean_ndvi_vals = []
        for shp in tqdm(polys, desc="Computing mean NDVI values"):
            mask = rasterio.features.geometry_mask([shp], transform=affine, invert=True, out_shape=ndvi.shape)
            mean_ndvi = ndvi[mask].mean()
            mean_ndvi_vals.append(mean_ndvi)
            if len(mean_ndvi_vals) < 10:
                print(f"Segment: {len(mean_ndvi_vals)} | NDVI Mean: {mean_ndvi}")

        mean_ndvi_vals = np.array(mean_ndvi_vals).reshape(-1, 1)

        # Apply k-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(mean_ndvi_vals)
        labels = kmeans.labels_

        # Create GeoDataFrame with segments and their cluster labels
        geom = [shape(i) for i in polys]
        gdf = gpd.GeoDataFrame({'geometry': geom, 'cluster': labels}, crs=sr)

        # Determine which cluster corresponds to 'tree' based on NDVI values
        cluster_mean_ndvi = [mean_ndvi_vals[labels == i].mean() for i in range(n_clusters)]
        tree_cluster_idx = np.argmax(cluster_mean_ndvi)

        # Test
        print("Cluster mean NDVI values:", cluster_mean_ndvi)
        print("Index of tree cluster:", tree_cluster_idx)

        # Assign class labels based on the cluster with higher NDVI being 'tree'
        gdf['class'] = gdf['cluster'].apply(lambda x: 1 if x == tree_cluster_idx else 0)

        # Dissolve polygons by 'class' to merge connected polygons
        dissolved_gdfs = []
        for cls in tqdm(gdf['class'].unique(), desc="Dissolving polygons by class"):
            class_gdf = gdf[gdf['class'] == cls]
            dissolved_gdf = class_gdf.dissolve()
            dissolved_gdf['class'] = cls
            dissolved_gdfs.append(dissolved_gdf)

        # Combine the dissolved GeoDataFrames
        dissolved_gdf = gpd.GeoDataFrame(pd.concat(dissolved_gdfs, ignore_index=True), crs=sr)

        # Plot Classified Clusters (Tree vs Not Tree)
        classified_img = np.zeros_like(ndvi)
        for shp, cls in zip(polys, labels):
            mask = rasterio.features.geometry_mask([shp], transform=affine, invert=True, out_shape=classified_img.shape)
            classified_img[mask] = cls
        plt.imshow(classified_img, cmap='gray')
        plt.title("Classified Clusters (Tree vs Not Tree)")
        plt.axis('off')
        plt.savefig(f"{plot_path}_classified_clusters.png")
        plt.close()

    return dissolved_gdf


def plot_binary_gdf(dissolved_gdf, filepath=None, save_png_file=False):
    # Add a new column for categorical labels
    dissolved_gdf['category'] = dissolved_gdf['class'].map({1: 'Tree', 0: 'Not Tree'})

    fig, ax = plt.subplots(figsize=(10, 10))

    # Remove axis labels, ticks, and tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)

    dissolved_gdf.plot(column='category',
                       ax=ax, legend=True, cmap='viridis',
                       legend_kwds={'title': "Class"})
    plt.title("Classified Clusters (Tree and Not Tree)")

    if save_png_file:
        plt.savefig(filepath)

    plt.show()


# Convert multipolygons to individual polygons
def multipolygons_to_polygons(dissolved_gdf):
    polygons = []
    classes = []
    for idx, row in dissolved_gdf.iterrows():
        if isinstance(row.geometry, MultiPolygon):
            for poly in row.geometry.geoms:  # Corrected line
                polygons.append(poly)
                classes.append(row['class'])
        else:
            polygons.append(row.geometry)
            classes.append(row['class'])
    return gpd.GeoDataFrame({'geometry': polygons, 'class': classes}, crs=dissolved_gdf.crs)


def classless_multipolygons_to_polygons(gdf):
    polygons = []
    for idx, row in gdf.iterrows():
        if isinstance(row.geometry, MultiPolygon):
            for poly in row.geometry.geoms:
                polygons.append(poly)
        else:
            polygons.append(row.geometry)
    return gpd.GeoDataFrame({'geometry': polygons}, crs=gdf.crs)


# Calculate area
def calculate_area(gdf):
    gdf['area_feet'] = gdf.geometry.area
    gdf['area_acres'] = gdf['area_feet'] / 43560
    return gdf


# Function to bin and plot the areas
def bin_plot(gdf, bins, labels, title, filepath=None, save_png_file=False):
    gdf['bin'] = pd.cut(gdf['area_acres'], bins=bins, labels=labels, right=False)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # Remove axis labels, ticks, and tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)

    plot = gdf.plot(column='bin', ax=ax, legend=True, categorical=True, legend_kwds={'title': 'Size Category'})
    # plot = gdf.plot(column='bin', ax=ax, legend=True, categorical=True, 
    #                 legend_kwds={'title': 'Size Category'}, edgecolor='black')
    ax.set_title(title)
    plt.tight_layout()
    filename = title.split('.')[0]

    if save_png_file:
        plt.savefig(filepath)
    
    plt.show()


def plot_gdf(gdf, title, filepath=None, save_png_file=False):
    fig, ax = plt.subplots(figsize=(10, 10))
    # Remove axis labels, ticks, and tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    gdf.plot(ax=ax, color='lightblue', edgecolor='black')
    plt.title(title)

    if save_png_file:
        plt.savefig(filepath)

    plt.show()


def get_bounds_gdf(geotiff_path):
    tile = rasterio.open(geotiff_path)
    bounds = tile.bounds
    minx, miny, maxx, maxy = bounds
    bounds_poly = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])
    gdf = gpd.GeoDataFrame(geometry=[bounds_poly], crs=tile.crs)
    return gdf


def apply_buffer(canopy_gdf, bounds_gdf, buffer_size=5):
    """
    Creates two GeoDataFrames: one for buffered canopy polygons and one for open space polygons.

    Parameters:
    - canopy_gdf: GeoDataFrame containing canopy polygons.
    - bounds_gdf: GeoDataFrame containing the bounds to clip the buffered canopy polygons.
    - buffer_size: The size of the buffer to apply to the canopy polygons (default is 5 feet).

    Returns:
    - buffered_gdf: GeoDataFrame containing buffered canopy polygons.
    - openspace_gdf: GeoDataFrame containing open space polygons.
    """

    # Buffer the canopy polygons by the specified buffer size
    canopy_buffer = canopy_gdf.buffer(buffer_size)

    # Create a GeoDataFrame from the buffered canopy polygons
    buffered_gdf = gpd.GeoDataFrame(geometry=canopy_buffer, crs=canopy_gdf.crs)

    # Clip the buffered canopy polygons to the original bounds
    canopy_buffer_clipped = gpd.clip(buffered_gdf, bounds_gdf)

    # Create a unary union of the clipped buffer polygons
    buffer_union = unary_union(canopy_buffer_clipped.geometry)

    # Invert the buffer to get the open space polygons
    openspace_polygons = bounds_gdf.geometry.difference(buffer_union)

    # Create a GeoDataFrame for the open space polygons
    openspace_gdf = gpd.GeoDataFrame(geometry=openspace_polygons, crs=bounds_gdf.crs)

    return buffered_gdf, openspace_gdf
