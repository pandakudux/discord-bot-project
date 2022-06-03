# main file for gusefleyhead discord bot

from debt_calc import calc_indv_debts

# main area for testing
debts = calc_indv_debts()
for person in debts.keys():
    print(f"{person} owes the following people:")
    for debt in debts[person].keys():
        if not debt == 'Total':
            print(f"   {debt}: ${debts[person][debt]}")
    print(f"for a total of: ${debts[person]['Total']}")