import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import os
import matplotlib.patches as mpatches
import seaborn as sns

mpl.rcParams["figure.figsize"] = (3.5, 2.625)

sns.set_context("paper", rc={"font.size": 8,"axes.titlesize": 8,
                             "axes.labelsize": 8, "xtick.labelsize": 7,
                             "ytick.labelsize": 7, "legend.fontsize": 7})
sns.set_style("whitegrid")

NEW_TABLEAU10 = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2','#59A14E',
                 '#EDC949','#B07AA2','#FF9DA7','#9C755F','#BAB0AC']
sns.set_palette(sns.color_palette(NEW_TABLEAU10))

markersize = 5
colors = [f"C{i}" for i in range(10)]
styles = ["o","s","v","^","D",">","<","*","h","H","+","1","2","3","4","8","p",
          "d","|","_",".",","]

AI_HBM = []
AI_DRAM = []
AI_L1 = []
AI_L2 = []
AI_L3 = []

with open(sys.argv[1], "r") as f:
    for line in f:
        if "memroofs" in line:
            linesp = line.split()
            linesp = linesp[1:]
            smemroofs = [float(a) for a in linesp]
            print("memroofs", smemroofs)
        elif "mem_roof_names" in line:
            linesp = line.strip().split("\'")
            linesp = filter(lambda a: (a != " ") and (a != ""), linesp)
            smem_roof_name  = list(linesp)[1:]
            print("mem_roof_names", smem_roof_name)
        elif "comproofs" in line:
            scomproofs  = [float(a) for a in line.split()[1:]]
            print("comproofs", scomproofs)
        elif "comp_roof_names" in line:
            linesp = line.strip().split("\'")
            linesp = filter(lambda a: (a != " ") and (a != ""), linesp)
            scomp_roof_name  = list(linesp)[1:]
            print("comp_roof_names", scomp_roof_name)
        elif "AI_HBM" in line:
            AI_HBM = [float(a) for a in line.split()[1:]]
            print("AI_HBM", AI_HBM)
        elif "AI_DRAM" in line:
            AI_DRAM = [float(a) for a in line.split()[1:]]
            print("AI_DRAM", AI_DRAM)
        elif "AI_L3" in line:
            AI_L3 = [float(a) for a in line.split()[1:]]
            print("AI_L3", AI_L3)
        elif "AI_L2" in line:
            AI_L2 = [float(a) for a in line.split()[1:]]
            print("AI_L2", AI_L2)
        elif "AI_L1" in line:
            AI_L1 = [float(a) for a in line.split()[1:]]
            print("AI_L1", AI_L1)
        elif "FLOPS" in line:
            FLOPS = [float(a) for a in line.split()[1:]]
            print("FLOPS", FLOPS)
        elif "labels" in line:
            labels = [label for label in line.strip().split("\'")
                      if label != " " and label != ""][1:]
            print("labels", labels)


fig = plt.figure(1)
plt.clf()
ax = fig.gca()
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Arithmetic Intensity [FLOPs/Byte]")
ax.set_ylabel("Performance [GFLOP/s]")

nx = 10000
xmin = -2
xmax = 3
ymin = 100.0
ymax = 20000

ax.set_xlim(10**xmin, 10**xmax)
ax.set_ylim(ymin, ymax)

ixx = int(nx*0.02)
xlim = ax.get_xlim()
ylim = ax.get_ylim()

scomp_x_elbow = []
scomp_ix_elbow = []
smem_x_elbow = []
smem_ix_elbow = []

x = np.logspace(xmin,xmax,nx)
for roof in scomproofs:
    for ix in range(1,nx):
        if smemroofs[0] * x[ix] >= roof and smemroofs[0] * x[ix-1] < roof:
            scomp_x_elbow.append(x[ix-1])
            scomp_ix_elbow.append(ix-1)
            break


for roof in smemroofs:
    for ix in range(1,nx):
        if (scomproofs[0] <= roof * x[ix] and scomproofs[0] > roof * x[ix-1]):
            smem_x_elbow.append(x[ix-1])
            smem_ix_elbow.append(ix-1)
            break

for i in range(0,len(scomproofs)):
    roof = scomproofs[i]
    y = np.ones(len(x)) * roof
    ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c="k",ls="-")

for i in range(0,len(smemroofs)):
    roof = smemroofs[i]
    y = x * roof
    ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c="k",ls="-")


marker_handles = list()

for i, AI in enumerate(AI_L1):
    ax.plot(float(AI),float(FLOPS[i]),c=colors[0],marker=styles[i],
            linestyle="None",ms=markersize,label=labels[i])
if AI_L1:
    ax.plot(AI_L1,FLOPS,c=colors[0],linestyle="-")

for i, AI in enumerate(AI_L2):
    ax.plot(float(AI),float(FLOPS[i]),c=colors[1],marker=styles[i],
            linestyle="None",ms=markersize,label=labels[i])
if AI_L2:
    ax.plot(AI_L2,FLOPS,c=colors[1],linestyle="-")

for i, AI in enumerate(AI_L3):
    ax.plot(float(AI),float(FLOPS[i]),c=colors[2],marker=styles[i],
            linestyle="None",ms=markersize,label=labels[i])
if AI_L3:
    ax.plot(AI_L3,FLOPS,c=colors[2],linestyle="-")

for i, AI in enumerate(AI_HBM):
    ax.plot(float(AI),float(FLOPS[i]),c=colors[2],marker=styles[i],
            linestyle="None",ms=markersize,label=labels[i])
    marker_handles.append(ax.plot([],[],c="gray",marker=styles[i],linestyle="None",ms=markersize,label=labels[i])[0])
if AI_HBM:
    ax.plot(AI_HBM,FLOPS,c=colors[2],linestyle="-")

for i, AI in enumerate(AI_DRAM):
    ax.plot(float(AI),float(FLOPS[i]),c=colors[3],marker=styles[i],
            linestyle="None",ms=markersize,label=labels[i])
    marker_handles.append(ax.plot([],[],c="gray",marker=styles[i],
                                  linestyle="None",ms=markersize,label=labels[i])[0])
if AI_DRAM:
    ax.plot(AI_DRAM,FLOPS,c=colors[3],linestyle="-")


for roof in scomproofs:
    ax.text(x[-ixx],roof,
            scomp_roof_name[scomproofs.index(roof)] + ": " + "{0:.1f}".format(float(roof)) + " GFLOP/s",
            horizontalalignment="right",
            verticalalignment="bottom")

for roof in smemroofs:
    ang = np.arctan(np.log10(xlim[1]/xlim[0]) / np.log10(ylim[1]/ylim[0])
                    * fig.get_size_inches()[1]/fig.get_size_inches()[0] )
    if x[ixx]*roof >ymin:
        ax.text(x[ixx],x[ixx]*roof*(1+0.25*np.sin(ang)**2)*1.2,
                smem_roof_name[smemroofs.index(roof)] + ": " + "{0:.1f}".format(float(roof)) + " GB/s",
                horizontalalignment="left",
                verticalalignment="bottom",
                rotation=180/np.pi*ang)
    else:
        ymin_ix_elbow = []
        ymin_x_elbow = []
        for ix in range(1,nx):
            if (ymin <= roof * x[ix] and ymin > roof * x[ix-1]):
                ymin_x_elbow.append(x[ix-1])
                ymin_ix_elbow.append(ix-1)
                break
        ax.text(x[ixx+ymin_ix_elbow[0]],x[ixx+ymin_ix_elbow[0]] *roof*(1+0.25*np.sin(ang)**2)*1.2,
                smem_roof_name[smemroofs.index(roof)] + ": " + "{0:.1f}".format(float(roof)) + " GB/s",
                horizontalalignment="left",
                verticalalignment="bottom",
                rotation=180/np.pi*ang)


leg1 = plt.legend(handles = marker_handles,loc="lower right")
ax.add_artist(leg1)

patch_handles = []
for i in range(len(smem_roof_name)):
    patch_handles.append(mpatches.Patch(color=colors[i], label=smem_roof_name[i]))

leg2 = plt.legend(handles=patch_handles, loc="lower right",
                  bbox_to_anchor=(0.75,0), scatterpoints=1)

# ax.text(xlim[0]*1.1,ylim[1]/1.1,"EPYC 7742",horizontalalignment="left",verticalalignment="top")

plt.savefig(sys.argv[2], bbox_inches="tight", pad_inches=0)
