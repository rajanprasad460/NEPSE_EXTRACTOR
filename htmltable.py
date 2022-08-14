def extracttable(link): 
    # Scrap the html page into tables if exists 
    # Trail to run a simple Python code
    # This module can work on other website as well, however, mainly prepared for Nepse Website [old]

    #The code starts form here

    # Trying to read a webpage
    # importing the urllib package

    from urllib import request
    import numpy as np
    import pandas as pd

    # importing regular expression module to match the expressions
    import re

    # The link of the webpage is defined here
    #link = 'http://www.nepalstock.com/main/floorsheet/index/9/?contract-no=&stock-symbol=&buyer=&seller=&_limit=50';


    # Reading the content of the webpage end_index = html.find("</title>")
    mypage = request.urlopen(link).read();
    #print(mypage)

    #type(mypage)
    # decoding byte to string
    mypage = mypage.decode("utf-8")
    #print(mypage)

    mypage2=mypage;

    # Extracting particular data of interest 
    start_index = mypage.find("<table>") + len("<table>")
    end_index = mypage.find("</table>")+ len("<table>")

    #print(start_index)
    #print(end_index)

    pattern1 = "<table.*?>.*?</table>"
    temp = mypage.replace("\n", " ");
    tabstr = re.findall(pattern1, temp)
    #tabstr

    if np.size(tabstr)<1:
        print('could not find start and end of tables');
        print('\n')
        #print('Or no table exist in the page')
    else:
        #print('The tables can be extracted')

        list3=[]; # Empty initialization to store all the table avaviliable inthe webpage
        count=0; # Counter initialization to count the number of tables
        # Check all the table to extract the data
        for r in np.arange(np.size(tabstr)):

            # Search in the selected table
            #Read content of the selected table
            mypage3 = tabstr[r];
            # patterns to identify rows, and cols
            pattern = "<tr.*?>.*?</tr>"
            # find rows of the tables
            substring = re.findall(pattern, mypage3)
            pattern2 = "<td.*?>.*?</td>"
            pattern3 = ">.*?<"
            list1=[]; # Empty initalization to store all rows of table (one complete table)
            # finding data for all rows 
            for i in np.arange(np.size(substring)):
                # inside a single row
                substringh = re.findall(pattern2, substring[i])
                list2=[]; # empty initialization to strore single rows of table
                str1='';
                # Find all data in a row ( all coloumns values)
                for j in np.arange(np.size(substringh)):
                    substring_C = re.findall(pattern2, substringh[j])
                    # finding the data of the index
                    data = re.findall(pattern3, substring_C[0])
                    #Combine all the array of data to find one data of the index
                    t_data = str1.join(data)    
                    t_data =re.sub("<","",t_data)
                    t_data =re.sub(">",'',t_data)
                    t_data =re.sub("&nbsp;","",t_data)
                    t_data =re.sub("|","",t_data)
                    if (t_data.strip()!=''):
                        k_data = t_data;
                        # appending into list containg array of a table
                        if (k_data.strip()!=''):
                            list2.append(k_data)
                        else:
                            list2.append('N/A') 
                 # appending the list containing individual tables       
                list1.append(list2)    

            #append to list of all list (master)
            list3.append(list1)
            count = count+1;

        # Convert the list into panda dataframe or table
        listtables = []
        for m in np.arange(count):
            #df = pd.DataFrame(list3[m][2:],columns=list3[m][2]) # with col
            df = pd.DataFrame(list3[m][1:]) # without cols
            listtables.append(df)
            
            
    return list3,listtables,count