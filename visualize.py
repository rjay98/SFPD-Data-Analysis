"""
Visualize.py
------------
Contains all of the visualization code to generate graphs.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.colors import ListedColormap
import Image

def parse_time(time):
    '''
    Parses time string, returns a datetime object
    '''
    f = "%Y-%m-%d %H:%M:%S.%f"
    return datetime.strptime(time[:-4], f)

def zipcodes():
  """
  Code for generating incidents by zipcode bar chart.
  (I just saved the png, but here's the source code).
  """
  df = pd.read_csv('./data/cleaned_data.csv')
  plt.figure(figsize=(14,6))
  sns.set_style("whitegrid")
  sns.barplot(x=df.zipcode_of_incident, y=df.response_time, estimator=np.mean)
  plt.ylabel('Average Response Time (Seconds)')
  plt.xlabel('Zipcode of Incident')
  plt.savefig('static/img/zipcodes.png', format='png', transparent=True)

def heatplot():
  """
  Generates heatplot utilizing latitude and longitude.
  Duplicates high priority emergency calls for the heatmap.
  """
  df = pd.read_csv('./data/cleaned_data.csv')
  # Duplicate rows with high importance to add more weight.
  high_priority = df[df['final_priority'] == 3]
  df = pd.concat([df, high_priority], ignore_index=True) 
  plt.figure(figsize=(6,6))
  cmap=plt.cm.gist_heat_r
  my_cmap = cmap(np.arange(cmap.N))
  my_cmap[:,-1] = np.linspace(0, 1, cmap.N)
  my_cmap = ListedColormap(my_cmap)
  sns.jointplot(df.latitude, df.longitude, kind="hex", color='#FF7700', cmap=my_cmap, stat_func=None)
  plt.savefig('static/img/heatmap_no_bg.png', transparent=True)

  p = Image.open('static/img/heatmap_no_bg.png')
  pdat = p.load()
  for x in xrange(80, 480):
    for y in xrange(122, 527):
      if pdat[x, y] == (255, 255, 255, 255):
        pdat[x, y] = 255, 255, 255, 0

  canvas = Image.new('RGBA', p.size, "white")
  bg = Image.open('static/img/san_francisco_bg.png')
  # Resize background image
  size = (400, 405)
  bg = bg.resize(size, Image.ANTIALIAS)
  canvas.paste(bg, box=(80,122))
  canvas.paste(p, mask=p)
  canvas.save('static/img/heatmap_with_bg.png', transparent=False)

def increase_time():
  """
  Generates line plots based on the number of calls every day for each zipcode.
  """
  # List of all zipcodes in the dataset
  zips = [94102, 94103, 94104, 94105, 94107, 94108, 94109, 94110, 94111, 94112, 94114, 94115, 94116, 94117, 94118, 94121, 94122, 94123, 94124, 94127, 94129, 94130, 94131, 94132, 94133, 94134, 94158]

  zip_pos = {}

  for i, z in enumerate(zips):
    zip_pos[z] = i

  # representing the twelve days in the dataset
  data = [([0] * 12) for _ in range(len(zips))]

  df = pd.read_csv('./data/cleaned_data.csv')

  for _, row in df.iterrows():
    z = row.zipcode_of_incident
    day = int(row.day)
    # filter out edges of data
    if day != 25:
      data[zip_pos[z]][day-13] += 1

  x_days = list(xrange(12, 24))

  # Construct dataframe
  df = pd.DataFrame(columns=x_days, data=data)
  df = df.set_index([zips])

  df2 = df.stack().reset_index()
  df2.columns = ['Zip', 'Day', 'Call Frequency']

  plt.figure(figsize=(12, 8))
  ax = sns.pointplot(x='Day', y='Call Frequency', hue='Zip', data=df2)
  plt.show()

def process_times():
  """
  Generates a graph detailing average time in seconds for each segment of the response.
  """
  df = pd.read_csv('./data/cleaned_data.csv')
  # Evaluates rows that are parsable
  df = df.dropna(subset=['received_timestamp', 'entry_timestamp', 'dispatch_timestamp', 'response_timestamp', 'on_scene_timestamp'])

  # Stores the increments between each timestamp.
  incs = []
  for index, row in df.iterrows():
    [t0, t1, t2, t3, t4] = map(parse_time, [
      row.received_timestamp,
      row.entry_timestamp,
      row.dispatch_timestamp,
      row.response_timestamp,
      row.on_scene_timestamp])
    time_diffs = [
      (t1-t0).total_seconds(),
      (t2-t1).total_seconds(),
      (t3-t2).total_seconds(),
      (t4-t3).total_seconds()]
    incs.append(time_diffs)
  increment_names = ['Received-Entry', 'Entry-Dispatch', 'Dispatch-Response', 'Response-On_Scene']
  df2 = pd.DataFrame(columns=increment_names, data=incs)
  plt.figure(figsize=(12,6))
  ax = sns.barplot(data=df2)
  plt.show()

def main():
  """
  This function generates all of the image outputs.
  """
  process_times()

if __name__=="__main__":
  main()