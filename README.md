# Job Postings Project; Experimenting with Dash by Plotly

Back in August of 2019 I became interested in identifying which technical skills would set me up for specific career paths. Of course, a simple Google search can answer the question, "What skills do I need for job X?" but this approach doesn't answer the question that I -- along with many other students -- truly care about, "Is job X right for me?". 

Career postings websites like Indeed and LinkedIn do a tremendous job of matching job postings to the right candidates, but I wanted to explore how these algorithms are created, and why they make sense.

This Job Postings Project is my attempt at creating my own job postings matching algorithm which displays the information in a dashboard format. Technically, I'm attempting to re-create common algorithms employed by sites like Indeed and LinkedIn in order to better understand what actually constitutes a satisfactory job match.

# Methodology

I began by scraping Indeed job postings in September 2019 on a weekly basis using Python and Selenium. The program looks for all 'Analyst' roles within 75km of Toronto with no other specifications to narrow down the search. I plan to expand the searching mechanism to include 'developer' and 'consultant' jobs in order to get a broader range of careers, but it should be noted that the 'Analyst' search does return a fair number of 'developer' and 'consultant' jobs. I collected the job title, company, location, link to the posting, and the job description for each unique posting. Each weekly scrape consists of roughly 1,300 to 1,800 job postings.

From these, I search the descriptions of each posting to determine whether a skill is mentioned, then count how many postings mention that skill. I.e. for the week of December 28th, there were 283 unique job postings on Indeed that mentioned 'SQL' as a requirement or 'nice-to-have' skill, whereas there were only 75 that mentioned 'Python'. The same process is carried out for common certifications. 118 job postings mention the 'CPA' whereas 38 mention the 'CFA' for that week. 

Once I had three months of weekly scrapes highlighting the number of skill mentions for 'Analyst' roles I moved onto visualizing this information in an interactive way. The dashboard offers the ability to explore a checklist of skills/certifications to see how they change over time (i.e. are they becoming more or less popular over time?). Again, this question can be solved by a simple Google search, but it is still informative and useful to quickly explore these 'popularity' changes over time.

The first tab consists of seven callbacks. The checklist boxes update which skills are shown. The first dropdown changes the graph to display either skills or certifications. The second dropdown displays either the base graph (first seven options of the skills or certifications category), the highest percentage change, or the highest average value. The first dropdown also updates the bar chart to show the top skills or certifications.

![](https://media.giphy.com/media/LT65LPO9wYfTGNShaW/giphy.gif)


![alt text](https://i.pinimg.com/originals/9e/a2/2b/9ea22bbd919c690db6de78771ac1d59a.png)





# Expanding the app to encompass school progress

The second tab of the Dash app looks at my academic progress for the Fall 2019 school semester. I wanted a way to visualize my grades as assignments/test grades came out so that I can ensure I'm on the right track throughout the semester. I plan to expand this tab to serve as a full academic dashboard that can present all useful school information (deadlines, study guides, documents) on one page.


![](https://media.giphy.com/media/hs1mHsZbPhnoApZFXe/giphy.gif)


![alt text](https://i.pinimg.com/originals/1c/7d/56/1c7d56fc335d89424b61071e9291061a.png)



# Next Steps

The app is still in very early stages. I plan to add several more features that I hope could make this a useful website for keeping track of job applications and school progress. 

## Tab one plans
- data table that returns jobs with selected skills of interest.
- option to export the data table to excel to easily keep track of job applications.
- resume parser that matches a list of job postings to an uploaded resume based on mentioned skills and experience.
- job application progress tracker.

## Tab two plans
- scrape intranet site containing all relevant semester information (deadlines, assignments, tests, weights, weekly objectives, etc.).
- create progress tracker for each class.

## Overall plans
- deploy app to Heroku, allow user access and caching of information.













