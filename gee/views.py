from django.shortcuts import render

# generic base view
from django.views.generic import TemplateView 


#folium
import folium
from folium import plugins


#gee
import ee

ee.Initialize()


#home
class home(TemplateView):
    template_name = 'index.html'

    # Define a method for displaying Earth Engine image tiles on a folium map.
    def get_context_data(self, **kwargs):

        figure = folium.Figure()
        
        #create Folium Object
        m = folium.Map(
            location=[-0.3131, 37.34495724],
            zoom_start=10
        )
        
        #add map to figure
        m.add_to(figure)

        
        #select the Dataset Here's used the MODIS data
        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                  .filter(ee.Filter.date('2022-03-01', '2022-05-30'))
                  .first())
        modisndvi = dataset.select('NDVI')
        modisevi = dataset.select('EVI')

        #Styling 
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        vis_paramsEVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301']}

        
        #add the map to the the folium map
        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
        map_id_dict2 = ee.Image(modisevi).getMapId(vis_paramsEVI)
       
        #GEE raster data to TileLayer
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'NDVI',
                    overlay = True,
                    control = True
                    ).add_to(m)
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict2['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'EVI',
                    overlay = True,
                    control = True
                    ).add_to(m)
        
        #add Layer control
        m.add_child(folium.LayerControl())
       
        #figure 
        figure.render()
         
        #return map
        return {"map": figure}