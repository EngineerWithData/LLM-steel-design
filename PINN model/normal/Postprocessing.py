# Python Code for 2025 SSRC column brain paper postprocessing of figures
# 01/22/2025 by Zhidong Zhang

#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator # for plot tick formatting integer
import pandas as pd

import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\users\jhuzzd\miniconda3\envs\pythonproject\lib\site-packages\PyQt5\Qt\plugins\platforms'


# Read data into the Dataframe
df_original = pd.read_csv("final_results.csv")
df_original['Ratio'] = df_original['Predicted_Pn'] / df_original['Noise_Added_Pn']
df_original['Sigma_e'] = (df_original['I'].mul((3.1415926) * (3.1415926) * 29000) / (df_original['L']*df_original['L'])) / df_original['A']
df_original['η'] = df_original['delta_o']*df_original['c']/(df_original['I'] /df_original['A'])

# Filter the dataframe to only include the Pn from 0 t0 20000kip
df = df_original.loc[(df_original['Noise_Added_Pn'] >= 0) & (df_original['Noise_Added_Pn'] <= 20000)]
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
#X = df[features].to_numpy()
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
#max_limit = max(ax1.get_xlim()[1], ax1.get_ylim()[1])
max_limit = 20000
plt.scatter(df['Noise_Added_Pn'],df['Predicted_Pn'], s=1,c='black')
plt.plot([0,0],[max_limit, max_limit],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
ax1.set_xlim(0, max_limit)
ax1.set_ylim(0, max_limit)
ax1.set_xlim(xmin=0) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_aspect('equal')
ax1.set_xlabel("True Compressive Strength Pn (kip)",font3) # label font and size
ax1.set_ylabel("Predicted Compressive Strength Pn (kip)",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('1_True_Prediction.png', bbox_inches='tight')



# Plot Prediction-to-true ratio vs fy
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
plt.scatter(df['fy'],df['Ratio'], s=1,c='black')
plt.plot([0,1],[100000, 1],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
max_limit = df['fy'].max()
ax1.set_xlim(0, max_limit)
ax1.set_ylim(0, 1.5)
ax1.set_xlim(xmin=40) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_xlabel("Yield Strength fy (ksi)",font3) # label font and size
ax1.set_ylabel("Prediction-to-Truth Ratio",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('2_Ratio_fy.png', bbox_inches='tight')


# Plot Prediction-to-true ratio vs sigma_e
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
plt.scatter(df['Sigma_e'],df['Ratio'], s=1,c='black')
plt.plot([0,1],[100000, 1],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
max_limit = df['Sigma_e'].max()
ax1.set_xlim(0, max_limit)
ax1.set_ylim(0, 1.5)
ax1.set_xlim(xmin=0) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_xlabel("Elastic Buckling Strength σe (ksi)",font3) # label font and size
ax1.set_ylabel("Prediction-to-Truth Ratio",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('3_Ratio_Sigmae.png', bbox_inches='tight')



# Plot Prediction-to-true ratio vs η
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
plt.scatter(df['η'],df['Ratio'], s=1,c='black')
plt.plot([0,1],[100000, 1],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
max_limit = df['η'].max()
ax1.set_xlim(0, 20)
ax1.set_ylim(0, 1.5)
ax1.set_xlim(xmin=0) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_xlabel("Imperfection Factor η",font3) # label font and size
ax1.set_ylabel("Prediction-to-Truth Ratio",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('4_Ratio_Yita.png', bbox_inches='tight')



# Plot Prediction-to-true ratio vs L
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
plt.scatter(df['L'],df['Ratio'], s=1,c='black')
plt.plot([0,1],[100000, 1],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
max_limit = df['L'].max()
ax1.set_xlim(0, max_limit)
ax1.set_ylim(0, 1.5)
ax1.set_xlim(xmin=0) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_xlabel("Column Length L (inch)",font3) # label font and size
ax1.set_ylabel("Prediction-to-Truth Ratio",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('5_Ratio_Length.png', bbox_inches='tight')



# Plot Prediction-to-true ratio vs δo
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
plt.scatter(df['delta_o'],df['Ratio'], s=1,c='black')
plt.plot([0,1],[100000, 1],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
max_limit = df['delta_o'].max()
ax1.set_xlim(0, 40)
ax1.set_ylim(0, 1.5)
ax1.set_xlim(xmin=0) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_xlabel(r'$δ_{o}$',font3) # label font and size
ax1.set_ylabel("Prediction-to-Truth Ratio",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('6_Ratio_Delta_o.png', bbox_inches='tight')



# Plot Prediction-to-true ratio vs c
fig, ax1 = plt.subplots(1,1,figsize=(3.26771654, 3.26771654/6.4*4.8), dpi= 800)
# Prepare data (Stacked Area Chart)
mycolors = ['tab:blue','tab:red']      
#labs = ['True Compressive Strength Pn (kip)','Predicted Compressive Strength Pn (kip)'] 
font1 = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 10} #'Times New Roman'
font2 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 10} #'Times New Roman','normal'for weight or 'bold'
font3 = {'family' : 'Arial', 'weight' : 'normal', 'size'   : 7} #'Times New Roman','normal'for weight or 'bold'
# Plot for each time series data
ax1 = plt.gca()
features = ['Original_Pn','Noise_Added_Pn','Predicted_Pn','A','I','c','L','fy','delta_o']
plt.scatter(df['c'],df['Ratio'], s=1,c='black')
plt.plot([0,1],[100000, 1],linestyle='--', color='black') 
# Decorations
ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) # set the tick number float with one digit ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_xlim(xmax=max(dis_total_sim/9*100)) # set the x axis limit from 0
# ax1.set_ylim(ymax=129) # set the y axis limit from 0
max_limit = df['c'].max()
ax1.set_xlim(0, max_limit)
ax1.set_ylim(0, 1.5)
ax1.set_xlim(xmin=0) # set the x axis limit from 0
ax1.set_ylim(ymin=0) # set the y axis limit from 0
ax1.set_xlabel("c",font3) # label font and size
ax1.set_ylabel("Prediction-to-Truth Ratio",font3)
ax1.tick_params(labelsize=4, direction='in', length=2) # set up the tick inside the plot and size
ax1.legend(loc='upper right', prop=font3, ncol=1, frameon=False)     # number of columns the legend ncol, at lower right conor, no frame box
# plt.yticks(np.arange(0, 120, 20), fontsize=9)
# Lighten borders
plt.gca().spines["top"]
plt.gca().spines["bottom"]
plt.gca().spines["right"]
plt.gca().spines["left"]
plt.savefig('7_Ratio_c.png', bbox_inches='tight')


