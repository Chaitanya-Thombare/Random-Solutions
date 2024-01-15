import pandas as pd

path = r'./splitter.xlsx'
df = pd.read_excel(path, sheet_name='Sheet2')

peeps_col = df.columns[-1]
peeps = df.columns[-1].split(',')

main_chart = dict.fromkeys(peeps, 0)
spent_chart = dict.fromkeys(peeps, 0)
consumed_chart = dict.fromkeys(peeps, 0)

for expense in df.to_dict(orient='records'):
    main_chart[expense['Sponsor']] -= expense['Cost']
    spent_chart[expense['Sponsor']] += expense['Cost']
    involved = expense[peeps_col].replace(' ', '').split(',')
    per_head_cost = round(expense['Cost'] / len(involved), 2)
    for peep in involved:
        main_chart[peep] += per_head_cost
        consumed_chart[peep] += per_head_cost

creds, debts, cleared = {}, {}, {}
for k, v in main_chart.items():
    if v < 0: creds[k] = -v
    if v > 0: debts[k] = v
    if v == 0: cleared[k] = v

creds = dict(sorted(creds.items(), key=lambda x: x[1], reverse=True))
debts = dict(sorted(debts.items(), key=lambda x: x[1], reverse=True))

creds_keys = list(creds.keys())
debts_keys = list(debts.keys())

transactions = []

for payee in creds_keys:
    for payer in debts_keys:
        if debts[payer] < creds[payee]:
            transactions.append((payer, payee, debts[payer]))
            creds[payee] -= debts[payer]
            debts[payer] = 0
            continue

        elif debts[payer] >= creds[payee]:
            transactions.append((payer, payee, creds[payee]))
            debts[payer] -= creds[payee]
            creds[payee] = 0
            break

transactions_df = pd.DataFrame(transactions, columns=['Payer', 'Payee', 'Amount'])
spent_df = pd.DataFrame(spent_chart.items(), columns=['Name', 'Spent'])
consume_df = pd.DataFrame(consumed_chart.items(), columns=['Name', 'Consumed'])

print(transactions_df)
print(spent_df)
print(consume_df)