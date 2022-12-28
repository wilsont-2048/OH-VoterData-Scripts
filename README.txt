Method:


To pull voter file data, and to overcome Cloudflare's anti-bot defense found in the Ohio Secretary of State Website, the python package “cloudscrapper” was used to impersonate requesting the files from a web browser such as Google Chrome.


To match the data from the OH SOS website to the given input data, I decided to match each row based on three possible criteria: last name, first name, birth year or postal code. I prioritized last name since both data sets did not have many empty gaps in last name data and I believe this could provide the best preliminary one-to-one match possible. Splitting the full name to only last name strings in the input file helped to achieve this when using the inner join procedure with both data sets.


To further narrow down the matches, only matches that had the same first name were left in the data set. Finally, matches that had the same birth year or zip code were left in the final data set since this was the best possible additional data I had to match a voter based on personal information or geographic location.




Further Improvements:


Each data file obtained from the website is currently saved as data1.txt, data2.txt, and so on. Ideally, it would be best if each file were properly identified by the county name it corresponds to. Using a dictionary could help to achieve this in the future.


Ideally, each record should be precisely matched to a voter record from the SOS website. But using the current method of including matches by zip code or birth year it is possible duplicate matches are given. For example, two records that have the same name and the same zip code would be duplicate matches since it is not currently possible to further narrow down by address.


There are also names in the input file that only have the first initial of a name. This leaves out possible matches where every other field matches with the input data except for a first name. This can possibly be addressed by creating a method that checks for every other field first and matches a record based on this criteria.