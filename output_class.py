
### output_class

import open_api

### this module creates each class for a output
# print statement included in the method for each class

class latlong:
    def print_info(self, json_file) -> None:
        '''
        prints latitude and longitude in a line
        in the format like 123 N 456W
       '''
        print("LATLONGS")
        for item in json_file['route']['locations']: # gets lat and long value
            lat = item['latLng']['lat']
            long = item['latLng']['lng']
            if lat < 0:
                sphere = 'S'
            else:
                sphere = 'N'
            if long < 0:
                earth = 'W'
            else:
                earth = 'E'
            # prints the correct format of statement
            # to two decimal places
            print("{:.2f}{} {:.2f}{}".format(abs(lat), sphere, abs(long), earth))
        print()


class steps:
    def print_info(self, json_file) -> None:
        '''
        prints the entire direction of the route
        '''
        print('DIRECTIONS')
        for item in json_file['route']['legs']:
            for step in item['maneuvers']:
                print(step['narrative'])
        print()

        
class total_time:
    def print_info(self, json_file) -> None:
        '''
        prints the total time needed in a route
        in the format: TOTAL TIME: 123 minutes
        '''
        time_list = []
        for item in json_file['route']['legs']:
            time_list.append(item['time'])
        time = sum(time_list) / 60 # gets the total time in minutes(integer)
        self._total_time = "TOTAL TIME: {} minutes".format(round(time))
        print(self._total_time)
        print()

        
class total_distance:
    def print_info(self, json_file) -> None:
        '''
        prints the total distance of the route
        in the format: TOTAL DISTANCE: 123 miles
        '''
        distance_list = []
        for item in json_file['route']['legs']:
            distance_list.append(item['distance'])
        total_dis = sum(distance_list)# gets total distance in miles(integer)
        print("TOTAL DISTANCE: {} miles".format(round(total_dis)))
        print()

        
class elevation:
    def print_info(self, json_file) -> None:
        '''
        prints the elevation of every location
        '''
        print('ELEVATIONS')
        latlong_list = [] # a list of dictionaries, like {'lat':12, 'lng':34}
        for item in json_file['route']['locations']:
            latlong_list.append(item['latLng'])
        new_latlong = [] # consists of several sublists: [[1, 2], [3, 4]]
        for unit in latlong_list:
            sub_list = [] # sublist: two elements [lat_value, long_value]
            sub_list.append(unit['lat'])
            sub_list.append(unit['lng'])
            new_latlong.append(sub_list)
        ele_list = []
        for every in new_latlong:
            json_obj = open_api.open_url(open_api.build_elevation_url(every))
            # gets the json object from elevation url
            for item in json_obj['elevationProfile']:
                ele_list.append(str(round(item['height'] * 3.28)).strip())
                # gets the elevation value
        for unit in ele_list:# prints every elevation value(feet) in the elevation list
            print(unit)
        print()
            
    
class copy_right:
    def print_info(self) -> None:
        '''
        prints the copyright line
        '''
        print('Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors')
