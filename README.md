The main targets in this project were:
1. Learn how to use an API in order to extract data from a website (Alphavintage, Bitcoin TimeSeries data)
2. Scrape information from a website (u.today -> Articles related to Bitcoin)
3. Host both datasets in a PostgreSQL database (Supabase)
4. Build a regular update cycle for both datasets by using AWS Lambda functions (Connecting functions with Eventbridge, Setting Data Trigger)  
5. Display the data in a user-friendly way as a streamlit app



All in all, I perceived the setup of the whole environment as quite complex and hence quite taxing.
In stark contrast to previous assignments, this project required a significant amount of debugging.    
However I'm happy with the result. 
I enjoyed researching into stock market analysis and which graphs to use (e.g. candle stick chart).  
If you want to try the app, then use the link below:
https://btc-scraping.streamlit.app/


My Learnings and key takeaways:
I have respect for people who focus on AWS data engineering. 
I gained a solid understanding of the fundamentals of how to organize and/or structure data pipeline and regular refresh patterns.
It was also good to realize that database table settings in Postgres environment can help to avoid duplicate appearance of records. I.e. avoid to collect information of the same news article twice by using date and title as composite primary key.
I can recommend the following article, which helped me to refresh my stock market knowledge and how to make best use of a certain type of chart.
https://www.schwab.com/learn/story/how-to-read-stock-charts-and-trading-patterns
