import csv
import requests
import json

outfile = open('results_file.csv', 'w', newline="", encoding='utf-8')
writer = csv.writer(outfile)

writer.writerow(['1. What is your email?', '2. Please enter your BTC address with 0 balance.', '3. Total Sent', '4. Total received', '5. Final balance', '6. Status', '7. Link to your submission?', '8. Landed At', '9. Submitted At'])


def toFloatStr(bitcoin):
    x = float(bitcoin)
    return str(x/100000000)

result = []
with open("wallets.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        result.append(line)

info = []
for line in result:
    result = str(line).strip("[]'")
    info.append([str(result.split(",")[0]),str(result.split(",")[1]),str(result.split(",")[2]),str(result.split(",")[3]),str(result.split(",")[4]),str(result.split(",")[5])])

wallets = ""
for line in info:
    wallets += line[1] + '|'
wallets = (wallets[:-1]) + '&n=0'
url = "https://blockchain.info/multiaddr?active=" + wallets

response = requests.get(url)


if response.status_code == 200:
    print('success')

    requestResult = response.json()

    finalResult = []
    for req in requestResult['addresses']:
        address = req['address']
        for details in info:
            if details[1] == address:
                finalResult.append([details[0], details[1], toFloatStr(req['total_sent']), toFloatStr(req['total_received']), toFloatStr(req['final_balance']), details[2],details[3], details[4], details[5]])

    print(finalResult)
    for line in finalResult:
        writer.writerow([line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]])


outfile.close()

