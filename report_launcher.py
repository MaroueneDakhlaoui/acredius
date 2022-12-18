from matplotlib import pyplot as plt
from backend_functions import *
import seaborn as sns
import io
import base64

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
<h2>I-/ Data cleaning </h2>
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
over_30_table = over_30.to_frame().to_html(header=None, max_rows=10)
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
input_data = input_data.drop(labels=["Nombre de mois de la période 15", "Nombre de mois de la période 16"
    , "Nombre de mois de la période 17", "Nombre de mois de la période 18"]
                             , axis=1)

# ------ The CA Column------
# ------ First remarks ------
message = """<h2>b-/ The 'Chiffre d'affaire' Columns (15 => 18) </h2>  <p> As mentioned in section 1, three of the 
four years we are taking data for CA have a lot of missing values</p> <p id="important-remark-red">We can not just 
drop these columns, because the money turnover is an important indicator for credit risk prediction <br> As a start We 
can write a function to see how many rows have missing data in the four years together.</p> """
f.write(message)
# ------ How many CA are null in 4 years together ------
message = "<p>"
f.write(message)
message = null_in_four_years(input_data, "CA15", "CA16", "CA17", "CA18")
f.write(message)
# ------ Description, of The solution ------
message = "That is not too bad of a percentage, but we have to work through it. <br><br>For those rows, we have no " \
          "choice " \
          "but to drop them, the good news is that we have an idea for the remaining rows to have an inclusive data " \
          "about this column. <br><br> The idea is to develop a function that finds the most recent, " \
          "non-null money " \
          "turnover for each row and creates a column that takes that most recent value for all rows, " \
          "that way we will have an inclusive information regarding this variable for all remaining rows and we won't " \
          "have to lose much data.<br><br> After applying this function, we develop and apply another function that " \
          "casts " \
          "all variables of the new column for recent CA to str, removes all non-int characters, and then casts all " \
          "row values to floats with 2 decimals to have all the data as floats for the model " \
          "<br><br> ** Feel free to check the 'null_in_four years', 'keep_not_null_together', 'create_recent_variable'" \
          " and 'unique_stats' functions in backend_functions.py as they will be used a lot during this report **</p>"
f.write(message)
# ------ Applying the solution ------
# ------ Remove fields where CA is null for all four years ------
input_data = keep_not_null_together(input_data, "CA15", "CA16", "CA17", "CA18")
# ------ Creating and populating the recent_CA column ------
input_data = create_recent_variable(input_data, "CA15", "CA16", "CA17", "CA18", "CA")
# ------ Casting to all floats ------
input_data = make_float(input_data, "CA")
input_data.dropna(subset=['CA'], inplace=True)

# -------- THE CA EV Column --------
# ------ First remarks ------
message = """<h2>c-/ The 'Evolution Chiffre d'affaire' Columns (15 => 18) </h2>  <p> Similarly we have a lot of 
missing data in this<mark> very important </mark>column but the interesting finding here is that """
f.write(message)
# ------ Show how many rows are null in the four years ------
message = null_in_four_years(input_data, "EV_CA15", "EV_CA16", "EV_CA17", "EV_CA18") + \
          "which is a very small percentage, we can just drop the few rows that are null across all years</p> " \
          "<p>Similarly to what we did to the 'CA' variable, we will use these 4 columns to generate a column that " \
          "has information about the latest 'CA Evolution' for each row <br><br> After doing so, We find some columns " \
          "containing 'Na' or '-' values instead of Nan so we use the str replace function to replace those with Nan " \
          "before removing them (few occurrences ). <br><br> With the same function we remove the % sign and " \
          "whitespace, replace the comma with a dot for decimals before casting all rows of this column to a float " \
          "</p> "
f.write(message)
# ------ Only keep rows that have at least one value for this variable across the 4 years ------
input_data = keep_not_null_together(input_data, "EV_CA15", "EV_CA16", "EV_CA17", "EV_CA18")
# ------ Creating and populating the latest_CA_EV column ------
input_data = create_recent_variable(input_data, "EV_CA15", "EV_CA16", "EV_CA17", "EV_CA18", "CA_EV")
# ------ Some rows have Na or - instead of Nan, so we replace them to avoid errors in the future  ------
input_data['CA_EV'].replace('Na', np.nan, inplace=True)
input_data['CA_EV'].replace('-', np.nan, inplace=True)
# ------ Drop nan values  ------
input_data.dropna(subset=['CA_EV'], inplace=True)
# ------ Removing the percentage  ------
input_data['CA_EV'] = input_data['CA_EV'].str.replace('%', '')
# ------ Removing the white spaces  ------
input_data['CA_EV'] = input_data['CA_EV'].str.replace(' ', '')
# ------ Replace the comma with a dot for decimals  ------
input_data['CA_EV'] = input_data['CA_EV'].str.replace(',', '.')
# ------ Convert to float  and keep it as a percentage------
input_data['CA_EV'] = pd.to_numeric(input_data['CA_EV'])

# -------- THE EB Column --------
message = """<h2>d-/ The 'EBE' Columns (15 => 18) </h2>  <p> Upon inspecting the unique values inside this column, 
I noticed that there are rows that have EBE in a percentage, others in a margin of percentages, and the rest as raw 
numbers mostly indicating money <br><br> With a little bit of research I found that the that EBE (Excédent Brut 
d'Exploitation) is usually representated by the money value.<br><br>We have  """
f.write(message)
message = str(count_invalid_rows(input_data, "EBE(retraité des loyers de leasing) 15"))
f.write(message)
message = """Rows that cannot be cast to float (mostly they have the % symbol or erroneous entries<br><br>That is 
almost half of the data we have left and we can not afford to drop that much data.<br><br> To impute this column we 
need more business understading and a help from someone with a financial background to find a way in which we can 
clean the data without harming the model.<br><br> For now I will drop the column so that the model 
doesn't use it in its current condition """
f.write(message)
input_data = input_data.drop(labels=["EBE(retraité des loyers de leasing) 15", "EBE(retraité des loyers de leasing) 16"
    , "EBE(retraité des loyers de leasing) 17", "EBE(retraité des loyers de leasing) 18"]
                             , axis=1)

# -------- THE Marge EB Column --------
message = """<h2>e-/ The 'Marge EB' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Marge d'EBE 15", "Marge d'EBE 16", "Marge d'EBE 17", "Marge d'EBE 18")
f.write(message)
message = "<p>Meaning more than half of the data is missing during all years of this column, so we have no option but " \
          "to drop the column </p> "
f.write(message)
input_data = input_data.drop(labels=["Marge d'EBE 15", "Marge d'EBE 16", "Marge d'EBE 17", "Marge d'EBE 18"], axis=1)

# -------- THE Resultat Net Column --------
message = """<h2>f-/ The 'Resultat Net' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Resultat Net 15", "Resultat Net 16", "Resultat Net 17", "Resultat Net 18")
f.write(message)
message = """<p>We Can just drop those 3 rows and continue inspecting this column <br><br> We will get the recent " \
          "'Resultat Net' for each row in a new column. <br><br> When inspecting the unique values and their " \
          "occurences for this column we can see the values are mostly ranges of percentages (eg 0-5% or 15 - 20%), " \
          "just straight percentages (eg -32,77%), straight numbers (eg 3037) or strings ending in /n (eg 0%-5%/n )  " \
          "<br><br> There is a lot of data cleaning here to make sure all the percentages are in the same format:<br><br>
          - The same percentage interval is written differentely (eg 0-5% and 0%-5% ) so I remove the % and make the interval (a-b)<br><br>
            - Remove the /n at the end of intervals<br><br>
             - Remove Leading and trailing whitespaces with strip <br><br>
             - Split the value on the dash and convert the two resulting values to floats <br><br>
             - Calculate the median of the range by taking the average of the two values <br><br>
             - Return the median, rounded to 1 decimal place <br><br>
             - The result is the median of the interval (7.5 for 5-10%) or the raw value casted to float if the row wasn't an interval at the first place <br><br>
             <br><br> ** Feel free to check the 'convert_to_median' function in backend_functions.py **</p> """
f.write(message)

# Drop the rows where it's null in 4 years
input_data = keep_not_null_together(input_data, "Resultat Net 15", "Resultat Net 16", "Resultat Net 17",
                                    "Resultat Net 18")
# Create the recent resultat net column and populate it
input_data = create_recent_variable(input_data, "Resultat Net 15", "Resultat Net 16", "Resultat Net 17",
                                    "Resultat Net 18",
                                    "recent_resultat_net")
input_data['recent_resultat_net'] = input_data['recent_resultat_net'].str.replace(' ', '')
# ------ Drop rows where the value is exactly -  ------
input_data = input_data[input_data["recent_resultat_net"] != "-"]
# ------ CLEAN -  ------
# input_data=range_to_median(input_data,"recent_resultat_net")
input_data['recent_resultat_net'] = input_data['recent_resultat_net'].apply(convert_to_median)

# -------- THE Total bilan Column --------
message = """<h2>g-/ The 'Total Bilan' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Total Bilan 15", "Total Bilan 16", "Total Bilan 17", "Total Bilan 18")
f.write(message)
message = "<br><br> For this column then, we will not lose any data rows, As usual I get the most recent 'Total " \
          "Bilan' for each row. <br><br> By Inspecting the data inside this column, it is more straightforward than " \
          "the previous columns I checked: It has numeric money value floats currently need a little bit of cleaning." \
          "<br><br> - Cast all the column rows into str" \
          "<br><br> - Remove whitespaces with the replace function" \
          "<br><br> - Replace ',' with '.' for decimals" \
          "<br><br> - Remove alphabetical letters  if they exist" \
          "<br><br> - Cast all the column rows into float" \
          "<br><br> ** Feel free to check the 'process_bilan' function in backend_functions.py **"
f.write(message)
input_data = keep_not_null_together(input_data, "Total Bilan 15", "Total Bilan 16", "Total Bilan 17", "Total Bilan 18")
input_data = create_recent_variable(input_data, "Total Bilan 15", "Total Bilan 16", "Total Bilan 17", "Total Bilan 18",
                                    "bilan")
input_data["bilan"] = input_data["bilan"].apply(process_bilan)

# -------- THE Total BFRE Column --------
message = """<h2>h-/ The 'BFRE' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "BFRE 15", "BFRE 16", "BFRE 17", "BFRE 18")
f.write(message)
message = "<p>Meaning more than half of the data is missing during all years of this column, so we have no option but " \
          "to drop the column </p> "
f.write(message)
input_data = input_data.drop(labels=["BFRE 15", "BFRE 16", "BFRE 17", "BFRE 18"], axis=1)

# -------- THE Total BFRE Column --------
message = """<h2>i-/ The 'Capacité de remboursement (FCCR)' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Capacité de remboursement (FCCR) 15", "Capacité de remboursement (FCCR) 16"
                             , "Capacité de remboursement (FCCR) 17", "Capacité de remboursement (FCCR) 18")
f.write(message)
# We drop that one row missing in all years
input_data = keep_not_null_together(input_data, "Capacité de remboursement (FCCR) 15",
                                    "Capacité de remboursement (FCCR) 16"
                                    , "Capacité de remboursement (FCCR) 17", "Capacité de remboursement (FCCR) 18")
# We create the latest FCCR column and populate it
input_data = create_recent_variable(input_data, "Capacité de remboursement (FCCR) 15",
                                    "Capacité de remboursement (FCCR) 16"
                                    , "Capacité de remboursement (FCCR) 17", "Capacité de remboursement (FCCR) 18",
                                    "FCCR")

message = """<p> For this column the values are in the same condition as in the 'total_bilan' columns, we can just use
the process_bilan function to clean everything."""
f.write(message)
input_data['FCCR'] = input_data['FCCR'].apply(process_bilan)
input_data.dropna(subset=['FCCR'], inplace=True)

# -------- THE Fonds Propres Column --------
message = """<h2>j-/ The 'Fonds Propres' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Fonds Propres 15", "Fonds Propres 16", "Fonds Propres 17", "Fonds Propres 18")
f.write(message)
# We drop that one row missing in all years
input_data = keep_not_null_together(input_data, "Fonds Propres 15", "Fonds Propres 16", "Fonds Propres 17",
                                    "Fonds Propres 18")
# We create the latest FCCR column and populate it
input_data = create_recent_variable(input_data, "Fonds Propres 15", "Fonds Propres 16", "Fonds Propres 17",
                                    "Fonds Propres 18", "fond_propres")
message = """<p> For this column the values are in the same condition as in the 'total_bilan' columns, we can just use
the process_bilan function to clean everything."""
f.write(message)
input_data['fond_propres'] = input_data['fond_propres'].apply(process_bilan)
input_data.dropna(subset=['fond_propres'], inplace=True)

# -------- THE Fonds Propres Column --------
message = """<h2>k-/ The 'Fonds Propres / Total Bilan' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Fonds Propres / Total Bilan 15", "Fonds Propres / Total Bilan 16",
                             "Fonds Propres / Total Bilan 17", "Fonds Propres / Total Bilan 18")
f.write(message)
# We drop that one row missing in all years
input_data = keep_not_null_together(input_data, "Fonds Propres / Total Bilan 15", "Fonds Propres / Total Bilan 16",
                                    "Fonds Propres / Total Bilan 17", "Fonds Propres / Total Bilan 18")
# We create the latest FCCR column and populate it
input_data = create_recent_variable(input_data, "Fonds Propres / Total Bilan 15", "Fonds Propres / Total Bilan 16",
                                    "Fonds Propres / Total Bilan 17", "Fonds Propres / Total Bilan 18", "FP_TB")
message = "<p> For this column, the data inspections shows mostly percentages that need formatting (eg 13,82%/n) : " \
          "<br><br>- Replace ',' with '.' for decimals" \
          "<br><br>- Remove all the non int characters except '-' for negative percentage and '.' for decimals" \
          "<br><br>- Cast the result to a float" \
          "<br><br> *** Feel free to check the process_FP_TB function in backend_functions.py ***</p>"
f.write(message)
input_data['FP_TB'] = input_data['FP_TB'].apply(process_FP_TB)

# -------- THE Dettes Nettes / EBE Column --------
message = """<h2>l-/ The 'Dettes Nettes / EBE' Columns (15 => 18) </h2> """
f.write(message)
message = null_in_four_years(input_data, "Dettes Nettes / EBE(* années) 15", "Dettes Nettes / EBE(* années) 16",
                             "Dettes Nettes / EBE(* années) 17", "Dettes Nettes / EBE(* années) 18")
f.write(message)
message = "<p>Upon Inspecting the data for this column, we can see that it's a float indicator that need some formatting:" \
          "<br><br> - Replacing ',' with '.' for decimals." \
          "<br><br> - Removing all non int characters except '.' and '-'." \
          "<br><br> - Removing all whitespaces." \
          "<br><br> - Casting to Float. " \
          "<br><br> **** Feel free to check the process_dette_EBE function in backend_functions.py **** </p> "
f.write(message)
keep_not_null_together(input_data, "Dettes Nettes / EBE(* années) 15", "Dettes Nettes / EBE(* années) 16",
                       "Dettes Nettes / EBE(* années) 17", "Dettes Nettes / EBE(* années) 18")
input_data = create_recent_variable(input_data, "Dettes Nettes / EBE(* années) 15", "Dettes Nettes / EBE(* années) 16",
                                    "Dettes Nettes / EBE(* années) 17", "Dettes Nettes / EBE(* années) 18",
                                    "Dettes Nettes / EBE")
input_data.dropna(subset=['Dettes Nettes / EBE'], inplace=True)
input_data["Dettes Nettes / EBE"] = input_data["Dettes Nettes / EBE"].apply(process_dette_EBE)

# -------- Niveau de risque --------
message = """<h2>m-/ The risk level column </h2> """
f.write(message)
message = """<p>These are all the available risk levels in the data (A+, A, B+, B, C)
<br><br>I wrote a function to apply ordinal encoding on this column: assign numerical values to the categories based 
on their ordinal relationship. In this case,  the value 1 to category A+, 2 to category A, 3 to 
category B+, and so on, up to 5 for category C.<br><br> I chose this encoding method to create some bias in the model
 , As Risk categories should make some applicants better/worse than others 
 <br><br> **** Feel free to check encode_risk_levels function in backend_functions.py **** <p>"""
f.write(message)
input_data = encode_risk_category(input_data, "Niveau de risque")

# -------- Effectifs --------
message = """<h2>n-/ The Effectifs (head count) column </h2> """
f.write(message)
message = """<p>For the head count column, it might be more be suitable to use one hot encoding
<br><br> Does a high head count of an applicant company make it better than others?
<br><br> To answer this question I tried two encoding methods: One hot encoding (Unbiased), and Label encoding (Biased).
<br><br> Before Applying the encoding, I cleaned the levels a little by removing some extra characters and unifying the format.
<br><br> Later When checking the model performance, I tried both approaches and the country columns gave better when encoded with bias.
 <br><br> **** Feel free to check process_head_count (2 versions), encode_HC (2versions)
  and get_first_number functions in backend_functions.py **** <p>"""
f.write(message)
input_data["effectifs"] = input_data["effectifs"].apply(process_head_count_2)
input_data = input_data[input_data['effectifs'] != '']
input_data["effectifs"] = input_data["effectifs"].apply(get_first_number)
input_data = label_encode(input_data, "effectifs")

# input_data = one_hot_encode(input_data,"effectifs")

# -------- Pays --------
message = """<h2>o-/ The 'Pays' column </h2> """
f.write(message)
message = """<p>There is no reason for me to introduce a bias to the model in terms of country, All I did here is 
 some data cleaning (removing whitespaces and /n) and One hot encoding the 4 available countries (France, Spain, Italy, and the 
 Netherlands).
 <br><br> **** Feel free to check process_pays function in backend_functions.py **** <p>"""
f.write(message)
input_data["Pays"] = input_data["Pays"].apply(process_pays)
input_data = one_hot_encode(input_data, "Pays")

# -------- Rest of the columns --------
message = """<h2>p-/ Rest of the columns </h2> """
f.write(message)
message = """<p>To not make this report longer than it already is, some of the remaining columns 
(eg Taux, Montant, Capital social) Were also processed by techniques and functions that are already discussed 
in this report (removing '%' '€' and whitespaces ).
<br><br>*** Feel free to check 'process_montant_ou_capital' and process_taux function in backend_funcrions.py ***.
<br><br> Other columns like Passif circulant had too many nulls values across the 4 years together.
<br><br> For time constraints I dropped these columns, it would be interesting to spend more
time investigating a proper solutions for them in the future.</p>"""
f.write(message)
input_data = input_data.drop(labels=["Passif circulant 15", "Passif circulant 16", "Passif circulant 17",
                                     "Passif circulant 18", "Actif immobilisé 15", "Actif immobilisé 16",
                                     "Actif immobilisé 17", "Actif immobilisé 18", "Actif circulant 15",
                                     "Actif circulant 16", "Actif circulant 17", "Actif circulant 18",
                                     "Dettes court terme 15", "Dettes court terme 16", "Dettes court terme 17",
                                     "Dettes court terme 18", "Dettes Moyen long terme 15",
                                     "Dettes Moyen long terme 16",
                                     "Dettes Moyen long terme 17", "Dettes Moyen long terme 18",
                                     "Dettes Nettes / Fonds propres 15", "Dettes Nettes / Fonds propres 16",
                                     "Dettes Nettes / Fonds propres 17", "Dettes Nettes / Fonds propres 18",
                                     "BFRE en nombre de jours de CA 15", "BFRE en nombre de jours de CA 16",
                                     "BFRE en nombre de jours de CA 17", "BFRE en nombre de jours de CA 18"], axis=1)

# Apply processing for montant et capital social
input_data["Montant"] = input_data["Montant"].apply(process_montant_ou_capital)
input_data["capital social"] = input_data["capital social"].apply(process_montant_ou_capital)
input_data["Taux"] = input_data["Taux"].apply(process_taux)
# ---------------------------------
# ------ create a dataframe containing a preview of data ------
# Drop a few rows where there null values (17 only)
input_data = input_data.dropna()

#######  EDA ################
message = """<h2>II-/ EDA </h2>"""
f.write(message)
# Calculate the correlation matrix
corr = input_data.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

# Save the heatmap to a buffer
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

# Encode the image data as a base64 string
image_data = base64.b64encode(buf.getvalue()).decode('utf-8')

# Write the HTML file
f.write('<img src="data:image/png;base64,{}" />'.format(image_data))
message = """<p> The correlation heatmap (Pearson) shows that our target is mostly correlated with the 'Risk level'.
<br><br>We can also deduct the non-linear relation between the target and the rest of the columns.
<br><br>For now I will just remove the encoded countries, the ID, and "emprunter" fields before modelling 
<br><br>We can plot use the feature's importance later to add to our deductions</p>"""
f.write(message)
initial_model_df = input_data.drop(labels=["ID", "Emprunteur", "Pays", "France", "Espagne", "Pays-Bas", "Italie"],
                                   axis=1)
initial_model_df.to_excel('clean_data.xlsx', index=True)

################  Modelling ################
message = """<h2>III-/ Modelling </h2>"""
f.write(message)
message = """<p>For reasons related to performance the code for the modelling part of this task can be found on this 
<a href="https://colab.research.google.com/drive/1Uih8AIc83iPL_DJ8VmSbIqcEl2FLjS_T?usp=sharingm">Google Collab Notebook.</a>
<br><br> Make sure to use this <a href="https://docs.google.com/spreadsheets/d/1wAGZVc24EVtZhkEHIJbECnFpdZeThkDK/edit?usp=sharing&ouid=107921434568511366033&rtpof=true&sd=true">Clean data</a>
and import it in the notebook.
<br><br> The notebook is well documented and you can find everything there but for the sake of this report, I will 
summarize the modelling part here.
<br><br> Since there is no linear relationship between the data columns, we can not consider a Linear Regressor.
 <br><br> I decided to go with a Random Forrest Classifier and an XGBoost for the following reasons:</p>"""
f.write(message)
message = """<p style="text-indent: 20px;"> - Random forests do not require feature scaling because the decision trees
that make up the forest are not sensitive to the scale of the features.</p>
<p style="text-indent: 20px;"> - They are robust to outliers in the input data and can handle non-linear relationships
 between features and the target variable Which is the case here!</p>
 <p style="text-indent: 20px;"> - They can be used to estimate the importance of different features in the prediction 
 task, which can be helpful for feature selection.</p>
 <p style="text-indent: 20px;"> - XGBoost is especially well-suited for structured data, such as that typically found 
 in financial datasets.</p>
  <p style="text-indent: 20px;"> - XGBoost combines the predictions of multiple "weak" models to create a single
 "strong" model. This can lead to improved accuracy and robustness compared to using a single model.</p>"""
f.write(message)

################  Evaluation ################
message = """<h2>III-/ Evaluation </h2>"""
f.write(message)
message = """
<table>
  <tr>
    <th>Model</th>
    <th>MSE</th>
    <th>Best actual</th>
    <th>Best pred</th>
    <th>Worst actual</th>
    <th>Worst pred</th>
  </tr>
  <tr>
    <td>RandomForest</td>
    <td>6.742833</td>
    <td>6.5</td>
    <td>6.364224</td>
    <td>0.07</td>
    <td>6.179379</td>
  </tr>
  <tr>
    <td>XGBOOST</td>
    <td>6.416491</td>
    <td>6.5</td>
    <td>6.364224</td>
    <td>0.07</td>
    <td>6.179379</td>
  </tr>
  <tr>
    <td>XGBOOST+Optuna</td>
    <td>7.653989</td>
    <td>6.5</td>
    <td>6.364224</td>
    <td>0.07</td>
    <td>6.179379</td>
  </tr>
</table>
"""
f.write(message)
message=""" <p> As observed, the models all performed closely, it did great on some rates predicting almost exactly
 correct, while being off on others. <br> <br> The problem here is that during the data cleaning phase, I lost 
 a lot of data, especially columns that are financially important to this case study (eg actifs courant,Dettes..).
  <br> <br> with more time, and more data, it would be interesting to improve this model more and more.</p>"""
f.write(message)
# ------ Finished with writing the html file, so close it and open the browser ------
f.close()
webbrowser.open_new_tab("output.html")
# input_data = input_data.reset_index()
