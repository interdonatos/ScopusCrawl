import pandas as pd

df = pd.read_csv("title_search_sn_clean.csv", sep=";")

#crisis_keywords = ["crisis", "disaster", "emergency", "humanitarian", "catastrophe", "hazard", "pandemic", "outbreak","earthquake", "flood","hurricane","wildfire"]

terms_path = './data/crisis_keys.txt'

# Read terms from a text file into a list
with open(terms_path, "r") as f:
    crisis_keywords = [line.strip() for line in f if line.strip()]

def has_crisis_keyword(title):
    if not isinstance(title, str):
        return False
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in crisis_keywords)

def first_cleaning():
    suffix = 'sn'
    # Assuming your results are in a dataframe already, if not:
    # df = pd.DataFrame([r._asdict() for r in s.results])

    terms_path = './data/sn_list.txt'

    # Read terms from a text file into a list
    with open(terms_path, "r") as f:
        terms = [line.strip() for line in f if line.strip()]

    # 1. Remove articles where the ONLY keyword match in title is "thread" or "threads"
    other_keywords = [kw for kw in terms if kw.lower() not in ("thread", "threads")]

    def has_other_keyword(title):
        if not isinstance(title, str):
            return False
        title_lower = title.lower()
        return any(kw.lower() in title_lower for kw in other_keywords)

    df = df[df["title"].apply(has_other_keyword)]

    # 2. Remove articles before 2004
    df["coverDate"] = pd.to_datetime(df["coverDate"])
    df = df[df["coverDate"].dt.year >= 2004]

    print(f"Remaining results: {len(df)}")

    df.to_csv('title_search_%s_clean.csv' % suffix, sep=';')

def crisis_cleaning():

    df_crisis = df[df["title"].apply(has_crisis_keyword)]

    print(f"Crisis-related results: {len(df_crisis)}")
    print(df_crisis[["title", "coverDate"]].head(10))

    df_crisis.to_csv("crisis_results_new.csv", index=False, sep=';')

if __name__=="__main__":
    crisis_cleaning()