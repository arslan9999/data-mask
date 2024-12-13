import sys
import faker
import json
from datetime import datetime
from DatabaseConnection import DatabaseConnection

sourceType = sys.argv[1]
sourceName = sys.argv[2]
destType = sys.argv[3]
destName = sys.argv[4]
maskingLevel = sys.argv[5]


print("Connecting to Database...")
try:
    databaseConnection = DatabaseConnection()
    sourceConnection = databaseConnection.getConnection(sourceType, sourceName)
    sourceCursor = sourceConnection.cursor()
    destConnection = databaseConnection.getConnection(destType, destName)
    destCursor = destConnection.cursor()
except:
    print("Failed to connect to database.")
    exit()

print("Database connection established... \n ------------")
fake = faker.Faker()

maskingTemplate = json.load(open("template.json"))["masking_levels"][maskingLevel.lower()]

def applyMasing(mask, value):
    if mask["masking_type"] == "none":
        return value
    elif mask["masking_type"] == "partial":
        visible_start = int(mask["visible_start"])
        visible_end = int(mask["visible_end"])
        masked = '*' * (len(value) - visible_start - visible_end)
        return value[:visible_start] + masked + value[-visible_end:]
    elif mask["masking_type"] == "fixed":
        return mask["masking_value"]
    elif mask["masking_type"] == "scramble":
        if mask["field_name"] == "address":
            return fake.address()
        elif mask["field_name"] == "city":
            return fake.city()
        elif mask["field_name"] == "maiden_name":
            return fake.last_name()
        elif mask["field_name"] == "lname":
            return fake.last_name()
        elif mask["field_name"] == "fname":
            return fake.first_name()
        elif mask["field_name"] == "cc_expiredate":
            cc_expire = fake.credit_card_expire()  # Format is MM/YY
            cc_expire_month, cc_expire_year = map(int, cc_expire.split('/'))
            return datetime(year=2000 + cc_expire_year, month=cc_expire_month, day=1).date()
        elif mask["field_name"] == "birthdate":
            return fake.date_of_birth()
    return value

tempAppliedMasking = {}

def implementMasking(fieldName, value):
    loopCount = 1
    totalFields = len(maskingTemplate)
    for maskField in maskingTemplate:
        if maskField["field_name"].lower() == fieldName.lower():
             return applyMasing(maskField, value)
        elif loopCount == totalFields:
            if(fieldName.lower() in tempAppliedMasking):
                if tempAppliedMasking[fieldName] == "1":
                    return value
                elif tempAppliedMasking[fieldName] == "2":
                    return "*"
                else:
                    return value
            else:
                print("Masking type not found for " + fieldName)
                print("Select a masking type: \n")
                print("1 for None\n2 for Fixed\n")
                userSelection = input()
                tempAppliedMasking[fieldName.lower()] = userSelection
                if tempAppliedMasking[fieldName] == "1":
                    return value
                elif tempAppliedMasking[fieldName] == "2":
                    return "*"
                else:
                    return value

        loopCount += 1

# Assign data query
query1 = "SELECT * FROM users"

# Execute query
sourceCursor.execute(query1)

# Fetch all records
table = sourceCursor.fetchall()
coloums = sourceCursor.description


count = 0
conditions = {}
# Process each record and insert into the destination table
for attr in table:
    colNum = 0
    finalVal = {}
    for coloum in coloums:
        finalVal[coloum[0]] = implementMasking(coloum[0], attr[colNum])
        colNum += 1

    #print(finalVal)

    # Define parameterized query
    insertionQuery = '''
    INSERT INTO users (
        id, gender, birthdate, maiden_name, lname, fname, address, city, state, zip, phone, email, cc_type, cc_number, cc_cvc, cc_expiredate
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''

    #print(finalVal)
    # Execute the query with parameterized values
    destCursor.execute(insertionQuery, list(finalVal.values()))
    count += 1

# Commit changes to the destination database
destConnection.commit()

#print(conditions)
print("Masking completed... \n Total masked rows: " + str(count))
allTempVals = tempAppliedMasking.values()
print("Total Fields masked: " + str(len(maskingTemplate) + len(tempAppliedMasking)))

# Close cursor and connection objects
sourceCursor.close()
destCursor.close()
sourceConnection.close()
destConnection.close()