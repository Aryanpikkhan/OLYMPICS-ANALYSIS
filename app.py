import streamlit as st
import pandas as pd
import preprocessor,helpher
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events1.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df,region_df)

st.sidebar.header("OLYMPICS ANALYSIS")
st.sidebar.image("https://yt3.googleusercontent.com/ytc/AGIKgqM7OxmzrTI3jba7pPGb9uaWAOXtOBWBH7PH6FCoy-E=s900-c-k-c0x00ffffff-no-rj")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country_wise Analysis', 'Athlete wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helpher.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)


    medal_tally = helpher.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Performance")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Performance in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Medal Performance in " + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("Medal Performance in " + selected_country + " " + str(selected_year)+ " Olympics")




    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Cities")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Athelets")
        st.title(athletes)

    with col3:
        st.header("Nations")
        st.title(nations)


    nations_over_time  = helpher.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.header("Participating nations in Olympics")
    st.plotly_chart(fig)

    events_over_time  = helpher.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.header("Events over the years")
    st.plotly_chart(fig)

    events_over_time  = helpher.data_over_time(df,'Name')
    fig = px.line(events_over_time, x="Edition", y="Name")
    st.header("Athelets over the years")
    st.plotly_chart(fig)



    st.title("NO. of Event over time(Every sport)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates({'Year', 'Sport', 'Event'})
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)


    x=helpher.most_successful(df,selected_sport)
    st.table(x)



    #st.title("Most successful Athletes")

if user_menu == 'Country_wise Analysis':

    st.sidebar.title('Country wise analytsis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)


    country_df = helpher.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal_tally over the years")
    st.plotly_chart(fig)


    st.title(selected_country + " Heat map  over the years")
    pt = helpher.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helpher.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)

    fig.update_layout(autosize=False,width = 500,height = 500)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # x = []
    # name = []
    # famous_sports = ['Basketball',
    #                  'Judo',
    #                  'Football',
    #                  'Tug-Of-War',
    #                  'Athletics',
    #                  'Swimming',
    #                  'Badminton',
    #                  'Sailing',
    #                  'Gymnastics',
    #                  'Canoeing',
    #                  'Tennis',
    #                  'Modern Pentathlon',
    #                  'Golf',
    #                  'Softball',
    #                  'Archery',
    #                  'Volleyball',
    #                  'Synchronized Swimming',
    #                  'Table Tennis',
    #                  'Baseball',
    #                  'Rugby',
    #                  'Lacrosse',
    #                  'Polo',
    #                  'Cricket',
    #                  'Ice Hockey',
    #                  'Racquets',
    #                  'Motorboating',
    #                  'Croquet',
    #                  'Figure Skating',
    #                  'Jeu De Paume',
    #                  'Roque',
    #                  'Basque Pelota',
    #                  'Aeronautics']
    # for sport in famous_sports:
    #     temp_df = athlete_df[athlete_df['Sport'] == sport]
    #     x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    #     name.append(sport)
    #
    # fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=500, height=500)
    # st.title("Distribution of Age")
    # st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("weight plot")
    selected_sport = st.selectbox('Select a sport', sport_list)
    temp_df = helpher.weight_v_height(df,selected_sport)
    fig , ax = plt.subplots()
    x = temp_df['Weight']
    y = temp_df['Height']
    ax = sns.scatterplot(x)
    st.pyplot(fig)

    st.title("Men vs Women participation over the years ")
    final = helpher.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)











