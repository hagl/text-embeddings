import csv


##### MAIN SCRIPT #####

if __name__ == '__main__':
    INDEX_NAME = "posts"
    INDEX_FILE = "data/keywords/index.json"

    DATA_FILE = "data/images/metadata.csv"
    BATCH_SIZE = 1000

    SEARCH_SIZE = 5

    print("Reading cvs...")
    with open(DATA_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            print(row[0], ":", len(row), ":", row[1])
            doc = {
                "imageId": row[0],
                "title": row[1],
            }
            print(doc)
    print("Done.")
