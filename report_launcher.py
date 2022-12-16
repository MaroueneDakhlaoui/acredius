from backend_functions import *

# ------ Hello there, this python script is meant to generate the output report of this task in an HTML format ------
# ------ If you are reviewing the code structure, I would advise you to check the 'backend_functions.py' file ------
# ------ If you still want to check this out though, you are more than welcome to do so, I will try to guide you
# through the sections of this code ------

input_data = data_reader()  # <--- Read the data
input_data = columns_rename(input_data)
f = open('output.html', 'w')  # <--- Initialize an HTML file that will generate the report
# ------ The message variable will hold the html elements we want to add to our report ------
message = """<html>
<link rel="stylesheet" href="main.css">
<script src="main.js"></script>
<title> Marouene Dakhlaoui- Acredius case-study </title>
<body>
<h1> Marouene Dakhlaoui-Acredius Case Study! </h1>
<h2>I-/ Exploratory data analysis </h2>
<p>First things first let's look at the data</p>
</body>
</html>"""
# ------ Everytime we finish building the message attribute we write it to the HTML file ------
f.write(message)
# ------ create a dataframe containing a preview of data ------
data_head = data_head(input_data)
# ------ Export to an HTML table ------
data_head_table = data_head.to_html(max_cols=8)
# ------ Write the table to the html file ------
f.write(data_head_table)
# ------ The message variable  ------
message = "<br><br> <strong> The shape of the dataframe is: "
f.write(message)
message = str(input_data.shape)
f.write(message)
message = "</strong> "
f.write(message)
message = "<p>I have only printed an 8 by 8 mini version of the dataframe for clarity in this report, but I have went " \
          "through more inclusive version of the dataframe. </p> <h2> 1-/ Null values </h2> " \
          "<p>Let's check the percentages of null and empty values for each column</p> <p>In doing so we create two " \
          "pandas series, One for columns that have 30% or more missing values, and another for columns with less " \
          "than 30% missing values</p> "
f.write(message)

message = "</p>"
f.write(message)
# ------ Writing the content to the file  ------
f.write(message)
# ------ create a dataframe for columns having more than 30% null values ------
over_30 = describe_data_pipeline(input_data)['over_30']
# ------ Export to an HTML table ------
over_30_table = over_30.to_frame().to_html(header=None)
# ------ Write the table to the html file ------
f.write(over_30_table)
message = "<br> <br>"
f.write(message)
# ------ Display the size of the series to have a better idea on how many columns have more than 30% missing data ------
message = size_of_series(over_30)
f.write(message)
# ------ Data cleaning section ------
message = "<p>In the following sections we will decide what to do with these Null values based on the business need " \
          "and importance the column </p> "
f.write(message)
# ------ Cleaning the nombre de la periode columns ------
message = "<h2>a-/ The 'Nombre de mois de la période' Columns (15 => 18) </h2>" \
          "<p> Let's explore the different unique values of these variables from 2015 to 2018 and their occurrences</p>"
f.write(message)
period_15_unique = unique_stats(input_data['Nombre de mois de la période 15'])
period_15_unique_table = period_15_unique.to_frame().to_html()
period_16_unique = unique_stats(input_data['Nombre de mois de la période 16'])
period_16_unique_table = period_16_unique.to_frame().to_html()
period_17_unique = unique_stats(input_data['Nombre de mois de la période 17'])
period_17_unique_table = period_17_unique.to_frame().to_html()
period_18_unique = unique_stats(input_data['Nombre de mois de la période 18'])
period_18_unique_table = period_18_unique.to_frame().to_html()
f.write(period_16_unique_table)
f.write(period_17_unique_table)
f.write(period_15_unique_table)
f.write(period_18_unique_table)
message = "<p> We can see a lack of variability in this column, most of the data is either 12 months or missing (with " \
          "some exception), this applies to this column for the four years from 2015 to 2018 </p> "
f.write(message)
message = """<p id="important-remark"> We can safely conclude that these variables will not contribute to any target 
and can be removed from our dataset </p> """
f.write(message)
# ------ Cleaning the Chiffre d'affaire columns ------
# ------ First remarks ------
message = """<h2>a-/ The 'Chiffre d'affaire' Columns (15 => 18) </h2>  <p> As mentioned in section 1, three of the 
four years we are taking data for CA have a lot of missing values</p> <p id="important-remark-red">We can not just 
drop these columns, because the money turnover is an important indicator for credit risk prediction <br> As a start We 
can write a function to see how many rows have missing data <mark>in the four years together</mark></p> """
f.write(message)
# ------ How many CA are null in 4 years together ------
message = "<p>"
f.write(message)
message = null_in_four_years(input_data, "CA15", "CA16", "CA17", "CA18")
f.write(message)
# ------ Description, of The solution ------
message = "That is not too bad of a percentage, but we have to work through it. <br>For those rows, we have no choice " \
          "but to drop them, the good news is that we have an idea for the remaining rows to have an inclusive data " \
          "about this column <br> The idea is to develop a function that <mark> finds the most recent, non-null money " \
          "turnover for each row </mark> and creates a column that takes that most recent value for all rows, " \
          "that way we will have an inclusive information regarding this variable for all remaining rows and we won't " \
          "have to lose much data.<br> After applying this function, we develop and apply another function that casts " \
          "all variables of the new column for recent CA to str, removes all non-int characters, and then casts all " \
          "row values to floats with 2 decimals to have all the data as floats for the model </p> "
f.write(message)
# ------ Applying the solution ------
# ------ Remove fields where CA is null for all four years ------
input_data = keep_not_null_together(input_data, "CA15", "CA16", "CA17", "CA18")
# ------ Creating and populating the recent_CA column ------
input_data = create_recent_variable(input_data, "CA15", "CA16", "CA17", "CA18")
# ------ Casting to all floats ------
input_data = clean_column(input_data, "recent_CA")
input_data.dropna(subset=['recent_CA'], inplace=True)
# ------ Cleaning the 'Evolution de chiffre d'affaire' columns ------
# ------ First remarks ------
message = """<h2>b-/ The 'Evolution Chiffre d'affaire' Columns (15 => 18) </h2>  <p> Similarly we have a lot of 
missing data in this<mark> very important </mark>column but the interesting finding here is that """
f.write(message)
# ------ Show how many rows are null in the four years ------
message = null_in_four_years(input_data, "EV_CA15", "EV_CA16", "EV_CA17", "EV_CA18") + \
          "which is a very small percentage, we can just drop the few rows that are null across all years</p>"
f.write(message)
# ------ Only keep rows that have at least one value for this variable across the 4 years ------
input_data = keep_not_null_together(input_data, "EV_CA15", "EV_CA16", "EV_CA17", "EV_CA18")


# ------ Finished with writing the html file, so close it and open the browser ------
f.close()
webbrowser.open_new_tab("output.html")
