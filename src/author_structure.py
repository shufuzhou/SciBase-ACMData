import re
import json
import unicodedata

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('_',' ',text)
    return text

def initialize():
    global country_list

    temp_list = open("./Sorting References/all_countries.txt","r").read().split('\n')
    country_list = [ text_to_id(i.split('|')[1]) for i in temp_list]


def get_country(astring):
    global country_list
    for country in country_list:
        if country in astring:
            return country

    return None


def get_values(arecord):
    author_dict = {}
    author_dict['Name'] = arecord['name']
    if arecord['affiliation']!=None:
        author_dict['university'] = arecord['affiliation']
        author_dict['country'] = get_country(arecord['affiliation'])
    else:
        author_dict['university'] = None
        author_dict['Country'] = None

    return author_dict

country_list = []
initialize()

journal_list = []

with open('../data/ACM_Journal_list.csv','r') as infile:
    lines = infile.read().split('\n')
for line in lines:
    jname = line.split(',')[2]
    journal_list.append(jname)

for journal_name in journal_list:
    journal_dict = {}
    try:
        with open('../output/Journal Data/'+journal_name+'.json','r') as infile:
            journal_dict = json.load(infile)
    except FileNotFoundError:
        print('File Not Found : '+journal_name)
        continue
    volume_dict = {}
    for volume in journal_dict[journal_name]['Volumes']:
        issue_dict = {}
        for issue in journal_dict[journal_name]['Volumes'][volume]:
            article_dict = {}
            for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
                authors_data_list = []
                for author in journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['affiliation_data']:
                    authors_data_list.append(get_values(author))
                article_dict[article] = authors_data_list
            issue_dict[issue] =article_dict
        volume_dict[volume] = issue_dict


    final_dict = {'Volumes':volume_dict}

    with open('../output/Article_Author_data/'+journal_name+'.json','w') as outfile:
        json.dump(final_dict,outfile)