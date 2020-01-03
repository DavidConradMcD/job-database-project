
import numpy as np
from collections import defaultdict
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly import tools
from scipy import stats
from collections import Counter
import glob
import os
import dash_table
# Python program to show time by process_time()
from time import process_time
from jitcache import Cache

cache = Cache()

# Start the stopwatch / counter
t1_start = process_time()





##############################################################################################
                        #### Part One: Data Cleaning ####
##############################################################################################



                #### Tab One: Skills/Certifications Assessment ####
path = "/Users/david/Desktop/Desktop/Python/job-database-project/job scrapes"
col_names = ['Job Title','Company','Location','Link','Description']
all_files = sorted(glob.glob(path + "/*.csv"))
pd.options.display.float_format = '{:,.02f}'.format

df_list = []
desc_list = []
file_order = 0
file_order_list = []

for filename in all_files:
    df1 = pd.read_csv(filename, names=col_names, header=None, sep=',').iloc[1:]
    file_order_list.append(file_order)
    df1['File order'] = file_order
    df_list.append(df1)
    file_order += 1

df = pd.concat(df_list, axis=0, ignore_index=True)
df = df[df['Description'].isna()==False]
df = df.reset_index().drop(columns=['index'])

file_order_list = df['File order']
descriptions = df['Description']
desc_list = list(descriptions)

### contains the string name for each skill
skill_names = ['Python', 'SQL', 'Java', ' R ', ' C ', 'C++', 'C#',\
              'Hadoop', 'Spark', 'Tableau', 'Sas', 'Excel', 'VBA', 'Macros', 'PowerPoint',\
              'Microsoft Word', 'D3.js', 'Matlab', 'Jasper', 'Cognos', 'ggplot2', 'Dash',\
              'Jupyter','Matplotlib','Nltk','Scikit-learn','TensorFlow','Weka','Google Analytics',\
              'JavaScript','PHP','Ruby','Swift','Bloomberg','Reuters','SPSS','TypeScript','Perl']

certifications = ['CSC','CFA','CPA','MBA','CFP','IFC','PFSA','FP I','FP II','AFP',\
                  'BCO','PLM','BMF','PTM','BDPM','WME','LIC',\
                  'IATP','IMT','AIS','NEC','CRM','ADMS','DFC','DFOL',\
                  'FLC','OLC','OPSC','CCSE','TTC','ETS','BMAP','ETFM']
### creating a dictionary that holds lists with variable names pertaining to each value in the above skill_names list ###
skill_lists = {skill_names[i]: [] for i in range(len(skill_names))}
certif_lists = {certifications[i]: [] for i in range(len(certifications))}
for i in range(len(descriptions)):
    for j in range(len(skill_names)):
        if desc_list[i].__contains__(skill_names[j]) or \
        desc_list[i].__contains__(skill_names[j].upper()) or \
        desc_list[i].__contains__(skill_names[j].lower()) or \
        desc_list[i].__contains__(' ' + skill_names[j] + ' '):
            skill_lists[skill_names[j]].append(1)
        else:
            skill_lists[skill_names[j]].append(0)

for i in range(len(descriptions)):
    for j in range(len(certifications)):
        if desc_list[i].__contains__(certifications[j]) or \
        desc_list[i].__contains__(' ' + certifications[j] + ' '):
            certif_lists[certifications[j]].append(1)
        else:
            certif_lists[certifications[j]].append(0)

skill_df = pd.DataFrame(skill_lists)
skill_df['File order'] = file_order_list
certif_df = pd.DataFrame(certif_lists)
certif_df['File order'] = file_order_list

skill_counts = {skill_names[i]: [] for i in range(len(skill_names))}
certif_counts = {certifications[i]: [] for i in range(len(certifications))}

for i in range(len(skill_counts)):
    for j in range(len(all_files)):
        skill_counts[skill_names[i]].append((skill_df[(skill_df[skill_names[i]] == 1) & (skill_df['File order'] == j)].count())[0])

for i in range(len(certif_counts)):
    for j in range(len(all_files)):
        certif_counts[certifications[i]].append((certif_df[(certif_df[certifications[i]] == 1) & (certif_df['File order'] == j)].count())[0])


graph_sort_options = ['Base Chart','Highest Percentage Change','Highest Average Value']
graph_type_options = ['Line Chart', 'Bar Chart']
skill_or_certificaiton = ['Skills','Certifications']


skill_pct_chg_list = []
skill_avg_val_list = []
for i in skill_df.columns[:-1]:
    try:
        skill_pct_chg_list.append([i,(sum((skill_df[i] == 1) & (skill_df['File order'] == 13)) - sum((skill_df[i] == 1) & (skill_df['File order'] == 0)))/(sum((skill_df[i] == 1) & (skill_df['File order'] == 0)))])
        skill_avg_val_list.append(sum(skill_counts[i])/len(all_files))
    except ZeroDivisionError as Error:
        pass
skill_roc_df = pd.DataFrame(skill_pct_chg_list, columns=['Skill','Skill % Change'])
skill_roc_df['Skill Avg Val'] = skill_avg_val_list
skill_roc_df['% Change Skill'] = skill_roc_df['Skill % Change']*100
skill_roc_df['% Skill Val'] = skill_roc_df['Skill Avg Val']/len(skill_roc_df['Skill'])
skill_pct_chg_df = skill_roc_df.sort_values(by=['% Change Skill'],ascending=False)[:5]
skill_val_chg_df = skill_roc_df.sort_values(by=['Skill Avg Val'],ascending=False)[:5]
skill_roc_df = skill_roc_df.drop(columns=['Skill % Change'])

certif_pct_chg_list = []
certif_avg_val_list = []
for i in certif_df.columns[:-1]:
    try:
        certif_pct_chg_list.append([i,(sum((certif_df[i] == 1) & (certif_df['File order'] == 13)) - sum((certif_df[i] == 1) & (certif_df['File order'] == 0)))/(sum((certif_df[i] == 1) & (certif_df['File order'] == 0)))])
        certif_avg_val_list.append(sum(certif_counts[i])/len(all_files))
    except ZeroDivisionError as Error:
        pass
certif_roc_df = pd.DataFrame(certif_pct_chg_list, columns=['Certification','Certification % Change'])
certif_roc_df['Certification Avg Val'] = certif_avg_val_list
certif_roc_df['% Change Certification'] = certif_roc_df['Certification % Change']*100
certif_roc_df['% Certification Val'] = certif_roc_df['Certification Avg Val']/len(certif_roc_df['Certification'])
certif_pct_chg_df = certif_roc_df.sort_values(by=['% Change Certification'],ascending=False)[:5]
certif_val_chg_df = certif_roc_df.sort_values(by=['Certification Avg Val'],ascending=False)[:5]
certif_roc_df = certif_roc_df.drop(columns=['Certification % Change'])


rate_chg_df = pd.concat([skill_roc_df,certif_roc_df],axis=1)
rate_chg_df.columns = ['Name','Avg. Value','% Change', 'Proportion of total', 'Name C',\
      'Avg. Value C', '% Change C', 'Proportion of total C']
rate_chg_df.round({'Avg. Value': 2, '% Change': 2, 'Proportion of total':2,
                   'Avg. Value C': 2, '% Change C': 2, 'Proportion of total C':2,})

name_list = []
for i,j in enumerate(rate_chg_df.columns):
    if i < 4:
        name_list.append({"name": j, "id": j})
    else:
        name_list.append({"name": j, "id": j})


                #### Tab Two: School Semester Assessment ####

school_df_new = pd.read_csv("/Users/david/Downloads/F19-courses w_date-time - Sheet1 (1).csv",header=[0,1])


class_list = []
for i in school_df_new.columns.levels[0]:
    class_list.append(i)

class_names = []
for i in range(len(class_list)):
    class_names.append(class_list[i][11:].strip())

classes_dict = {class_names[i]:school_df_new[class_list[i]].dropna(how='any') for i in range(len(class_names))}
for i in range(len(class_names)):
    classes_dict[class_names[i]] = classes_dict[class_names[i]].sort_values('Date',ascending=False)

for i in range(len(class_names)):
    classes_dict[class_names[i]] = classes_dict[class_names[i]].reset_index().drop(columns=['index'])

assignment_names = ['Assignment', 'assignment','Presentation','presentation','Participation','participation',\
                   'Lab', 'lab', 'Homework', 'homework']
test_names = ['Test', 'test', 'Midterm', 'midterm']
exam_names = ['Final','Final Exam','Exam','exam']

#Adding additional columns for marker organizing
marker_color = [[] for i in range(len(class_names))]
assessment_names = [[] for i in range(len(class_names))]

for i in range(len(class_names)):
    for j in range(len(classes_dict[class_names[i]]['Assessment'])):
        if classes_dict[class_names[i]]['Assessment'][j].__contains__('Presentation')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Assignment')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Participation')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Lab')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Homework')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Submission'):
            marker_color[i].append(1)
        else:
            pass
        if classes_dict[class_names[i]]['Assessment'][j].__contains__('Test')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Midterm')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('midterm')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('test'):
            marker_color[i].append(2)
        else:
            pass
        if classes_dict[class_names[i]]['Assessment'][j].__contains__('Final Exam')\
        or classes_dict[class_names[i]]['Assessment'][j].__contains__('Exam'):
            marker_color[i].append(3)
        else:
            pass


    for j in marker_color[i]:
        if j == 1:
            assessment_names[i].append('Labs/Assignments')
        else:
            pass
        if j == 2:
            assessment_names[i].append('Tests')
        else:
            pass
        if j == 3:
            assessment_names[i].append('Final Exam')
        else:
            pass

for i in range(len(class_names)):
    classes_dict[class_names[i]]['Marker Color'] = marker_color[i]
    classes_dict[class_names[i]]['Assessment Type'] = assessment_names[i]

for i in range(len(class_names)):
    classes_dict[class_names[i]]['Date'] = pd.to_datetime(classes_dict[class_names[i]]['Date'], format='%m/%d/%Y')

for i in range(len(class_names)):
    classes_dict[class_names[i]] = classes_dict[class_names[i]].sort_values('Date',ascending=True)


class_stat_list = [{val:[]} for idx,val in enumerate(class_names)]
weighted_avg_list = [[] for i in range(len(class_names))]
for idx,val in enumerate(class_names):
    class_stat_list[idx][val] = classes_dict[val].reset_index().iloc[:,2:4]

for i in range(len(class_stat_list)):
    for j in range(len(class_stat_list[i][class_names[i]]['Grade'])):
        weighted_avg_list[i].append(sum(class_stat_list[i][class_names[i]]['Grade'][0:j+1] * \
                                     class_stat_list[i][class_names[i]]['Weight'][0:j+1])\
                                 /sum(class_stat_list[i][class_names[i]]['Weight'][0:j+1]))

for i in range(len(class_names)):
    classes_dict[class_names[i]] = classes_dict[class_names[i]].reset_index().drop(columns=['index'])

for i in range(len(class_names)):
    classes_dict[class_names[i]]['Weighted Avg'] = weighted_avg_list[i]



color_list = ['rgb(31, 119, 180)',
             'rgb(255, 127, 14)',
             'rgb(44, 160, 44)',
             'rgb(214, 39, 40)',
             'rgb(148, 103, 189)',
             'rgb(140, 86, 75)',
             'rgb(227, 119, 194)',
             'rgb(127, 127, 127)',
             'rgb(188, 189, 34)',
             'rgb(23, 190, 207)']


base_skill_values = skill_names[0:6]
def create_initial_graph(base_skill_values):
    traces = []

    for i in range(len(base_skill_values)):
        traces.append(go.Scatter(x = date_range,
                           y = skill_counts[base_skill_values[i]],
                           line=go.scatter.Line(
                            shape="spline",
                            smoothing = 1.0),
                           name = base_skill_values[i]))

    data = traces
    layout = go.Layout(
                  title='Skills mentioned in job postings (August to December)',hovermode='closest',
                  showlegend = True,
                  legend= {'itemsizing': 'constant'},
                  xaxis_title="Weekly scrape of Indeed job postings",
                  yaxis_title="# of mentions",
                  height = 400,
                  font=dict(
                    family="Courier New, monospace",
                    size=11,
                    color="#7f7f7f"),
                  margin=go.layout.Margin(
                      l=3,
                      r=3,
                      b=60,
                      t=50,
                      pad=1
                      ),
                  )

    fig = go.Figure(data=data,layout=layout)


    return fig


base_skill_bar_vals = skill_names[:]
def initial_bar_chart(base_skill_bar_vals):
    bar_width = 0.5

    traces = []
    for j in range(len(base_skill_bar_vals)):
        traces.append(go.Bar(
           x = [list(skill_counts.keys())[j]],
           y = [np.mean(skill_counts[base_skill_bar_vals[j]])],
           width=[bar_width],
           name = list(skill_counts.keys())[j],
           marker_color= color_list[1],
           ))

    data = traces

    layout = go.Layout(
      title='Skills Average Value',
      hovermode='closest',
      showlegend=False, legend= {'itemsizing': 'constant'},
      height = 225,
      font=dict(
        family="Courier New, monospace",
        size=11,
        color="#7f7f7f"),
      xaxis = {'automargin': True, 'title': 'Skill'},
      yaxis = {'automargin': True, 'title': 'Count'},
      margin=go.layout.Margin(
          l=2,
          r=2,
          b=90,
          t=30,
          pad=1
          ),
      )

    fig = go.Figure(data=data,layout=layout)


    return fig



def create_tab2_graph(classes_dict):
    fig = make_subplots(rows=1, cols=5,
                   subplot_titles=([i for i in class_names]),
                   shared_xaxes=False, shared_yaxes=True)

    for i in range(1,4):
        try:
            fig.add_trace(
                    go.Scatter(
                        x=classes_dict[class_names[0]][classes_dict[class_names[0]]['Marker Color'] == i]['Date'],
                        y=classes_dict[class_names[0]][classes_dict[class_names[0]]['Marker Color'] == i]['Grade'],
                        legendgroup = 'group3',
                        showlegend = False,
                        customdata = classes_dict[class_names[0]][classes_dict[class_names[0]]['Marker Color'] == i]['Weight'],
                        text = classes_dict[class_names[0]][classes_dict[class_names[0]]['Marker Color'] == i]['Assessment'],
                        mode = 'markers',
                        name = classes_dict[class_names[0]][classes_dict[class_names[0]]['Marker Color'] == i]['Assessment Type'].values[0],
                        marker=dict(
                            size=classes_dict[class_names[0]][classes_dict[class_names[0]]['Marker Color'] == i]['Weight']*2,
                            sizemin=6,
                            color = color_list[i],
                            line=dict(
                                color='rgb(1.00,1.00,1.00)',
                                width=1)
                            ),
                        hovertemplate =
                        '<i><b>Assessment</b></i>: %{text}<br>'+
                        '<i><b>Grade</b></i>: %{y}'+
                        '<br><b>Date</b>: %{x}<br>' +
                        '<b>Weight</b>: %{customdata}%<br>',
                        opacity = 0.8
                             ),
                row=1,col=1),

        except IndexError as Error:
            pass

    for i in range(1,4):
        try:
            fig.add_trace(
                    go.Scatter(
                        x=classes_dict[class_names[1]][classes_dict[class_names[1]]['Marker Color'] == i]['Date'],
                        y=classes_dict[class_names[1]][classes_dict[class_names[1]]['Marker Color'] == i]['Grade'],
                        legendgroup = 'group3',
                        showlegend = False,
                        customdata = classes_dict[class_names[1]][classes_dict[class_names[1]]['Marker Color'] == i]['Weight'],
                        text = classes_dict[class_names[1]][classes_dict[class_names[1]]['Marker Color'] == i]['Assessment'],
                        mode = 'markers',
                        name = classes_dict[class_names[1]][classes_dict[class_names[1]]['Marker Color'] == i]['Assessment Type'].values[0],
                        marker=dict(
                            size=classes_dict[class_names[1]][classes_dict[class_names[1]]['Marker Color'] == i]['Weight']*2,
                            sizemin=6,
                            color = color_list[i],
                            line=dict(
                                color='rgb(1.00,1.00,1.00)',
                                width=1)
                            ),
                        hovertemplate =
                        '<i><b>Assessment</b></i>: %{text}<br>'+
                        '<i><b>Grade</b></i>: %{y}'+
                        '<br><b>Date</b>: %{x}<br>' +
                        '<b>Weight</b>: %{customdata}%<br>',
                        opacity = 0.8
                             ),
                row=1,col=2),

        except IndexError as Error:
            pass

    for i in range(1,4):
        try:
            fig.add_trace(
                    go.Scatter(
                        x=classes_dict[class_names[2]][classes_dict[class_names[2]]['Marker Color'] == i]['Date'],
                        y=classes_dict[class_names[2]][classes_dict[class_names[2]]['Marker Color'] == i]['Grade'],
                        legendgroup = 'group3',
                        showlegend = False,
                        customdata = classes_dict[class_names[2]][classes_dict[class_names[2]]['Marker Color'] == i]['Weight'],
                        text = classes_dict[class_names[2]][classes_dict[class_names[2]]['Marker Color'] == i]['Assessment'],
                        mode = 'markers',
                        name = classes_dict[class_names[2]][classes_dict[class_names[2]]['Marker Color'] == i]['Assessment Type'].values[0],
                        marker=dict(
                            size=classes_dict[class_names[2]][classes_dict[class_names[2]]['Marker Color'] == i]['Weight']*2,
                            sizemin=6,
                            color = color_list[i],
                            line=dict(
                                color='rgb(1.00,1.00,1.00)',
                                width=1)
                            ),
                        hovertemplate =
                        '<i><b>Assessment</b></i>: %{text}<br>'+
                        '<i><b>Grade</b></i>: %{y}'+
                        '<br><b>Date</b>: %{x}<br>' +
                        '<b>Weight</b>: %{customdata}%<br>',
                        opacity = 0.8
                             ),
                row=1,col=3),
        except IndexError as Error:
            pass

    for i in range(1,4):
        try:
            fig.add_trace(
                    go.Scatter(
                        x=classes_dict[class_names[3]][classes_dict[class_names[3]]['Marker Color'] == i]['Date'],
                        y=classes_dict[class_names[3]][classes_dict[class_names[3]]['Marker Color'] == i]['Grade'],
                        legendgroup = 'group3',
                        showlegend = False,
                        customdata = classes_dict[class_names[3]][classes_dict[class_names[3]]['Marker Color'] == i]['Weight'],
                        text = classes_dict[class_names[3]][classes_dict[class_names[3]]['Marker Color'] == i]['Assessment'],
                        mode = 'markers',
                        name = classes_dict[class_names[3]][classes_dict[class_names[3]]['Marker Color'] == i]['Assessment Type'].values[0],
                        marker=dict(
                            size=classes_dict[class_names[3]][classes_dict[class_names[3]]['Marker Color'] == i]['Weight']*2,
                            sizemin=6,
                            color = color_list[i],
                            line=dict(
                                color='rgb(1.00,1.00,1.00)',
                                width=1)
                            ),
                        hovertemplate =
                        '<i><b>Assessment</b></i>: %{text}<br>'+
                        '<i><b>Grade</b></i>: %{y}'+
                        '<br><b>Date</b>: %{x}<br>' +
                        '<b>Weight</b>: %{customdata}%<br>',
                        opacity = 0.8
                             ),
                row=1,col=4)
        except IndexError as Error:
            pass

    for i in range(1,4):
        try:
            fig.add_trace(
                    go.Scatter(
                        x=classes_dict[class_names[4]][classes_dict[class_names[4]]['Marker Color'] == i]['Date'],
                        y=classes_dict[class_names[4]][classes_dict[class_names[4]]['Marker Color'] == i]['Grade'],
                        legendgroup = 'group3',
                        showlegend = True,
                        customdata = classes_dict[class_names[4]][classes_dict[class_names[4]]['Marker Color'] == i]['Weight'],
                        text = classes_dict[class_names[4]][classes_dict[class_names[4]]['Marker Color'] == i]['Assessment'],
                        mode = 'markers',
                        name = classes_dict[class_names[4]][classes_dict[class_names[4]]['Marker Color'] == i]['Assessment Type'].values[0],
                        marker=dict(
                            size=classes_dict[class_names[4]][classes_dict[class_names[4]]['Marker Color'] == i]['Weight']*2,
                            sizemin=6,
                            color = color_list[i],
                            line=dict(
                                color='rgb(1.00,1.00,1.00)',
                                width=1)
                            ),
                        hovertemplate =
                        '<i><b>Assessment</b></i>: %{text}<br>'+
                        '<i><b>Grade</b></i>: %{y}'+
                        '<br><b>Date</b>: %{x}<br>' +
                        '<b>Weight</b>: %{customdata}%<br>',
                        opacity = 0.8
                             ),
                row=1,col=5),
        except IndexError as Error:
            pass


    reference_line = go.Scatter(x=['2019-09-01 00:00:00', '2020-02-01 00:00:00'],
                                y=[70, 70],
                                mode="lines",
                                line=go.scatter.Line(color="gray"),
                                showlegend=False)
    fig.add_trace(reference_line, row=1, col=1)
    fig.add_trace(reference_line, row=1, col=2)
    fig.add_trace(reference_line, row=1, col=3)
    fig.add_trace(reference_line, row=1, col=4)
    fig.add_trace(reference_line, row=1, col=5)


    fig.add_trace(
        go.Scatter(
            x = classes_dict[class_names[0]]['Date'],
            y = classes_dict[class_names[0]]['Weighted Avg'],
            line=go.scatter.Line(color="gray",
                                shape="spline",
                                smoothing = 1.3),
            mode = 'lines+markers',
            opacity=0.9,
            showlegend=False,
            ),
        row=1, col=1),

    fig.add_trace(
        go.Scatter(
            x = classes_dict[class_names[1]]['Date'],
            y = classes_dict[class_names[1]]['Weighted Avg'],
            line=go.scatter.Line(color="gray",
                                shape="spline",
                                smoothing = 1.3),
            mode = 'lines+markers',
            opacity=0.9,
            showlegend=False,
            ),
        row=1, col=2),

    fig.add_trace(
        go.Scatter(
            x = classes_dict[class_names[2]]['Date'],
            y = classes_dict[class_names[2]]['Weighted Avg'],
            line=go.scatter.Line(color="gray",
                                shape="spline",
                                smoothing = 1.3),
            mode = 'lines+markers',
            opacity=0.9,
            showlegend=False,
            ),
        row=1, col=3),

    fig.add_trace(
        go.Scatter(
            x = classes_dict[class_names[3]]['Date'],
            y = classes_dict[class_names[3]]['Weighted Avg'],
            line=go.scatter.Line(color="gray",
                                shape="spline",
                                smoothing = 1.3),
            mode = 'lines+markers',
            opacity=0.9,
            showlegend=False,
            ),
        row=1, col=4),

    fig.add_trace(
        go.Scatter(
            x = classes_dict[class_names[4]]['Date'],
            y = classes_dict[class_names[4]]['Weighted Avg'],
            opacity=0.9,
            line=go.scatter.Line(color="gray",
                                shape="spline",
                                smoothing = 1.3),
            mode = 'lines+markers',
            showlegend=False,
            ),
        row=1, col=5),





    fig.update_layout(
        showlegend=True,
        hoverlabel_align = 'left',
        height=600,
        width = 1400,

        xaxis1=dict(
            gridcolor='white',
            nticks = 4
            ),

        yaxis1 = dict(title = 'Grade',
                    gridcolor = 'white')
        )


    return fig










##############################################################################################
                         #### Part Two: Dash Layout ####
##############################################################################################

'''
style_table={
   'maxHeight': '255px',
   'overflowY': 'scroll',
   'overflowX': 'scroll',
   'marginBottom':'5px',
   },
style_as_list_view=True,
merge_duplicate_headers=True,
css=[{
'selector': '.dash-cell div.dash-cell-value',
'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
}],
'''




date_range = [i for i in range(len(all_files))]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server
app.layout = html.Div([
    html.H2('Job Postings Database',
            style={
                'marginLeft':'5px'
            }),
    dcc.Tabs(id="tabs-example", value='tab-1-example',
             children=[
                dcc.Tab(label='Skills and Certifications', value='tab-1-example',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label='My Semester', value='tab-2-example',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
    ],style={
        'width':'85%',
        'marginLeft':'5px'
    }),
    html.Div(id='tabs-content-example')
], style = {
    'marginLeft':'10%',
})
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([

                        #upper-main Div
                        html.Div([

                            #dropdowns and checklists
                            html.Div([

                                html.Div([

                                    html.H6('Choose analytical skills',
                                            style={'marginTop':'3px',
                                            'marginBottom':'2px',}),
                                    dcc.Checklist(id='skills-checklist',
                                        #options=[{'label': x, 'value': x} for x in skill_names],
                                        value=[x for x in skill_names[:3]],
                                        style={'marginTop':'0%',
                                               'verticalAlign':'left',
                                               'textAlign':'left'},
                                                labelStyle={'display':'inline-block'}),
                                ],className="two columns",
                                     style={
                                        'height':'260px',
                                        'width':'90%',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '5px',
                                        'marginTop':'5px',
                                        'overflowY': 'scroll',
                                        'marginLeft':'5%',
                                        #'marginRight':'1%',
                                        'marginBottom':'10px',
                                        'textAlign':'center',
                                        'backgroundColor':'white',
                                        #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                        'box-shadow':'2px 2px 5px 0.1px rgba(0, 0, 0, 0.4)'}),

                                html.Div([

                                    html.H6('Choose Certifications',
                                            style={'marginTop':'3px',
                                            'marginBottom':'2px',}),

                                    dcc.Checklist(id='certif-checklist',
                                        #'white-space': 'nowrap',
                                        #'overflow': 'scroll',


                                        value=[x for x in certifications[:3]],
                                        style={'marginTop':'0%',
                                               'verticalAlign':'left',
                                               'textAlign':'left',
                                               'text-overflow': 'ellipsis',},
                                                labelStyle={'display':'inline-block'})

                                ],className="two columns",
                                     style={
                                        'height':'220px',
                                        'width':'90%',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '5px',
                                        'marginTop':'10px',
                                        'overflowY': 'scroll',
                                        'marginLeft':'5%',
                                        #'marginRight':'1%',
                                        'marginBottom':'5px',
                                        'textAlign':'center',
                                        'backgroundColor':'white',
                                        #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                        'box-shadow':'2px 2px 5px 0.1px rgba(0, 0, 0, 0.4)'}),

                        ],className="six columns",
                         style={'width':'33%',
                            'height':'515px',
                            'borderRadius': '5px',
                            'marginTop':'8px',
                            'marginLeft':'0.1%',
                            'marginRight':'0.5%',
                            'marginBottom':'15px',
                            'textAlign':'center',
                            'backgroundColor':'white',
                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                            #'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'
                            }),

                            #container for graphs (upper-main Div)
                            html.Div([

                                html.Div([

                                    html.Div([

                                        html.H6('Display Skills or Certifications',
                                                      style={'marginTop':'0.1px',
                                                      'marginBottom':'5px',
                                                      'padding':'1px',
                                                      'font-size': '1em',
                                                      'overflowX':'scroll',
                                                        }),
                                    ],className="three columns",
                                         style={
                                            'width':'40%',
                                            'height':'22px',
                                            'marginTop':'3px',
                                            'marginLeft':'7%',
                                            'marginRight':'2%',
                                            'marginBottom':'0.1px',
                                            'textAlign':'center',
                                            }),

                                    html.Div([

                                        html.H6('Change Graph display',
                                                      style={'marginTop':'0.1px',
                                                      'marginBottom':'5px',
                                                      'font-size': '1em'
                                                        }),
                                        ],className="three columns",
                                         style={
                                            'width':'40%',
                                            'height':'22px',
                                            'marginTop':'3px',
                                            'marginLeft':'2%',
                                            'marginRight':'7%',
                                            'marginBottom':'0.1px',
                                            'textAlign':'center',
                                            }),


                                    html.Div([
                                    dcc.Dropdown(id='skill-or-cert-dropdown',
                                                 options=[{'label':x,'value':x} for x in skill_or_certificaiton],
                                                 value = skill_or_certificaiton[0],
                                                style={
                                                    "margin-right": "0.1%",
                                                     "margin-left": "0%",
                                                     "marginBottom": "0%",
                                                     'width':'101%',
                                                     'height':'39.5px'})
                                    ],className="three columns",
                                         style={
                                            'width':'40%',
                                            'height':'39.5px',
                                            'borderRadius': '3px',
                                            'marginTop':'5px',
                                            'marginLeft':'7%',
                                            'marginRight':'2%',
                                            'marginBottom':'5px',
                                            'textAlign':'center',
                                            'vertical-align': 'middle',
                                            #'backgroundColor':'rgb(107, 213, 242)',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'2px 2px 15px 0.5px rgba(0, 0, 0, 0.4)'}),

                                    html.Div([
                                    dcc.Dropdown(id='graph-sort-dropdown',
                                                 options=[{'label':x,'value':x} for x in graph_sort_options],
                                                 value = graph_sort_options[0],
                                                style={
                                                    "margin-right": "0%",
                                                     "margin-left": "0.1%",
                                                     "marginBottom": "0.1%",
                                                     'width':'101%',
                                                     'height':'39.5px',
                                                     #'white-space': 'nowrap',
                                                     #'overflow': 'scroll',
                                                     #'text-overflow': 'ellipsis'
                                                     })
                                    ],className="three columns",
                                         style={
                                            'width':'40%',
                                            'height':'39px',
                                            'borderRadius': '3px',
                                            'marginTop':'5px',
                                            'marginLeft':'2%',
                                            'marginRight':'7%',
                                            'marginBottom':'5px',
                                            'vertical-align': 'middle',
                                            'display':'inline-block',
                                            'textAlign':'center',
                                            #'backgroundColor':'rgb(107, 213, 242)',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'2px 2px 10px 0.5px rgba(0, 0, 0, 0.4)'}),

                                ],className="two columns",
                                     style={'width':'97%',
                                        'height':'85px',
                                        'marginTop':'5px',
                                        'marginLeft':'1.5%',
                                        'marginRight':'25px',
                                        'marginBottom':'5px',
                                        'textAlign':'center',
                                        'backgroundColor':'white',
                                        #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                        #'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'
                                        }),
                                #graph one
                                html.Div([
                                    dcc.Graph(id='skills-time-graph',
                                              figure = create_initial_graph(base_skill_values)

                                )],className="two columns",
                                     style={'width':'97%',
                                        'height':'400px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '5px',
                                        'marginTop':'10px',
                                        'marginLeft':'1.5%',
                                        'marginRight':'0%',
                                        'marginBottom':'1%',
                                        'overflowX': 'scroll',
                                        'textAlign':'center',
                                        'backgroundColor':'white',
                                        #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                        'box-shadow':'2px 2px 10px 0.1px rgba(0, 0, 0, 0.4)'}),


                            ],className="two columns",
                                 style={'width':'65%',
                                    'height':'515px',
                                    'borderRadius': '5px',
                                    'marginTop':'8px',
                                    'marginLeft':'0.5%',
                                    'marginRight':'0.5%',
                                    'marginBottom':'15px',
                                    'textAlign':'center',
                                    'backgroundColor':'white',
                                    #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                    #'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'
                                    }),



                                html.Div([dcc.Graph(id='bar-chart',
                                                    figure = initial_bar_chart(base_skill_bar_vals))
                                    ],className="two columns",
                                         style={'width':'97%',
                                            'height':'302px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'solid',
                                            'borderRadius': '5px',
                                            'marginTop':'5px',
                                            'marginLeft':'1%',
                                            'marginRight':'0.5%',
                                            'overflowX': 'scroll',
                                            'marginBottom':'0.5%',
                                            'textAlign':'center',
                                            'backgroundColor':'white',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'3px 3px 10px 0.1px rgba(0, 0, 0, 0.4)'}),


                        ],className="row",
                                 style={'backgroundColor':'white',
                                        'height':'910px',
                                        'width':'99%',
                                        'marginLeft':'1%',
                                        'marginRight':'1%',
                                        'overflowX':'scroll',
                                        'marginTop':'20px'}),





            #main Div
            ],className="row",style={'backgroundColor':'white',
                    'width':'85%',
                    'height':'2200px',
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'marginLeft':'5px',
                    'marginRight':'5px'})


    #Tab two layout
    elif tab == 'tab-2-example':
        return html.Div([
            html.H6('Visual of Fall Semester Grades',
                    style={'marginTop':'3px',
                    'marginBottom':'3px',}),
            dcc.Graph(id='tab2-graph',
                    figure = create_tab2_graph(classes_dict),
                    style = {'width':'100%',
                             'marginRight':'0.5%',
                             'overflowX':'scroll'})
        ],className="two columns",
             style={'width':'85%',
                'height':'650px',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '5px',
                'marginTop':'2%',
                'marginLeft':'0.5%',
                'marginRight':'0.5%',
                'marginBottom':'0.5%',
                'textAlign':'center',
                'backgroundColor':'white',
                #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                'box-shadow':'3px 3px 10px 0.1px rgba(0, 0, 0, 0.4)'}),









##############################################################################################
                           #### Part Three: App Callbacks ####
##############################################################################################





@app.callback(Output('skills-time-graph','figure'),
              [Input('skills-checklist','value'),
               Input('certif-checklist','value')])
@cache.memoize
def callback_initial_graph(skill_values,certif_values):
    traces = []

    for i in range(len(skill_values)):
        traces.append(go.Scatter(x = date_range,
                           y = skill_counts[skill_values[i]],
                           line=go.scatter.Line(
                            shape="spline",
                            smoothing = 1.0),
                           name = skill_values[i]))
    for j in range(len(certif_values)):
        traces.append(go.Scatter(x = date_range,
                           y = certif_counts[certif_values[j]],
                           line=go.scatter.Line(
                            shape="spline",
                            smoothing = 1.0),
                           name = certif_values[j]))

    data = traces
    layout = go.Layout(
                  title='Skills/Certifications in job postings (August to December)',hovermode='closest',
                  showlegend=True, legend= {'itemsizing': 'constant'},
                  xaxis_title="Weekly scrape of Indeed job postings",
                  yaxis_title="# of mentions",
                  height = 400,
                  font=dict(
                    family="Courier New, monospace",
                    size=11,
                    color="#7f7f7f"),
                  margin=go.layout.Margin(
                      l=3,
                      r=3,
                      b=60,
                      t=50,
                      pad=1
                      ),
                  )

    fig = go.Figure(data=data,layout=layout)


    return fig

'''
id='graph-sort-dropdown',
             options=[{'label':x,'value':x} for x in graph_sort_options],
             value = graph_sort_options[0],
'''

@app.callback(Output('bar-chart', 'figure'),
              [Input('skills-checklist','options'),
               Input('certif-checklist','options'),
               Input('skill-or-cert-dropdown','value')])
@cache.memoize
def update_graph(data, cols, skill_or_cert):
    print(skill_or_cert)
    bar_width = 0.9
    traces = []
    x_values = []
    y_values = []

    if skill_or_cert == skill_or_certificaiton[0]:
        for j in range(len(skill_names)):
            x_values.append(list(skill_counts.keys())[j]),
            y_values.append(np.mean(skill_counts[skill_names[j]])),

        test = pd.DataFrame(zip(y_values, x_values))
        test.columns = ['value','name']
        test = test.sort_values(by = 'value', ascending=False)
        test = test.reset_index()

        traces.append(
                go.Bar(
                   x = test['name'],
                   y = test[test['value'] > 2]['value'],
                   width=[bar_width],
                   ))


        layout = go.Layout(
          title='Skills Average Value',
          hovermode='closest',
          showlegend=False, legend= {'itemsizing': 'constant'},
          height = 300,
          font=dict(
            family="Courier New, monospace",
            size=11,
            color="#7f7f7f"),
          xaxis = {'automargin': True, 'title': 'Skill',
                   },
          yaxis = {'automargin': True, 'title': 'Count'},
          margin=go.layout.Margin(
              l=2,
              r=2,
              b=90,
              t=30,
              pad=1
              ),
          )

        data = traces


    else:
        for j in range(len(certifications)):
            x_values.append(list(certif_counts.keys())[j]),
            y_values.append(np.mean(certif_counts[certifications[j]])),

        test = pd.DataFrame(zip(y_values, x_values))
        test.columns = ['value','name']
        test = test.sort_values(by = 'value', ascending=False)
        test = test.reset_index()

        traces.append(
                go.Bar(
                   x = test['name'],
                   y = test[test['value'] > 2]['value'],
                   width=[bar_width],
                   ))

        layout = go.Layout(
          title='Certification Average Value',
          hovermode='closest',
          showlegend=False, legend= {'itemsizing': 'constant'},
          height = 300,
          font=dict(
            family="Courier New, monospace",
            size=11,
            color="#7f7f7f"),
          xaxis = {'automargin': True, 'title': 'Certification'},
          yaxis = {'automargin': True, 'title': 'Count'},
          margin=go.layout.Margin(
              l=5,
              r=5,
              b=90,
              t=30,
              pad=1
              ),
          )

        data = traces

    fig = go.Figure(data=data,layout=layout)

    return fig

'''
#Dropdown One
@app.callback([Output('skills-checklist','options'),
              Output('certif-checklist','options')],
              [Input('skill-or-cert-dropdown','value'),
               Input('change-graph-dropdown','value')])
@cache.memoize
def line_or_bar(sc_dropdown,line_bar_val):

    if sc_dropdown == skill_or_certificaiton[0]:
        skill_checklist_values = [i for i in skill_names[:3]]
        certif_checklist_values = []

    if sc_dropdown == skill_or_certificaiton[1]:
        skill_checklist_values = []
        certif_checklist_values = [i for i in certifications[:3]]


    return skill_checklist_values, certif_checklist_values
'''

#Dropdown Two (part a)
@app.callback([Output('skills-checklist','options'),
              Output('certif-checklist','options')],
              [Input('skill-or-cert-dropdown','value')])
@cache.memoize
def choosing_skills_or_certifs(sc_dropdown):

    if sc_dropdown == skill_or_certificaiton[0]:
        skills_options = [{'label': x, 'value': x} for x in skill_names]
        certif_options = [{'label': x, 'value': x, 'disabled':True} for x in list(certifications)]

    else:
        skills_options = [{'label': x, 'value': x, 'disabled':True} for x in list(skill_names)]
        certif_options = [{'label': x, 'value': x} for x in certifications]


    return skills_options, certif_options

#Dropdown Two (part b)
@app.callback([Output('skills-checklist','value'),
              Output('certif-checklist','value')],
              [Input('skill-or-cert-dropdown','value'),
               Input('graph-sort-dropdown','value'),])
@cache.memoize
def selecting_chklist_vals(skill_cert_dropdown, sorting_dropdown):

    if skill_cert_dropdown == skill_or_certificaiton[0]:
        certif_value = [certifications[0]]
        if sorting_dropdown == graph_sort_options[0]:
            skills_value = [x for x in skill_names[:7]]

        if sorting_dropdown == graph_sort_options[1]:
            skills_value = [i for i in skill_pct_chg_df['Skill'][:7]]

        if sorting_dropdown == graph_sort_options[2]:
            skills_value = [i for i in skill_val_chg_df['Skill'][:7]]



    if skill_cert_dropdown == skill_or_certificaiton[1]:
        skills_value = [skill_names[0]]
        if sorting_dropdown == graph_sort_options[0]:
            certif_value = [i for i in certifications[:7]]

        if sorting_dropdown == graph_sort_options[1]:
            certif_value = [i for i in certif_pct_chg_df['Certification'][:7]]

        if sorting_dropdown == graph_sort_options[2]:
            certif_value = [i for i in certif_val_chg_df['Certification'][:7]]



    return skills_value, certif_value




#Data Table
'''
html.Div([
    html.H6('Explore the Dataset',
            style={'marginTop':'3px',
            'marginBottom':'3px',}),
    dash_table.DataTable(
    id = 'table',
    columns = name_list,
    data=rate_chg_df.to_dict('records'),
    style_cell={'textAlign': 'left',
                'textOverflow': 'ellipsis',
                'height': '30px',
                'minWidth': '10px', 'maxWidth': '90px',
                'whiteSpace': 'normal'},
    style_cell_conditional=[
                {
                    'if': {'column_id': 'Skills'},
                    'textAlign': 'center'
                }],
     style_table={
        'maxHeight': '255px',
        'overflowY': 'scroll',
        'overflowX': 'scroll',
        'marginBottom':'5px',
        },
    style_as_list_view=True,
    merge_duplicate_headers=True,
    css=[{
     'selector': '.dash-cell div.dash-cell-value',
     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
     }],
    editable=False,
    row_selectable="multi",
    sort_action="native",
    sort_mode="multi",
    fixed_rows={ 'headers': True, 'data': 0 }
    ),

    ],className="two columns",
         style={'width':'97%',
            'height':'290px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'marginTop':'2%',
            'marginLeft':'1.5%',
            'marginRight':'0%',
            'marginBottom':'0.5%',
            'textAlign':'center',
            'backgroundColor':'rgb(107, 213, 242)',
            'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
            'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'}),
'''


# Stop the stopwatch / counter
t1_stop = process_time()

print("Elapsed time:", t1_stop, t1_start)

print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)


if __name__ == '__main__':
    app.run_server(debug=True)
