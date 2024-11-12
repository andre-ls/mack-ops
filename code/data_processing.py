import json
import numpy as np
import pandas as pd
import geopy.distance

def readData():
  return pd.read_csv('../data/raw/Tornado_Tracks.csv')

def filterOldMagnitude(data):
  return data[data['fc'] == 0]

def filterColumns(data):
  return data.drop(['OBJECTID','om','yr','mo','dy','stf','stn','Month_Calc','Date_Calc','Shape__Length','fc'],axis=1)

def formatDateColumn(data):
  data['Date'] = pd.to_datetime(data['date'])
  return data.drop(['date','time','tz'],axis=1)

def renameColumns(data):
  names = {
      "st" : "State",
      "mag" : "Magnitude",
      "inj" : "Injuries",
      "fat" : "Fatalities",
      "loss" : "Property_Loss",
      "closs" : "Crop_Loss",
      "slat" : "Start_Latitude",
      "slon" : "Start_Longitude",
      "elat" : "End_Latitude",
      "elon" : "End_Longitude",
      "len" : "Length",
      "wid" : "Width",
      "fc" : "EF Scale"
  }

  return data.rename(columns=names)

def convertYardsToMeters(data):
  data['Length'] = data['Length'].apply(lambda x: x*0.9144)
  data['Width'] = data['Width'].apply(lambda x: x*0.9144)
  return data

def getStateNames(data):
  us_state_abbrev = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming',
            'DC': 'District of Columbia',
            'MP': 'Northern Mariana Islands',
            'PW': 'Palau',
            'PR': 'Puerto Rico',
            'VI': 'Virgin Islands',
            'AA': 'Armed Forces Americas (Except Canada)',
            'AE': 'Armed Forces Africa/Canada/Europe/Middle East',
            'AP': 'Armed Forces Pacific'
        }

  return data.replace({"State": us_state_abbrev})

def calculateDistanceFromLatLong(slat,slon,elat,elon):
  return geopy.distance.geodesic((slat,slon),(elat,elon)).km

def calculateDistance(data):
  data['Distance'] = data.apply(lambda x: calculateDistanceFromLatLong(x['Start_Latitude'],x['Start_Longitude'],x['End_Latitude'],x['End_Longitude']),axis=1)
  return data

def getCentralCoordinates(data):
  us_states_coordinates = {
    "Alabama": {"latitude": 32.806671, "longitude": -86.791130},
    "Alaska": {"latitude": 61.370716, "longitude": -152.404419},
    "Arizona": {"latitude": 33.729759, "longitude": -111.431221},
    "Arkansas": {"latitude": 34.969704, "longitude": -92.373123},
    "California": {"latitude": 36.116203, "longitude": -119.681564},
    "Colorado": {"latitude": 39.059811, "longitude": -105.311104},
    "Connecticut": {"latitude": 41.597782, "longitude": -72.755371},
    "Delaware": {"latitude": 39.318523, "longitude": -75.507141},
    "Florida": {"latitude": 27.766279, "longitude": -81.686783},
    "Georgia": {"latitude": 33.040619, "longitude": -83.643074},
    "Hawaii": {"latitude": 21.094318, "longitude": -157.498337},
    "Idaho": {"latitude": 44.240459, "longitude": -114.478828},
    "Illinois": {"latitude": 40.349457, "longitude": -88.986137},
    "Indiana": {"latitude": 39.849426, "longitude": -86.258278},
    "Iowa": {"latitude": 42.011539, "longitude": -93.210526},
    "Kansas": {"latitude": 38.526600, "longitude": -96.726486},
    "Kentucky": {"latitude": 37.668140, "longitude": -84.670067},
    "Louisiana": {"latitude": 31.169546, "longitude": -91.867805},
    "Maine": {"latitude": 44.693947, "longitude": -69.381927},
    "Maryland": {"latitude": 39.063946, "longitude": -76.802101},
    "Massachusetts": {"latitude": 42.230171, "longitude": -71.530106},
    "Michigan": {"latitude": 43.326618, "longitude": -84.536095},
    "Minnesota": {"latitude": 45.694454, "longitude": -93.900192},
    "Mississippi": {"latitude": 32.741646, "longitude": -89.678696},
    "Missouri": {"latitude": 38.456085, "longitude": -92.288368},
    "Montana": {"latitude": 46.921925, "longitude": -110.454353},
    "Nebraska": {"latitude": 41.125370, "longitude": -98.268082},
    "Nevada": {"latitude": 38.313515, "longitude": -117.055374},
    "New Hampshire": {"latitude": 43.452492, "longitude": -71.563896},
    "New Jersey": {"latitude": 40.298904, "longitude": -74.521011},
    "New Mexico": {"latitude": 34.840515, "longitude": -106.248482},
    "New York": {"latitude": 42.165726, "longitude": -74.948051},
    "North Carolina": {"latitude": 35.630066, "longitude": -79.806419},
    "North Dakota": {"latitude": 47.528912, "longitude": -99.784012},
    "Ohio": {"latitude": 40.388783, "longitude": -82.764915},
    "Oklahoma": {"latitude": 35.565342, "longitude": -96.928917},
    "Oregon": {"latitude": 44.572021, "longitude": -122.070938},
    "Pennsylvania": {"latitude": 40.590752, "longitude": -77.209755},
    "Rhode Island": {"latitude": 41.680893, "longitude": -71.511780},
    "South Carolina": {"latitude": 33.856892, "longitude": -80.945007},
    "South Dakota": {"latitude": 44.299782, "longitude": -99.438828},
    "Tennessee": {"latitude": 35.747845, "longitude": -86.692345},
    "Texas": {"latitude": 31.054487, "longitude": -97.563461},
    "Utah": {"latitude": 40.150032, "longitude": -111.862434},
    "Vermont": {"latitude": 44.045876, "longitude": -72.710686},
    "Virginia": {"latitude": 37.769337, "longitude": -78.169968},
    "Washington": {"latitude": 47.400902, "longitude": -121.490494},
    "West Virginia": {"latitude": 38.491226, "longitude": -80.954456},
    "Wisconsin": {"latitude": 44.268543, "longitude": -89.616508},
    "Wyoming": {"latitude": 42.755966, "longitude": -107.302490},
    "Puerto Rico": {"latitude": 18.220833, "longitude": -66.590149},
    "Virgin Islands": {"latitude": 18.335765, "longitude": -64.896335}
  }

  data['State_Central_Latitude'] =data['State'].map({k:v['latitude'] for k,v in us_states_coordinates.items()})
  data['State_Central_Longitude'] =data['State'].map({k:v['longitude'] for k,v in us_states_coordinates.items()})
  return data

def saveData(data):
    data.to_csv('../data/processed/tornado_processed_data.csv')

if __name__ == "__main__":
    data = readData()
    data = filterOldMagnitude(data)
    data = filterColumns(data)
    data = formatDateColumn(data)
    data = renameColumns(data)
    data = convertYardsToMeters(data)
    data = getStateNames(data)
    data = calculateDistance(data)
    data = getCentralCoordinates(data)
    saveData(data)
