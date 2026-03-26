import os
import pandas as pd
import datetime
from pathlib import Path
from dotenv import load_dotenv
import funcs
import constants as cnst

if __name__ == "__main__":
    funcs.resetDir()
    os.chdir("Keys")
    os.chdir("Secrets")
    load_dotenv("Files.env")
    load_dotenv("secrets.env")
    funcs.resetDir()
    
    os.chdir("Keys")
    os.chdir("Hidden Files")
    pendingTasklist = pd.read_csv("Pending.csv")
    completedTasklist = pd.read_csv("Completed.csv")
    print(pendingTasklist)
    print(completedTasklist)
    funcs.resetDir()

    toDF = {"Tag":[],"Task":[],"Completed?":[],"Due Date":[],"Due Time":[]}

    taskFilePath = Path(os.getenv("OBSIDIAN_TASK_FILE"))
    with open(taskFilePath, 'r') as f:
        for i in f.readlines():
            if "#" in i:
                if i == "# Completed":
                    break
            else:
                toDF["Tag"].append(i.split("->")[0].split("]")[1].strip())
                toDF["Task"].append(i.split("->")[1].split("|")[0].strip())
                toDF["Due Date"].append(i.split("Due by")[1].split("at")[0].strip())
                toDF["Due Time"].append(i.split("Due by")[1].split("at")[1].strip())

                toDF["Completed?"].append((lambda x: True if x == "x" else False)(i[3]))

    
    pendingDF = pd.DataFrame(toDF)

    toDF = {"Tag":[],"Task":[],"Completed?":[],"Due Date":[],"Due Time":[]}

    with open(taskFilePath, 'r') as f:
        completedReached = False
        for i in f.readlines():
            if "#" in i:
                if i.strip() == "# Completed":
                    completedReached = True
            else:
                if completedReached:
                    toDF["Tag"].append(i.split("->")[0].split("]")[1].strip())
                    toDF["Task"].append(i.split("->")[1].split("|")[0].strip())
                    toDF["Due Date"].append(i.split("Due by")[1].split("at")[0].strip())
                    toDF["Due Time"].append(i.split("Due by")[1].split("at")[1].strip())

                    toDF["Completed?"].append((lambda x: True if x == "x" else False)(i[3]))


    completedDF = pd.DataFrame(toDF)
    completedDF = pd.concat(objs = [completedDF,pendingDF[pendingDF["Completed?"] == True]],ignore_index=True).drop_duplicates()
    pendingDF = pendingDF[pendingDF["Completed?"] == False].drop_duplicates()
    completedDF["Due Date"] = pd.to_datetime(completedDF["Due Date"],format="%m/%d/%Y",errors="coerce")
    pendingDF["Due Date"] = pd.to_datetime(pendingDF["Due Date"],format="%m/%d/%Y",errors="coerce")
    completedDF["Due Time"] = pd.to_datetime(completedDF["Due Time"],format="%H%M",errors="coerce")
    pendingDF["Due Time"] = pd.to_datetime(pendingDF["Due Time"],format="%H%M",errors="coerce")
    
    completedDF["Key"] = completedDF.apply(lambda x: funcs.generateRowIDHash(x["Tag"] + x["Task"]), axis=1)
    pendingDF["Key"] = pendingDF.apply(lambda x: funcs.generateRowIDHash(x["Tag"] + x["Task"]), axis=1)

    completedDF.sort_values(by=["Due Date","Due Time"], ascending=[False,False],inplace=True)
    pendingDF.sort_values(by=["Due Date","Due Time"], ascending=[True,True],inplace=True)

    completedDF.reset_index(inplace=True,drop=True)
    pendingDF.reset_index(inplace=True,drop=True)
    
    nuFileContent = cnst.header + "# Pending\n"
    for i in pendingDF.iterrows():
        nuFileContent += f"- [{"x" if i[1]["Completed?"] else " "}] {i[1]["Tag"]} -> {i[1]["Task"]} | Due by {i[1]["Due Date"].strftime('%m/%d/%Y') if not type(i[1]["Due Date"]) == type(pd.NaT) else "None"} at {i[1]["Due Time"].strftime('%H%M') if not type(i[1]["Due Time"]) == type(pd.NaT) else "None"}\n"
    nuFileContent += "# Completed\n"
    for i in completedDF.iterrows():
        nuFileContent += f"- [{"x" if i[1]["Completed?"] else " "}] {i[1]["Tag"]} -> {i[1]["Task"]} | Due by {i[1]["Due Date"].strftime('%m/%d/%Y') if not type(i[1]["Due Date"]) == type(pd.NaT) else "None"} at {i[1]["Due Time"].strftime('%H%M') if not type(i[1]["Due Time"]) == type(pd.NaT) else "None"}\n"
    with open(taskFilePath, 'w') as f:
        f.write(nuFileContent)
    
    funcs.resetDir()
    
    os.chdir("Keys")
    os.chdir("Hidden Files")
    completedDF.to_csv("Completed.csv",index=False)
    pendingDF.to_csv("Pending.csv",index=False)
    funcs.resetDir()