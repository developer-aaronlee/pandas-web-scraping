import pandas as pd
import re

payscale_url = "http://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
frames = []

for x in range(1, 35):
    if x == 1:
        url = payscale_url
    else:
        url = f"{payscale_url}/page/{x}"

    data = pd.read_html(url)[0].copy()
    data.columns = ["Rank", "Major", "DegreeType", "EarlyCareerPay", "MidCareerPay", "HighMeaning"]
    frames.append(data)

results = pd.concat(frames, axis=0, ignore_index=True)
# print(results)

target_df = results[["Major", "EarlyCareerPay", "MidCareerPay"]]

# target_df["EarlyCareerPay"] = target_df["EarlyCareerPay"].str.replace(r"[a-zA-Z$:,]", "")

clean_dic = {"Major": target_df["Major"].str.strip("Major:"),
             "EarlyCareerPay": target_df["EarlyCareerPay"].str.replace(r"[a-zA-Z$:,-]", "", regex=True),
             "MidCareerPay": target_df["MidCareerPay"].str.replace(r"[a-zA-Z$:,-]", "", regex=True)}

clean_df = pd.DataFrame(data=clean_dic)
clean_df[["EarlyCareerPay", "MidCareerPay"]] = clean_df[["EarlyCareerPay", "MidCareerPay"]].apply(pd.to_numeric)
# print(clean_df)

# highest_early_pay = clean_df.sort_values("EarlyCareerPay", ascending=False)
highest_early_pay = clean_df.nlargest(5, "EarlyCareerPay")
print(highest_early_pay[["Major", "EarlyCareerPay"]].head())

# highest_mid_pay = clean_df.sort_values("MidCareerPay", ascending=False)
highest_mid_pay = clean_df.nlargest(5, "MidCareerPay")
print(highest_mid_pay[["Major", "MidCareerPay"]].head())



