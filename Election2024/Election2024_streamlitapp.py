import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid

st.title("Election 2024 Analytics")
st.write("This Project involves EDA of election 2024 dataset from election portal (sourced github), providing insights on results on leading parties and trailing parties")

st.divider()


st.image('OIP.jpeg', caption='LokSabha Election 2024')

st.empty()
st.divider()


st.subheader("Glossary")
st.markdown("**:orange[Margin]**: The margin in an election context is the difference in votes between the winning candidate and the runner-up. It represents how many more votes the winning candidate received compared to the candidate with the second-highest number of votes.")
st.markdown("**:green[Constituency]**: A constituency is a geographic area represented by a member of a legislative body, such as a parliament or assembly. In an election context, it refers to the area where voters elect a representative.")
st.markdown("**:violet[Leading Party]**: The leading party is the party that is ahead in the election results, either in terms of the number of seats won, total votes received, or other relevant metrics.")
st.markdown("**:blue[Trailing Party]**: The trailing party is the party that is behind in the election results compared to others. It typically refers to parties with fewer seats or votes than the leading parties.")

st.divider()

st.subheader("Data Preview")
data = pd.read_csv('C:\\Users\\Asus\\sreamlitprojects\\election_results_2024.csv')
st.write(data.head(15))

party_votes = data.groupby('Leading Party')['Margin'].sum().sort_values(ascending=False)
data['Margin'] = pd.to_numeric(data['Margin'], errors='coerce')  #ensuring numeric

# Party with highest and lowest margin of victory
highest_margin = data.loc[data['Margin'].idxmax()]  #row-wise
lowest_margin = data.loc[data['Margin'].idxmin()]

party_votes = data.groupby('Leading Party')['Margin'].sum().sort_values(ascending=False)
party_votes = pd.to_numeric(party_votes, errors='coerce') # Convert party_votes to numeric
leading_party_highest_votes = party_votes.idxmax()
leading_party_lowest_votes = party_votes.idxmin()
# Number of seats won by each party
seats_won = data['Leading Party'].value_counts()
# Plotting number of seats won by each party
plt.figure(figsize=(20, 8))
sns.barplot(x=seats_won.index, y=seats_won.values, palette='viridis')
plt.title('Number of Seats Won by Each Party')
plt.xlabel('Party')
plt.ylabel('Seats Won')
plt.xticks(rotation=90)
plt.show()

st.divider()

st.subheader("Highest Margin Victory")
st.empty()

st.markdown(f"Party with highest margin of victory: :orange[{highest_margin['Leading Party']}] with a margin of :rainbow[{highest_margin['Margin']}]")
st.markdown(f"Party with lowest margin of victory: :orange[{lowest_margin['Leading Party']}] with a margin of :rainbow[{lowest_margin['Margin']}]")

st.bar_chart(data=seats_won)
with st.expander("See explanation"):
    st.write('''
A bar chart illustrating the margin of victory for the candidate with the highest margin and the candidate with the lowest margin of victory, showing the range of electoral wins.''')


rahul_entries = data[data['Leading Candidate'] == 'RAHUL GANDHI']
modi_entries = data[data['Leading Candidate'] == 'NARENDRA MODI']
amit_entries = data[data['Leading Candidate'] == 'AMIT SHAH']

# Get the votes for Rahul Gandhi, Narendra Modi, and Amit Shah
rahul_votes = rahul_entries['Margin'].values
modi_votes = modi_entries['Margin'].values[0] if not modi_entries.empty else 0
amit_votes = amit_entries['Margin'].values[0] if not amit_entries.empty else 0

# Get the original constituency names for Rahul Gandhi
rahul_constituencies = list(rahul_entries['Constituency'])

# Get the original constituency name for Narendra Modi
modi_constituency = modi_entries['Constituency'].values[0] if not modi_entries.empty else "Modi Constituency"

# Get the original constituency name for Amit Shah
amit_constituency = amit_entries['Constituency'].values[0] if not amit_entries.empty else "Amit Shah Constituency"

# Combine the data
data_to_plot = pd.DataFrame({
    'Candidate': ['Rahul Gandhi'] * len(rahul_votes) + ['Narendra Modi', 'Amit Shah'],
    'Constituency': rahul_constituencies + [modi_constituency, amit_constituency],
    'Votes': list(rahul_votes) + [modi_votes, amit_votes]
})

# Plot the comparison
plt.figure(figsize=(12, 6))
sns.barplot(data=data_to_plot, x='Constituency', y='Votes', hue='Candidate', palette='muted')
plt.title('Comparison of Votes for Rahul Gandhi, Narendra Modi, and Amit Shah')
plt.xlabel('Constituency')
plt.ylabel('Votes')
plt.xticks(rotation=45)
plt.show()

st.divider()

st.subheader("Comparison of Votes")

st.bar_chart(data=data_to_plot)
with st.expander("See explanation"):
    st.write('''
        A bar chart comparing the number of votes received by Rahul Gandhi, Narendra Modi, and Amit Shah across different constituencies.
    ''')

data['Margin'] = pd.to_numeric(data['Margin'], errors='coerce')
highest_margin_entry = data.loc[data['Margin'].idxmax()]
lowest_margin_entry = data.loc[data['Margin'].idxmin()]


st.divider()
# Combine the data
data_to_plott= pd.DataFrame({
    'Candidate': [highest_margin_entry['Leading Candidate'], lowest_margin_entry['Leading Candidate']],
    'Party': [highest_margin_entry['Leading Party'], lowest_margin_entry['Leading Party']],
    'Margin': [highest_margin_entry['Margin'], lowest_margin_entry['Margin']]
})


st.subheader("Highest Margin Entry and Lowest Margin Entry Leading Party")
st.empty()
st.write(data_to_plott)

st.divider()
data_to_plott['Margin'] = pd.to_numeric(data_to_plott['Margin'], errors='coerce')
# Plot the comparison


st.subheader("Margin Of Victory")

plt.figure(figsize=(10, 6))
sns.histplot(data['Margin'], bins=20, kde=True)
plt.title('Histogram of Margin of Victory')
plt.xlabel('Margin of Victory')
plt.ylabel('Frequency')
plt.show()

st.pyplot(plt)

with st.expander("See explanation"):
    st.write('''
        This bar chart visualizes the margin of victory for the candidates with the highest and lowest margin of victory in the dataset.
    ''')
st.divider()

st.subheader("Votes by Distribution")
party_votes = data.groupby('Leading Party')['Margin'].sum().sort_values(ascending=False)

# Plot pie chart
plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(party_votes, labels=None, autopct='%1.1f%%', startangle=140, wedgeprops=dict(edgecolor='w'))
plt.title('Votes Distribution by Party', pad=20)
plt.axis('equal')
plt.legend(labels=party_votes.index, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='medium')
plt.show()

st.pyplot(plt)
with st.expander("See explanation"):
    st.write('''
        This bar chart displays the total number of votes received by each party across all constituencies.
    ''')

st.divider()

trailing_party_votes = data.groupby('Trailing Party')['Margin'].sum().sort_values(ascending=False)
trailing_party_seats = data['Trailing Party'].value_counts()
plt.figure(figsize=(20, 6))

st.subheader("Top 10 trailing parties")
# Plot votes distribution by trailing party
plt.subplot(1, 2, 1)
sns.barplot(x=trailing_party_votes.index[:10], y=trailing_party_votes.values[:10], palette='viridis')
plt.title('Top 10 Trailing Parties by Votes')
plt.xlabel('Party')
plt.ylabel('Total Votes')
plt.xticks(rotation=45)

st.pyplot(plt)
with st.expander("See explanation"):
    st.write('''
This bar chart displays the ten parties with the fewest number of votes won in the election. ''')


st.divider()


st.subheader("Top 10 Trailing Parties by Seats")
plt.figure(figsize=(20, 6))
plt.subplot(1, 2, 2)
sns.barplot(x=trailing_party_seats.index[:10], y=trailing_party_seats.values[:10], palette='viridis')
plt.title('Top 10 Trailing Parties by Seats')
plt.xlabel('Party')
plt.ylabel('Number of Seats')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

st.pyplot(plt)
with st.expander("See explanation"):
    st.write('''
This bar chart displays the ten parties with the fewest number of seats won in the election. ''')
