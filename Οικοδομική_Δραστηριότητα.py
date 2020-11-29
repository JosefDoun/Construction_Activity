import os, re, tabula
import pandas as pd, matplotlib.pyplot as plt, numpy as np, matplotlib.cm as cm

pd.options.display.max_columns = 100
folder_files = os.listdir()

margins = ["^[ΝΙΠ ]?.* ?(ΘΕΣΣΑΛΟΝΙΚΗΣ)$", "^[ΝΙΠ ]?.* ?(ΚΙΛΚΙΣ)$", "^[ΝΙΠ ]?.* (Θεσσαλονίκης)$", "^[ΝΙΠ ]?.* (Κιλκίς)$"]

mc = {
    "Δ.Ε. Αγίου Αθανάσιου": ["Αγχιάλου",
                             "Ξηροχωρίου",
                             "Αγίου Αθανασίου",
                             "Γεφύρας",
                             "Μεσημβρίας",
                             "Βαθυλάκκου"],
    "Δ.Ε. Αξιού": ["Βραχιάς",
                   "Κυμίνων",
                   "Μαλγάρων"],
    "Δ.Ε. Εχέδωρου": ["Διαβατών",
                      "Καλοχωρίου",
                      "Μαγνησίας",
                      "Σίνδου"],
    "Δ.Ε. Καλλιθέας": ["Μεσαίου",
                       "Φιλαδελφείας",
                       "Νεοχωρούδας",
                       "Πενταλόφου"],
    "Δ.Ε. Κουφαλιών": ["Κουφαλίων",
                       "Προχώματος"],
    "Δ.Ε. Μυγδονίας": ["Μελισσοχωρίου",
                       "Δρυμού",
                       "Λητής"],
    "Δ.Ε. Χαλάστρας": ["Ανατολικού",
                       "Χαλάστρας"],
    "Δ.Ε. Χαλκηδόνος": ["Ελεούσης",
                        "Παρθενίου",
                        "Βαλτοχωρίου",
                        "Αδένδρου",
                        "Χαλκηδόνος",
                        "Μοναστηρίου"],
    "Δ.Ε. Ωραιοκάστρου": ["Ωραιοκάστρου"]
}

data = {
    "regex": [],
    "Δημοτικές/Τοπικές Κοινότητες": []
}


def data_population(dict):
    for key in dict:
        for value in dict[key]:
            data["Δημοτικές/Τοπικές Κοινότητες"].append(value)
            value = re.sub("[αειουωηάέίόύώή]", ".", value)
            value = str(".* ?" + value + "$")
            data["regex"].append(value)
    return


data_population(mc)

for file in folder_files:
    if re.search("\.xls.*$", file):
        try:
            year = re.search("_\d\d\d\d_", file).group()[1:-1]
            file = pd.read_excel(file)
            column0, column1 = file.columns[0], file.columns[1]
            file[column0] = file[column0].str.strip()
            try:
                start, end = file.loc[file[column0].str.match(margins[0], na=False)].index[0], \
                             file.loc[file[column0].str.match(margins[1], na=False)].index[0]
            except:
                start, end = file.loc[file[column0].str.match(margins[2], na=False)].index[0], \
                             file.loc[file[column0].str.match(margins[3], na=False)].index[0]
            data[year] = []
            count = 0
            for regex_value in data["regex"]:
                count += 1
                real_value = data["Δημοτικές/Τοπικές Κοινότητες"][data["regex"].index(regex_value)]
                criterion = file[column0].str.match(regex_value, na=False)[start:end]
                if criterion.any():
                    index_list = file[start:end][column0].loc[criterion].index
                    if len(index_list) > 1:
                        print(year, real_value, "Multiple Values Error")
                        print(file.iloc[index_list[0:2]])
                        print("for regex: ", regex_value)
                        break
                    else:
                        index = index_list[0]
                    if file.at[index, column1] != file.at[index, column1] and \
                            file.at[index + 1, column1] == file.at[index + 1, column1]:
                        while file.at[index, column1] != file.at[index, column1] or not str(
                                file.at[index, column1]).isnumeric():
                            try:
                                data[year].append(int(file.at[index, column1]))
                                break
                            except ValueError:
                                index -= 1
                    elif file.at[index, column1] != file.at[index, column1] and \
                            file.at[index + 1, column1] != file.at[index + 1, column1]:
                        while file.at[index, column1] != file.at[index, column1] or not str(
                                file.at[index, column1]).isnumeric():
                            try:
                                data[year].append(int(file.at[index, column1]))
                                break
                            except ValueError:
                                index += 1
                    data[year].append(int(file.at[index, column1]))
                else:
                    data[year].append(0)
        except Exception as e:
            print(year, real_value, "[{}/31]\n".format(count), e)
            break
    elif re.search("\.pdf$", file):
        try:
            year = re.search("_\d\d\d\d_", file).group()[1:-1]
            file = tabula.read_pdf(file, pages='all')
            tables = (table for table in file)
            file = pd.concat(tables, ignore_index=True)
            column0, column1 = file.columns[0], file.columns[1]
            file[column0] = file[column0].str.strip()
            try:
                start, end = file.loc[file[column0].str.match(margins[0], na=False)].index[0], \
                             file.loc[file[column0].str.match(margins[1], na=False)].index[0]
            except:
                start, end = file.loc[file[column0].str.match(margins[2], na=False)].index[0], \
                             file.loc[file[column0].str.match(margins[3], na=False)].index[0]
            data[year] = []
            count = 0
            for regex_value in data["regex"]:
                count += 1
                real_value = data["Δημοτικές/Τοπικές Κοινότητες"][data["regex"].index(regex_value)]
                criterion = file[column0].str.match(regex_value, na=False)[start:end]
                if criterion.any():
                    index_list = file[start:end][column0].loc[criterion].index
                    if len(index_list) > 1:
                        print(year, real_value, "Multiple Associated Values Error")
                        print(file.iloc[index_list[0:2]])
                        print("for regex: ", regex_value)
                        break
                    else:
                        index = index_list[0]
                    # NaN handling - Non numeric Str handling
                    if file.at[index, column1] != file.at[index, column1] and \
                            file.at[index + 1, column1] == file.at[index + 1, column1]:
                        while file.at[index, column1] != file.at[index, column1] or not \
                                file.at[index, column1].isnumeric():
                            try:
                                data[year].append(int(file.at[index, column1]))
                                break
                            except ValueError:
                                index -= 1
                    elif file.at[index, column1] != file.at[index, column1] and \
                            file.at[index + 1, column1] != file.at[index + 1, column1]:
                        while file.at[index, column1] != file.at[index, column1] or not \
                                file.at[index, column1].isnumeric():
                            try:
                                data[year].append(int(file.at[index, column1]))
                                break
                            except ValueError:
                                index += 1

                    data[year].append(int(file.at[index, column1]))
                else:
                    data[year].append(0)
        except Exception as e:
            print(year, real_value, "[{}/31]\n".format(count), e)
            print(file.loc[index - 6:index + 6])
            break

    else:
        continue

del data["regex"]

data = pd.DataFrame(data,
                    columns=tuple(data.keys())[1:],
                    index=data[tuple(data.keys())[0]])

# Group to Municipal Units and create excel
data = pd.DataFrame([data.loc[mc[key]].sum(axis=0) for key in mc], index=tuple(mc.keys()), columns=data.columns)
x1ticklabels = data.sum(axis=0)
print(data)
data = data.divide(data.sum(axis=0), axis=1) * 100
data.to_excel("Οικοδομική_δραστηριότητα_Διπλωματική.xls", columns=data.columns)

fig = plt.figure(num=1, facecolor=(0.92, 0.9, 0.9, 0.5), edgecolor='k', linewidth=5, dpi=100)
fig.suptitle("Ετήσια και μέση ετήσια κατανομή εκδοθεισών οικοδομικών αδειών νέων οικοδομών - Οικοδομικό ενδιαφέρον",
             fontsize=18,
             linespacing=1.5, x=0.5)
ax1 = fig.add_subplot(2, 1, 1,
                      ylabel='Σύνολο ετήσιων αδειών',
                      facecolor=(0.85, 0.85, 0.85, 0.5))
ax1.yaxis.set_label_position('right')
ax1.xaxis.set_label_position('top')
ax2 = fig.add_subplot(2, 1, 2)
ax_cbar = fig.add_axes([0.92, 0.1, 0.01, 0.755], title='')
cmap = cm.get_cmap('Spectral_r')

ax1.xaxis.set_visible(True)
ax1.xaxis.set_ticks_position('top')
ax1.xaxis.set(ticks=np.arange(0, len(data.columns), 1), ticklabels=x1ticklabels)
ax1.yaxis.set(ticks=(7, 15, 26, 38, 47, 55, 62, 69, 85, 100), ticklabels=(data.index))
ax1.set_yticklabels(labels=data.index, fontsize=14)
ax1.set_xticklabels(labels=x1ticklabels, fontsize=14)
ax1.set_ylabel(ylabel="<-  Ποσοστιαίο σύνολο  -> \n ετήσιων αδειών", fontsize=14)
ax1.set_xlabel(xlabel="Άθροισμα ετήσιων οικοδομικών αδειών", fontsize=13)
ax1.set_xlim(-0.5, len(data.columns) - 0.5)
ax1.set_ylim(0, 100)
ax1.grid(color='k', linestyle=':', linewidth=0.6, axis='x')
ax1.spines['bottom'].set(linewidth=6, color='red')

plot2 = ax2.pcolormesh(data.values, cmap=cmap, alpha=0.9, shading='flat')
ax2.xaxis.set(ticks=np.arange(0.5, len(data.columns), 1), ticklabels=data.columns)
ax2.set_ylabel(ylabel="Δημοτικές Ενότητες", fontsize=14)
ax2.set_yticklabels(labels=data.index, horizontalalignment='right', fontsize=14)
ax2.set_xticklabels(labels=data.columns, horizontalalignment='center', fontsize=13)
ax2.yaxis.set(ticks=np.arange(0.5, len(data.index), 1), ticklabels=data.index)
ax2.grid(color='k', linestyle=':', linewidth=0.6, axis='x')
ax2.spines['top'].set(linewidth=6, color='red')

plot1 = ax1.stackplot(data.columns, data,
                      labels=data.index,
                      edgecolor='k',
                      linewidth=0.2,
                      colors=[cmap((x / (data.max().max()))) for x in (data.sum(axis=1) / len(data.columns))],
                      alpha=0.9)

cbar = plt.colorbar(plot2, ax=ax2, cax=ax_cbar, format='%.0f%%')
cbar.set_label('Ποσοστό ετήσιων αδειών', fontsize=14)
cbar.ax.tick_params(labelsize=14)

handles, labels = ax1.get_legend_handles_labels()
# fig.legend(handles=handles[::-1], labels=labels[::-1],
#            frameon=False,
#            loc='center left',
#            bbox_to_anchor=[0.005, 0.525, 0.12, 0.35],
#            labelspacing=0.75,
#            handlelength = 1,
#            borderpad = 0,
#            fontsize=14,
#            title='Μέση ετήσια κατανομή',
#            title_fontsize = 14,
#            facecolor = (0.1,0.1,0.1,1))

fig.text(0.52, 0.03, "Πηγή: ΕΛΣΤΑΤ", ha='center', fontsize=15)

# ax1.annotate("Παράδειγμα!",
#              xy=(0, 0),
#              xycoords='data',
#              xytext=(10.5, 5),
#              textcoords='data',
#              arrowprops=dict(arrowstyle="->",
#                              connectionstyle="arc3"), )

plt.subplots_adjust(left=0.165, right=0.885, top=0.85, hspace=0, wspace=0)
plt.show()
