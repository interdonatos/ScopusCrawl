import pandas as pd
from pybliometrics.scopus import ScopusSearch

from pybliometrics.scopus import init
init()
#from pybliometrics.scopus  import create_config
#create_config()

#key = '5960f63c0f529e02a1d0a897e2c7a1cb'

#InstToken = '5695e567e557e78d6be40262be2b6a24'


def textToQueryList(text):
    lista = []
    vals = text.split(',')
    for v in vals:
        if len(v.strip().split(' '))>1:
            lista.append("{%s}" % v.strip())
        else:
            lista.append(v.strip())
    query = "("
    for t in range(len(lista)-1) :
        query+=lista[t]+" OR "
    query+=lista[len(lista)-1]+")"
    return query

def textToList(text):
    lista = []
    vals = text.split(',')
    for v in vals:
        if len(v.strip().split(' '))>1:
            lista.append("{%s}" % v.strip())
        else:
            lista.append(v.strip())
    return lista



def print_list_query(liste):
    title_search_query = ''
    for w in liste:
        if len(w.split(' '))>1:
            title_search_query += "{"+w.lower().strip() + '} OR '
        else:
            title_search_query+=w.lower().strip()+' OR '
    print(title_search_query)

def main_crawling(suffix):
    #os.chdir("D:\\Mes Donnees\\CharlottePlastic\\")

    title_queries = True

    terms_path = './data/sn_list.txt'

    # Read terms from a text file into a list
    with open(terms_path, "r") as f:
        terms = [line.strip() for line in f if line.strip()]

    print(terms)
    if title_queries:
        #title_search_12 = "TITLE%s AND TITLE%s AND (PUBYEAR > 1950) AND (PUBYEAR < 2010)" % (liste_1,liste_2)
        #title_search_13 = "TITLE%s AND TITLE%s AND (PUBYEAR > 1950) AND (PUBYEAR < 2010)" % (liste_1,liste_3)
        #title_search_123 = "TITLE%s AND TITLE%s AND TITLE%s AND (PUBYEAR > 1950) AND (PUBYEAR < 2010)" % (liste_1,liste_2,liste_3)
        #title_search_12 = "TITLE%s AND TITLE%s" % (liste_1,liste_2)
        # Build query
        title_query = " OR ".join([f"TITLE({kw})" for kw in terms])

        # COMP Computer Science
        # MATH Mathematics (covers stats, ML theory)
        # ENGI Engineering
        # DECI Decision Sciences (covers data analysis)

        subject_filter = "SUBJAREA(COMP) OR SUBJAREA(MATH) OR SUBJAREA(ENGI) OR SUBJAREA(DECI)"

        query = f"({title_query}) AND ({subject_filter})"

        print("Query:", query)


        st123 = ScopusSearch(query, refresh=True, kwds={'sort':'+pubyear'})
        print(st123.get_results_size())
        df123 = pd.DataFrame(pd.DataFrame(st123.results))
        #df.to_csv('test_jeremy2_abs-title-key.csv', sep=';')
        #df.to_csv('title_search_results_2_1308.csv', sep=';')
        df123.to_csv('title_search_%s.csv' % suffix, sep=';')
        print("Title search  OK")



def main_addterms(text1,text2,infile,outfile):
    #os.chdir("D:\\Mes Donnees\\CharlottePlastic\\")

    #v1
    #text1 = "plastic bag, single-use plastic, single-use plastic foodware, food packaging, cosmetics packaging, plastic packaging, sanitary products, microbeads, Expanded PolyStyrene, EPS, foam, straws, q-tip, stirrers, cotton swabs, cotton buds, plastic containers, plastic, plastic bottle, water bottle, plastic product, driftnet, fishing net, fishnet, single-use wipe, single-use water sachet, sachet drinking water, diaper"
    #text2 = "ban, tax, voluntary reduction, voluntary commitment, voluntary pledge, voluntary action, voluntary initiative"
    #V2
    #text1 = "plastic bag, single-use plastic, single-use plastic foodware, food packaging, cosmetics packaging, plastic packaging, sanitary products, microbeads, Expanded PolyStyrene, EPS, foam, straws, q-tip, stirrers, cotton swabs, cotton buds, plastic containers, plastic, plastic bottle, water bottle, plastic product, driftnet, fishing net, fishnet, single-use wipe, single-use water sachet, sachet drinking water, diaper"
    #text2 = "impact, consequence, environment, environmental impact, social impact, economic impact"
    #v3
    #text1 = "plastic bag, single-use plastic, single-use plastic foodware, food packaging, cosmetic packaging, plastic packaging, sanitary product, microbead, Expanded PolyStyrene, EPS, foam, straw, q-tip, stirrer, cotton swab, cotton bud, plastic container, plastic, plastic bottle, water bottle, plastic product, driftnet, single-use wipe, single-use water sachet, sachet drinking water, diaper, mask, ppe, personal protective equipment"
    #text2 = "ban, tax, voluntary reduction, voluntary commitment, voluntary pledge, voluntary action, voluntary initiative"
    #v4
    #text1 = "single-use plastic,plastic,plastic product,packaging waste,plastic bag,food packaging,plastic packaging,Expanded PolyStyrene,EPS,styrofoam,foam,plastic container,food container,plastic wrapper,cup,film,single-use plastic foodware,straw,stirrer,plastic utensil,plastic cutlery,cosmetics packaging,sanitary product,hygiene product,q-tip,microbead,cotton swab,cotton bud,single-use wipe,diaper,bottle,plastic bottle,water bottle,single-use water sachet,sachet drinking water,water sachet,mask,ppe,personal protective equipment,microplastic"
    #text2 = "Ban,tax,voluntary reduction,voluntary commitment,voluntary pledge,voluntary action,voluntary initiative,voluntary agreement,levy,levies ,public-private partnership,enforcement ,fiscal incentive,tax incentive,fiscal disincentive,tax disincentive"


    liste_1 = textToList(text1)
    liste_2 = textToList(text2)



    #infile = "abs_title_key_search_products+policy_V4.csv"
    #infile = "title_search_products+policy_V4.csv"

    df = pd.read_csv(infile,sep=';')
    df["Terms"]=""

    for index,row in df.iterrows():
        terms_liste1=set()
        terms_liste2=set()

        title=""
        abs=""
        keywords=""
        if not pd.isnull(row["title"]):
            title = row["title"]
        if not pd.isnull(row["description"]):
            abs= row["description"]
        if not pd.isnull(row["authkeywords"]):
            keywords = str(row["authkeywords"])

        for term in liste_1:
            term = term.lower().replace('{','').replace('}','')
            #print("LISTE 1 - Current term:",term)
            if term in title.lower() or term in abs.lower() or term in keywords.lower():
                terms_liste1.add(term)

        for term in liste_2:
            term = term.lower().replace('{','').replace('}','')
            #print("LISTE 2 - Current term:",term)
            if term in title.lower() or term in abs.lower() or term in keywords.lower():
                terms_liste2.add(term)

        df.at[index,"Terms"]= ','.join(terms_liste1)+" || "+','.join(terms_liste2)
    df.to_csv(outfile,sep=';')

if __name__=='__main__':

    #os.chdir("D:\\Mes Donnees\\CharlottePlastic\\")

    main_crawling("sn")
    exit()

    df1 = pd.read_csv("abs_title_key_search_products+policy_V6_TERMS.csv",sep=';',encoding='latin-1')
    df2 = pd.read_csv("abs_title_key_search_products+policy_V6_TERMS_AREAS.csv",sep=';',encoding='latin-1')




    #V5
    #text1 = "plastic, single-use plastic, disposable plastic, single-use plastic product, disposable plastic product, plastic product, plastic container, plastic waste, plastic packaging, cosmetics packaging, food packaging, plastic wrapping, plastic wrap, packaging waste, plastic bag, plastic carrier bag, single-use plastic foodware, plastic utensil, single-use plastic stirrer, disposable plastic stirrer, single-use plastic fork, disposable plastic fork, single-use plastic knife, disposable plastic knife, single-use plastic spoon, disposable plastic spoon, plastic food container, plastic beverage container, single-use plastic plate, disposable plastic plate, single-use plastic bowl, disposable plastic bowl, single-use plastic cup, disposable plastic cup, single-use plastic toothpick, disposable plastic toothpick, single-use plastic straw, disposable plastic straw, take-away container, take-away plastic cup, take-away coffee cup, take-away beverage cup, condiment sachet, condiment packet, sanitary product, diaper, nappy, sanitary pad, single-use wipe, hygiene product, tampon, menstrual item, menstrual product, primary microplastic, intentional microplastic, intentionally-added microbead, Expanded PolyStyrene, Expanded polystyrene, EPS, foam, foam packaging, packaging foam, Styrofoam, packing peanuts, q-tip, cotton swab, cotton bud, plastic water container, plastic bottle, water bottle, beverage bottle, water sachet, sachet drinking water, PPE, single-use mask, disposable mask, single-use gloves, disposable gloves, single-use PPE, disposable PPE, single-use goggles, disposable googles, personal protective equipment"
    #text2 = "legislation, law, regulation, ordinance, guideline, ban, prohibition, tax, levy, levies, voluntary reduction, voluntary commitment, voluntary pledge, voluntary action, voluntary initiative, voluntary agreement, public-private partnership, fiscal incentive, tax incentive, fiscal disincentive, tax disincentive"
    #V6
    text1_ext = "plastic, single-use plastic, disposable plastic, single-use plastic product, disposable plastic product, plastic product, plastic container, plastic waste, plastic packaging, cosmetics packaging, food packaging, plastic wrapping, plastic wrap, packaging waste, plastic bag, plastic carrier bag, single-use plastic foodware, plastic utensil, single-use plastic stirrer, disposable plastic stirrer, single-use plastic fork, disposable plastic fork, single-use plastic knife, disposable plastic knife, single-use plastic spoon, disposable plastic spoon, plastic food container, plastic beverage container, single-use plastic plate, disposable plastic plate, single-use plastic bowl, disposable plastic bowl, single-use plastic cup, disposable plastic cup, single-use plastic toothpick, disposable plastic toothpick, single-use plastic straw, disposable plastic straw, take-away container, take-away plastic cup, take-away coffee cup, take-away beverage cup, condiment sachet, condiment packet, sanitary product, diaper, nappy, sanitary pad, single-use wipe, hygiene product, tampon, menstrual item, menstrual product, primary microplastic, intentional microplastic, intentionally-added microbead, Expanded PolyStyrene, Expanded polystyrene, EPS, foam, foam packaging, packaging foam, Styrofoam, packing peanuts, q-tip, cotton swab, cotton bud, plastic water container, plastic bottle, water bottle, beverage bottle, water sachet, sachet drinking water, PPE, single-use mask, disposable mask, single-use gloves, disposable gloves, single-use PPE, disposable PPE, single-use goggles, disposable googles, personal protective equipment, glitter, confetti"
    text1 = "plastic, cosmetics packaging, food packaging,  packaging waste, take-away container, take-away coffee cup, take-away beverage cup, condiment sachet, condiment packet, sanitary product, diaper, nappy, sanitary pad, single-use wipe, hygiene product, tampon, menstrual item, menstrual product, primary microplastic, intentional microplastic, intentionally-added microbead, Expanded PolyStyrene, Expanded polystyrene, EPS, foam, foam packaging, packaging foam, Styrofoam, packing peanuts, q-tip, cotton swab, cotton bud, water bottle, beverage bottle, water sachet, sachet drinking water, PPE, single-use mask, disposable mask, single-use gloves, disposable gloves, single-use PPE, disposable PPE, single-use goggles, disposable googles, personal protective equipment, glitter, confetti"
    text2 = "legislation, law, regulation, ordinance, guideline, ban, prohibition, tax, levy, levies, voluntary reduction, voluntary commitment, voluntary pledge, voluntary action, voluntary initiative, voluntary agreement, public-private partnership, fiscal incentive, tax incentive, fiscal disincentive, tax disincentive"

    suffix = "products+policy_V6_2022"

    out_crawl_title = "title_search_%s.csv" % suffix
    out_crawl_abstitlekey = "abs_title_key_search_%s.csv" % suffix

    out_terms_title = "title_search_%s_TERMS.csv" % suffix
    out_terms_abstitlekey = "abs_title_key_search_%s_TERMS.csv" % suffix

    out_areas_title = "title_search_%s_TERMS_AREAS.csv" % suffix
    out_areas_abstitlekey = "abs_title_key_search_%s_TERMS_AREAS.csv" % suffix


    main_crawling(text1,text2,suffix)

    print("====== Crawling OK =========")

    main_addterms(text1_ext,text2,out_crawl_title,out_terms_title)
    main_addterms(text1_ext,text2,out_crawl_abstitlekey,out_terms_abstitlekey)

    print("====== Add Terms OK =========")

    getSubjectAreas(out_terms_title,out_areas_title)
    getSubjectAreas(out_terms_abstitlekey,out_areas_abstitlekey)

    print("====== Subject Areas OK =========")
