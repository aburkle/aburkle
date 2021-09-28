import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import glob
import missingno as msno


st.title('Analysis of the E-Learning during the COVID-19 pandemic in the US.')
st.header('Goal: How affected the COVID-19 the different social groups in US?')


st.header('The Data Bases:')

districts_info = pd.read_csv('C:/Users/andre/Desktop/Kaggle-e-Learning/learnplatform-covid19-impact-on-digital-learning/districts_info.csv', index_col=0)
products_info = pd.read_csv('C:/Users/andre/Desktop/Kaggle-e-Learning/learnplatform-covid19-impact-on-digital-learning/products_info.csv', index_col=0)
engagement_df = pd.read_csv('C:/Users/andre/Desktop/Streamlit/engagement_df.csv',index_col=0)




st.subheader('Data base:`districts_info`')

districts_info.sample(3)
districts_info.head()
st.write(districts_info.sample(3))
st.write(districts_info.shape)
st.write(''' Source of the Information:
- National Center for Education Statistics (NCES), 
- The Federal Communications Commission (FCC),
- Edunomics Lab.''')




st.subheader('Data base: `products_info`')
products_info.sample(3)
products_info.head()
st.write(products_info.sample(3))
st.write(products_info.shape)
st.write('''The product file includes information about the characteristics of the top 372 products with the most users in 2020.''')



st.subheader('Data base: `engagement_df`')

engagement_df.sample(3)
engagement_df.head()
st.write(engagement_df.sample(3))
st.write(engagement_df.shape)
st.write('''The engagement data are based on LearnPlatform’s Student Chrome Extension.
The extension collects page load events of over 10K education technology products in our product library, 
including websites, apps, web apps, software programs, extensions, ebooks, hardwares, and services used in educational institutions.''')



st.header('Some raw data numbers')
st.write(''' 

- `22,3` **MM Data Points!!** 

- `233` **School Districts** 

- `372` **Digital Products with most users**''' 
)


st.subheader('Data Cleaning: Nan´s in the different DF´s')

percent_missing = engagement_df.isnull().sum() *100/ len(engagement_df)
pie_values=[percent_missing['engagement_index'], percent_missing['pct_access'], 75.85]
names=['NaN_engagement_index','NaN_pct_access','Available Values']
fig = px.pie(pie_values, values=pie_values
             ,names=names, hole=0.5)
fig.update_layout(legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=0.9,
) #font=dict(
        #size=20,
        #),title_x=0.5
        )
st.plotly_chart(fig)




## ------- Bar Chart Nan's DF districts_info


fig = go.Figure(data=[go.Bar(x=districts_info.columns, y=districts_info.isnull().sum())]) 
fig.update_layout(legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=0.6))
st.plotly_chart(fig)

st.write('After some analysis, I drop the columns `county_connections_ratio`, `pp_total_raw` and Nan´s rows from State from `233` --> `176` districts to analyze from `district_info`.')
districts_info.dropna(subset=['state'], inplace=True)
districts_info.drop(['county_connections_ratio','pp_total_raw'], axis = 1,inplace=True)

## ------- Bar Chart Nan's DF products_info


fig = go.Figure(data=[go.Bar(x=products_info.columns, y=products_info.isnull().sum())]) 
fig.update_layout(legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=0.6))
                  

st.plotly_chart(fig)


products_info.dropna(subset=['Sector(s)'], inplace=True)

st.write('I drop all Nan´s from `372` --> `352` digital products from `products_info`') 

## ----- District Analysis

st.header('Districts Analysis: (This part is better known a Plotly-Party!)')

st.subheader('23 States divided per School Districts and Locale')

## ------- Tree Map (Squares-Chart)
    
fig, ax=plt.subplots()
state_locale= districts_info.groupby("state")["locale"].value_counts().to_frame().rename(columns={"locale": "Number of School Districts"}).reset_index()
fig = px.treemap(state_locale, path=['state', 'locale'], values='Number of School Districts',color='locale' )
fig.update_layout(title_x=0.5,margin=dict(l=10, r=20, t=30, b=20),
    autosize=False,
    width=1300,
    height=400,
    )
st.plotly_chart(fig)



## ------- Bar Chart 

st.subheader('School distribution per State')

lst = districts_info.state.value_counts() 
vals = districts_info.state.dropna().unique()
df1 = pd.DataFrame(columns=['Count'],index= vals)
df1.Count = lst
df1 = df1.sort_values(by='Count', ascending=True)
fig = px.bar(df1, x ="Count" , y =df1.index ,
              color_continuous_scale ='YlGnBu',color="Count",height=500)
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig)

## ------- Map Chart

st.subheader('Count of School Districts per State')

states_abreviation = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District Of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

districts_info['states_abreviation'] = districts_info['state'].map(states_abreviation)

fig = go.Figure()
layout = dict(
    geo_scope = 'usa'
)

fig.add_trace(
    go.Choropleth(
        locations = districts_info['states_abreviation'].value_counts().to_frame().reset_index()['index'],
        zmax = 1,
        z = districts_info['states_abreviation'].value_counts().to_frame().reset_index()['states_abreviation'],
        locationmode = 'USA-states',
        marker_line_color = 'white',
        geo = 'geo',
        colorscale = "YlGnBu", 
    )
)



fig.update_layout(layout)   
st.plotly_chart(fig)



## -------- Pie Chart

st.subheader('School distribution per Locale')

sizes = districts_info.locale.value_counts()
labels = districts_info.locale.dropna().unique() # I drop all de NaN's Values
df2 = pd.DataFrame(columns=['Count'],index= labels)
df2.Count = sizes

fig = px.pie(df2, values='Count', names=df2.index, hole=.5,color_discrete_sequence=px.colors.cyclical.Twilight)
fig.update_layout(title_x=0.5, legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=0.8))

st.plotly_chart(fig)

st.write('Almost 78% of the School Districts are Suburb + Rural')

## -------- Product Analysis


st.header('Which are the most popular products?')

products_engagement_data = pd.merge(products_info, engagement_df, left_on='LP ID', right_on='lp_id')


## -------- Bar Chart Top 5 Products

st.subheader('Top 5 Providers of Digital products')

lst = products_info["Provider/Company Name"].value_counts()
vals = products_info["Provider/Company Name"].unique()
df3__ = pd.DataFrame(columns=['Count'],index= vals)
df3__.Count = lst
df3__ = df3__.sort_values(by='Count', ascending=False)[:5]
### plot bar 
##df1, x ="Count" , y =df1.index ,title="States Distribution",
              
fig = px.bar(df3__, x =df3__.index , y ="Count",color="Count",height=500, color_continuous_scale='Blackbody')
fig.update_xaxes(tickangle=-40)
fig.update_layout(title_x=0.5,paper_bgcolor="White" )

st.plotly_chart(fig)



st.subheader('Top 5 most used of Digital products')

lst = products_engagement_data["Provider/Company Name"].value_counts()
vals = products_engagement_data["Provider/Company Name"].unique()
df3__ = pd.DataFrame(columns=['Count'],index= vals)
df3__.Count = lst
df3__ = df3__.sort_values(by='Count', ascending=False)[:5]
### plot bar 
##df1, x ="Count" , y =df1.index ,title="States Distribution",
              
fig = px.bar(df3__, x =df3__.index , y ="Count",color="Count",height=500, color_continuous_scale='Blackbody')
fig.update_xaxes(tickangle=-40)
fig.update_layout(title_x=0.5,paper_bgcolor="White" )

st.plotly_chart(fig)

st.write('The most important provider for digital Products is `Google LLC`')


## -------- Pie Chart most important Sector

st.subheader('Sectors of the digital products')


count = products_info['Sector(s)'].str.contains('PreK-12').sum()
sector_dict = {'PreK-12':0,'Higher Ed':0, 'Corporate':0}

for sector in sector_dict.keys():
    val = products_info['Sector(s)'].str.contains(sector).sum()
    sector_dict.update({sector:val})


df4 = pd.DataFrame(columns=['Count'],index= sector_dict.keys())
df4.Count = sector_dict.values()

fig = px.pie(df4, values='Count', names=df4.index , color_discrete_sequence=px.colors.sequential.Blackbody, hole=0.5)
fig.update_layout(legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=0.8))

st.plotly_chart(fig)

st.write('Prek-12 Which is from kindergarten to 12th grade, is dominant with `50.8%`')



## -------- Pie Chart Primary Essential Function

st.subheader('Functions per engagement of the digital products')


primary_essential_main = []
primary_essential_sub = []
for s in products_info["Primary Essential Function"]:
    if(not pd.isnull(s)):
        s1 = s.split("-",1)[0].strip()
        primary_essential_main.append(s1)
    else:
        primary_essential_main.append(np.nan)
    
    if(not pd.isnull(s)):
        s2 = s.split("-",1)[1].strip()
        primary_essential_sub.append(s2)
    else:
        primary_essential_sub.append(np.nan)

products_info["primary_essential_main"] = primary_essential_main
products_info["primary_essential_sub"] = primary_essential_sub

c1=c2=c3=0

for s in products_info["primary_essential_main"]:
    if(not pd.isnull(s)):
        c1 += s.count("CM")
        c2 += s.count("LC")
        c3 += s.count("SDO")
        
df5 = pd.DataFrame(columns=['Count'],index= ['CM','LC','SDO'])
df5.Count = [c1,c2, c3]
fig = px.pie(df5, values='Count', names=df5.index, color_discrete_sequence=px.colors.sequential.Blackbody, hole=0.5)

st.plotly_chart(fig)



'''- LC: Learning and Curriculum comes 1st with `75%` as the Primary Essential function of the Product'
- CM: Classroom Management comes 2nd with `13%`
- SDO: School and District Operation comes 3rd with `12%`')'''

## -------- Bar Chart Engagement_index per Locale

st.header('Engagement Analysis')

engagement_df["district_id"] = engagement_df["district_id"].astype(str).astype(int)
districts_engagement_data = pd.merge(districts_info, engagement_df, left_on='district_id', right_on='district_id')

result = districts_engagement_data.groupby(['locale']).agg({'engagement_index': 'mean'})
result = result.reset_index()

fig = px.bar(result, x ='locale' , y ='engagement_index',color="engagement_index",height=500, color_continuous_scale ='Blues')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor="White" )

st.plotly_chart(fig)

st.write('By far the highest `engagement_index` is in the rural areas (defined as: Total page-load events per 1000 students of a given digital product and on a given day')

## -------- Bar Chart pct_access per Locale

result = districts_engagement_data.groupby(['locale']).agg({'pct_access': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='locale' , y ='pct_access',color="pct_access",height=500, color_continuous_scale ='Blues')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor="White" )

st.plotly_chart(fig)

st.write('The case of `pct_access` is very similar to the engagement! `pct_access` defined as: Percentage of students in the district have at least one page-load event of a given product and on a given day')

st.subheader('Total Engagement over time per locale')

def time_series_plot(df,col1,col2,col3):
    max_list = df[[col1,col2]]\
        .groupby([col1])[col2].mean()\
        .sort_values(ascending=False).index[:5].tolist()

    df = df[df[col1].isin(max_list)]\
                    .reset_index(drop=True)[[col3, col1, col2]]
    df = df.pivot_table(index=col3, columns=col1, values=col2)

    fig = px.line(df, facet_col=col1, facet_col_wrap=1, width=900, height=1500)
    fig.update_layout(
                      title=("Top :"+ col1 + " , " + col2 + " , " + col3).title(),
                      title_x=0.39,
                      template="plotly_white",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)',
                      font = {'family': 'Serif', 'size': 20}
                     )
    st.plotly_chart(fig)




time_series_plot(districts_engagement_data,"locale","engagement_index","time")

st.write('It´s very clear that the engagement goes down between Jun-Aug due to the Summer-Break. Also, City is the only `locale` that had an increase in engagement over time.')

st.subheader('`engagement_index` over time per `pct_black/hispanic`')

st.write('Let´s see the distribution of the `pct_black/hispanic`')

## ---- Bar Chart B/H count

#result = districts_engagement_data.groupby(['pct_black/hispanic'])
#result = result.reset_index()
#fig = px.bar(result,height=500, color_continuous_scale ='Rdbu_r')
#fig.update_xaxes(tickangle=-40)
#fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
#                      plot_bgcolor = 'rgba(0,0,0,0)' )

#st.plotly_chart(fig)

# I need to understand de count of  

def count_plot(df, col, title, hue=None):
    fig, ax=plt.subplots()
    ax=sns.countplot(data = df, y=col, hue=hue, order=df[col].value_counts().index)
    sns.despine()
    plt.title(title, size=12)
    plt.xticks(rotation=75, fontsize=8)
    plt.yticks( fontsize=8)
    plt.xlabel(col, fontsize=10)
    plt.ylabel("Count", fontsize=10)
    st.pyplot(fig)

# count_plot(districts_engagement_data, 'pct_black/hispanic',title='Count of B/H')

## ---- Bar Chart B/H vs count


result = districts_engagement_data.groupby(['pct_black/hispanic']).count()
# result = result.reset_index()

fig = px.bar(result, y ='state', height=500, color_continuous_scale ='Rdbu_r',labels={'state':'B/H Count'})
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)' )

st.plotly_chart(fig)

## ---- Bar Chart B/H vs Engagement

result = districts_engagement_data.groupby(['pct_black/hispanic']).agg({'engagement_index': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='pct_black/hispanic' , y ='engagement_index',color="engagement_index",height=500, color_continuous_scale ='Rdbu_r')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)' )

st.plotly_chart(fig)

st.write('''It´s very interesting that the places with a high level of engagement in places where the representation of pct_black/hispanic is high.
Let´s check if there is a correlation with the locale, `state´, or a combination''')

## ----- Treemap between B/H vs Locale vs State

### """fig, ax=plt.subplots()
#state_locale= districts_engagement_data.groupby("state")["locale"].value_counts().to_frame().rename(columns={"locale": "Number of School Districts"}).reset_index()
#fig = px.treemap(state_locale, path=['state', 'locale'], values='',color='locale' )
#fig.update_layout(title_x=0.5,margin=dict(l=10, r=20, t=30, b=20),
 #   autosize=False,
  #  width=1300,
   # height=400,
    #)
#st.plotly_chart(fig) 

## ----- Bar Chart B/H vs Locale 


result = districts_engagement_data.groupby(['locale','pct_black/hispanic']).agg({'engagement_index': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='locale' , y ='engagement_index',color="pct_black/hispanic", barmode='group', height=500, color_continuous_scale ='Rdbu_r')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)' )

st.plotly_chart(fig)

'''Ok, we can see that the highest engagements we find in the cities, with a high level of `pct_black/hispanic`, and in the Rural areas where the representation `pct_black/hispanic` is at lowest.
Then we should try to find in which states we can find the highest engagements values. Another interesting point is that AVG City does not have the best accessibility or engagement in comparison with rural'''


result = districts_engagement_data.groupby(['state','pct_black/hispanic']).agg({'engagement_index': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='state' , y ='engagement_index',color="pct_black/hispanic", barmode='group', height=500, color_continuous_scale ='Rdbu_r')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)' )

st.plotly_chart(fig)

''' Finally, we found where comes the high engagement of `pct_black/hispanic` the group and it comes from  Arizona and New York. It's also remarkable that North Dakota, New Hampshire
     are rural areas where the B/H is really low. '''


## ----- pct_free/reduced vs engagement_index




st.subheader('`pct_free/reduced` per locale')
st.write('`pct_free/reduced` is defined as Percentage of students in the districts eligible for free or reduced-price lunch based on 2018-19 NCES data')

result = districts_engagement_data.groupby(['pct_free/reduced']).agg({'engagement_index': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='pct_free/reduced' , y ='engagement_index',color="engagement_index",height=500, color_continuous_scale ='Dense')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)' )
st.plotly_chart(fig)
st.write('Interesting that the ones who are eligible have the highest engagement_index. Let´s see more in detail')

## ----- pct_free/reduced vs engagement_index


result = districts_engagement_data.groupby(['locale','pct_free/reduced']).agg({'engagement_index': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='locale' , y ='engagement_index',color="pct_free/reduced", barmode='group', height=500, color_continuous_scale ='Rdbu_r')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)' )

st.plotly_chart(fig)

## ----- pct_free/reduced vs engagement_index

''' '''


result = districts_engagement_data.groupby(['state','pct_free/reduced']).agg({'engagement_index': 'mean'})
result = result.reset_index()
fig = px.bar(result, x ='state' , y ='engagement_index',color="pct_free/reduced", barmode='group', height=500, color_continuous_scale ='Rdbu_r')
fig.update_xaxes(tickangle=-40)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor = 'rgba(0,0,0,0)' )

st.plotly_chart(fig)


st.header('Recap- main Observations')

''' 
- The digital products are orientated to High-School students and Google LLC is by far the most important Provider with half of the engagement.
- Rural Areas have a higher engagement and accessibility than the others areas. 

- B/H is a clear minority (aprox 6 to 1)
- B/H is high in the Cities and Suburbs and the representation of B/H in Rural and Towns is low
- Surprisingly the engagement is the highest where the proportion of B/H is really high but the 2nd highest engagement value is where the proportion is at lowest in the rural areas.
- Dividing per locale we see 2 things:
    - The highest average value is due to a really high engagement in a very few schools, NY and Arizona.
    - The 2nd highest average value is in the schools where the proportion of B/H is less than 20% and the variation is lower. 
- In the Suburbs the engagement is higher in the schools where the proportion of B/H is lower.

- In regard to `pct_free/reduced` we see almost the same situation that with B/H. We have some restrictions with the available information (No Arizona). 
- With the exception of Cities, in every `locale` the is a clear negative correlation between `engagement_index` and `pct_access`, especially for `Town`.
    - Analyzing Cities is the same fall as with B/H a few really high engagement cases in NY and Indiana.


'''





st.header('Next Steps')

'''  
- Extrapolation to an international analysis. 
- A deeper understanding of the high `engagement_index` of the rural areas in comparison with the others. (Different State Policies?)
- It could be incorporated new Databases, to analyze the impact of:
  - States Policies during the pandemic, like restrictions, openings 
  - Reports of the 2020 KIDS COUNT DATA BOOK, to understand better the impact of race, wealth
  - Kaiser Family Foundation: State COVID-19 Data and Policy Actions, to see general health indicators 
'''
if st.checkbox('to the links '):
 '''
 - https://www.openicpsr.org/openicpsr/project/119446/version/V75/view;jsessionid=851ECB80E6CB42252D396C29564184DC) 
 - https://www.aecf.org/resources/2020-kids-count-data-book?gclid=CjwKCAiAudD_BRBXEiwAudakXyXtNK90IAicHQ5T3kT12l4TdJYfAQsYsHlMPNJLZnETp0XgshKE4xoC2UcQAvD_BwE
 - https://www.kff.org/coronavirus-covid-19/issue-brief/state-covid-19-data-and-policy-actions/'''




st.header('Libraries Used')

st.image('Libraries_Used.png')


st.header('Thank you all SPICED TEAM!')

st.image('Teachers.png')

'''  
- Tom Gatsby
- Paul Wlodkowski
- Stefan Roth
- Anastasia Mikheeva
- Career Team: Lindsay MCQuade
- Career Team: Olga Lavrenko 
- Administration Team: Anna Alongi
- Administration Team: Anne Luck
- Administration Team: Aniqua Fairooz


''' 

