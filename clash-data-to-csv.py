
# coding: utf-8

## Clash of Clans Data To CSV

# In[5]:

import pandas as pd
import requests
import re
import os


# In[6]:

def get_name_to_link(url, attribute_class):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    table = soup.find('table', attrs={"class":attribute_class})
    name_to_link = {}
    
    for row in table.findAll('tr'):
        columns = row.findAll('td')
        if (columns):
            category_link = columns[0].find('a')
            links = columns[1].findAll('a');   
            for link in links:
            
                name = link['title'].lower().replace(' ', '_').replace('/', '_').replace("'", '').replace('.','')
                name_to_link[ name ]= link['href']
    return name_to_link
troop_name_to_link = get_name_to_link('http://clashofclans.wikia.com/wiki/Troops', "article-table")

print troop_name_to_link


# In[7]:

def get_name_to_page(name_to_link):
    name_to_page = {}
    for name, link in name_to_link.iteritems():
        print name
        url = 'http://clashofclans.wikia.com' + link
        page = requests.get(url).text
        name_to_page[name] = page
    return name_to_page

troop_name_to_page = get_name_to_page(troop_name_to_link)


# In[8]:

def replace_column_names(table, regex, replace_with):
    column_name_list = table.columns.tolist()

    new_column_names = []
    for column_name in column_name_list:
        new_column_name = re.sub(regex, replace_with, column_name)
        new_column_names.append(new_column_name)
    table.columns=new_column_names
    return table


# In[9]:

def get_name_to_table( regex, name_to_page):
   
    name_to_table = {}
    column_replace_regex = '<img.*?>'
    column_replace_with = ''
    
    for name, page in name_to_page.iteritems():
        print 'name='+str(name)
        soup = BeautifulSoup(page, "html.parser")
    
        table_list = pd.read_html(page, match=regex, header=0 )
        if len(table_list) > 0 :
            table = table_list[0]   
            table = replace_column_names(table, column_replace_regex, column_replace_with)
            name_to_table[name] = table

    return name_to_table

meta_regex = re.compile('Preferred|Radius')
meta_name_to_table = get_name_to_table(meta_regex, troop_name_to_page)
print meta_name_to_table['barbarian'].columns.tolist()
print '----'
level_regex = re.compile('Hitpoints|Total|Duration|Freeze Time|Increase')
level_name_to_table = get_name_to_table(level_regex, troop_name_to_page)
print level_name_to_table['barbarian'].columns.tolist()
print '----'

#print meta_name_to
#print meta_name_to_table
#print '----'
#print level_name_to_table


# In[10]:

if not os.path.exists('csv'):
    os.makedirs('csv')
    
for name, table in meta_name_to_table.iteritems():
    sanitized_name = 'meta_' + name
    print sanitized_name
    table.to_csv( path_or_buf='csv/' + sanitized_name  + '.csv', encoding='utf-8')
    
print'---meta csv done---'


for name, table in level_name_to_table.iteritems():
    sanitized_name = 'level_' + name
    print sanitized_name
    table.to_csv( path_or_buf='csv/' + sanitized_name  + '.csv', encoding='utf-8')
    
print '---levels csv done---'
#for name, table in level_name_to_table.iteritems():
#    table.to_csv( path_or_buf='csv/level_' + name + '.csv')
    


# In[10]:



