
# Portfolio
This portfolio is designed to showcase my professional work and projects in data analytics and science, ranging from exploratory data analysis, visualisations, and machine learning in Python, R, SQL, Tableau, and Google Data Studio.

------
## Project Spotlight - Fraud Detection

Forthcoming

#### Libraries

- scikit-learn, pytorch

-------
## Project Spotlight - Financial Inclusion in Tanzania

#### Context

Financial inclusion means that individuals and businesses have access to useful and affordable financial products and services that meet their needs – transactions, payments, savings, credit and insurance – delivered in a responsible and sustainable way. It also facilitates day-to-day living, and helps families and businesses plan for everything from long-term goals to unexpected emergencies (WB).

However, there is an estimated 2 billion individuals who remain unbanked or underbanked, majority of whom are African and living in rural and isolate areas. The past 10 years have seen a rapid growth in the mobile money market as financial institutions continue to invest, opening up new channels of development in mobile money applications that deiver financial services services through mobile phone networks. 

Given that there are currently 2.6 billion smartphone subscriptions globally — a number that’s expected to hit 6.1 billion by 2020, it might be helpful to try understand the decision mechanisms that drive mobile money adoption. Thus findings from this analysis could help increase penetration in unbanked/underbanked markets across Tanzania and rest of Africa (i.e. increase financial inclusion by decreasing the number of unbanked).

#### Objectives

Using data on mobile money use of individuals in Tanzania, as well as spatial data on financial access points, we try to predict mobile money use by classifying each individual into four mutually exclusive categories:

0. No_financial_services: Individuals who do not use mobile money, do not save, do not have credit, and do not have insurance
1. Other_only: Individuals who do not use mobile money, but do use at least one of the other financial services (savings, credit, insurance)
2. Mm_only: Individuals who use mobile money only
3. Mm_plus: Individuals who use mobile money and also use at least one of the other financial services (savings, credit/borrowing, insurance)

Additional questions of interest: 

1. What is the current take-up for financial products across different dimensions, i.e location, age, gender etc:
2. What variables appear the most correlated with the take-up?
3. What is the most common/important use for financial products?
4. Where is adoption most prevelant (region)?
4. The nearest distance to financial access points?
5. The number of financial access points within a specified radius?
 

#### Findings

![Map 1 - Financial Access - High Traffic Areas](https://github.com/chirpc/Portfolio/assets/10565766/9fd4d69a-4f9d-4337-82a5-fb5097a79545)
![Map 2 - Financial Access - Serviced Areas](https://github.com/chirpc/Portfolio/assets/10565766/39103a12-ec64-4677-99aa-ec5639da516c)
![Map 3 - Financial Access - Filling a Gap](https://github.com/chirpc/Portfolio/assets/10565766/52e64324-e6d2-4aa6-8564-1b0fc24a1ac1)
![Map 4 - Financial Access - Gaps in the Market](https://github.com/chirpc/Portfolio/assets/10565766/20f3004c-c66b-4073-8e74-895800c2b7a2)


#### Libraries

- scikit-learn, arcgis, geopy

------
## Project Spotlight - Hate Speech on Twitter

#### Context

Networks form the building blocks of any group of people, organisations, entities; basically anything that can be defined as having a relation. The most familiar of these networks are online social network platforms like Facebook, Instagram, Twitter, LinkedIn, etc., where a link between users is establised through a follow, a comment, a like, or a post. Online social media and associated social networks are increasingly becoming an important forum for public debate and influence of individual attitudes and behaviours. In many cases, the decisive actions required to tackle the complex and divisive issues that permeate society can been found in the perceptions and opinions of those with which these connections are formed.

#### Objectives

Similar to strategies used in network interventions that rely on the social interactions and relationships that individuals have with each other to facilitate a change in behaviour or promote the adoption of a new idea, this study will explore the nature of social networks in online discourses. Specifically in the discourses of the #Senekal, #Brackenfell and #PutSAFirst movements. Critical to the success of these intervention programmes is knowing and understanding the context of the problem as well as the the people, positions and groups that potentially influence the outcome. The main objectives of this analysis are therefore to:

1. Identify key persons of influence based on network properties; 
2. Detect group structures formed by persons sharing common goals, interests, or positions; and 
3. Delineate a process in which the spread and adoption of social behaviour is affected by the role or position of the person propagating the discourse. 

The report is organised as follows:

- Part I: Descriptive Analysis
- Part II: Community Analysis
- Part III: Positional Analysis
- Part IV: Diffusion Analysis

#### Findings

The #Senekal, #Brackenfell and #PutSAFirst movements exhibit similar descriptive properties. Online users in these networks are found to have a tendency or preferential attachment toward popular users. This means a significant proportion of engagements or interactions in the network are with or between those most prominent or central in the discourse. Users in this network also share tighter and closer bonds with each other than would be expected in a random network. In other words, users would rather communicate within a close knit group than to communicate with others outside those groups. This also indicates a greater likelihood of "echo chambers", where opposite or contradicting views never enter discussions and are easily dismissed. Naturally, this would limit the ability for ideas to be shared, information to be discredited, and perceptions to be changed. 

I explore the networks further using clustering methods and conduct positional analysis using feature based techniques to group users in similar positions or roles based on patterns of interactions and distinct features. Results from the analysis generally revealed 5 distinct clusters. Based on the users assigned to each cluster, I classified them as follows:

>Observer Role: Periphery users that are far away from the centre of the discourse and have little participation or involvement.
>
>Spreader Role: Bridge users that are connected to users in various positions and can easily spread information across the network.
>
>Activator Role: Active users that reply to tweets and have a high interaction and engagement with other users.
>
>Informer Role: Public users that have many followers, are publicly listed and have a high global tweet count.
>
>Leader Role: Popular users that receive many replies to tweets and interact with other important users.

The users assigned to each of these roles were fairly consistent across the networks. Typically, members of political parties were positioned in the *Leader* role, and news agencies in the *Informer* role. The most active voices in the discourse, sharing the most tweets, were usually outliers assigned to the *Activator* role, while the least active and most distant were users in the *Observer* role. Active users who held positions in the network that connected distant users were classified in the *Spreader* role.

![Senekal - Indegree](https://github.com/chirpc/Portfolio/assets/10565766/fbec4f26-e86d-4fc2-a3d3-59c8e60de235)
![Senekal - Outdegree](https://github.com/chirpc/Portfolio/assets/10565766/7877e306-963d-4f1c-a100-f630f0fa3b14)
![Senekal - Word Cloud](https://github.com/chirpc/Portfolio/assets/10565766/193651fc-106f-4314-88b9-1e33cb06a939)
![Senekal - Role Players](https://github.com/chirpc/Portfolio/assets/10565766/df37090b-6dde-40a1-a9c7-833f8afd7b07)
![Senekal - Leader Cloud](https://github.com/chirpc/Portfolio/assets/10565766/0e7ec391-c2e4-40da-87d1-447a64a1f3c1)
![Senekal - Informer Cloud](https://github.com/chirpc/Portfolio/assets/10565766/a009cdda-5045-416c-91a5-5654da090f9f)

#### Libraries

- networkx, iGraph, scikit-learn, ndlib, dynetx