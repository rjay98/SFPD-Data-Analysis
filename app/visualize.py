"""
Visualize.py
------------
Contains all of the visualization code to generate graphs.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import Image

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

def main():
  """
  This function generates all of the image outputs.
  """
  heatplot()

if __name__=="__main__":
  main()