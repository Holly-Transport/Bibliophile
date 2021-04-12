import requests

class MapQuery:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"

    def query(self, key, value, location):
        self.key = key
        self.value = value
        self.location = location
        self.overpass_query = f"""
        [out:json];
        area({self.location});
        (node[{self.key}={self.value}](area);
         way[{self.key}={self.value}](area);
         relation[{self.key}={self.value}](area);
        );
        out geom;
        """
        self.response = requests.get(self.overpass_url, params={'data': self.overpass_query})
        self.data = self.response.json()
        return self.data

    def series(self, data, value):
        self.name = []
        self.type = []
        self.web = []
        self.lat = []
        self.lon = []
        self.data = data
        self.value = value

        for i in range (0,len(self.data['elements'])):
            try:
                self.name.append(self.data['elements'][i]['tags']['name'])
            except:
                self.name.append("n/a")
            self.type.append(value)
            self.lat.append(self.data['elements'][i]['lat'])
            self.lon.append(self.data['elements'][i]['lon'])
            try:
                self.web.append(self.data['elements'][i]['tags']['website'])
            except:
                self.web.append("n/a")
        return self.name, self.type, self.web, self.lat, self.lon

#----TESTING CODE----#

# key = "shop"
# value = "books"
# location = "3605396194"
# osm = MapQuery()
# data = osm.query(key, value, location)
# print (data)
# print (osm.series (data, key))

# for i in range (0,len (data_series[0])):
    # print (f"***{data_series[0][i]}, {data_series[1][i]}, {data_series[2][i]}, {data_series[3][i]}***")




