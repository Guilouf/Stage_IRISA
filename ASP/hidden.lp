% Hidden compounds

hidden("HYDROGEN-MOLECULE").
hidden("OXYGEN-MOLECULE").
hidden("PROTON").
hidden("WATER").
hidden("ADP").
hidden("ATP").
hidden("ACETYL-COA").
hidden("NITRATE").
hidden("OH").
hidden("Donor-H2").
hidden("NAD-P-OR-NOP").
hidden("NADH-P-OR-NOP").
hidden("GLT").
hidden("CO-A").
hidden("CARBON-DIOXYDE").

hidden(X):- is_a(X,"NAD-P-OR-NOP").
hidden(X):- is_a(X,"NADH-P-OR-NOP").
