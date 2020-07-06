from Utility import *

#b1
orderedListOfHiddenVariables = ["Trav", "FP", "Fraud", "IP", "OC", "CRP"]
factorListAll = [Factor([Variable("Trav", [True, False])], [0.05, 0.95]), 
                Factor([Variable("Trav", [True, False]), Variable("Fraud", [True, False]), Variable("FP", [True, False])], [0.9, 0.1, 0.9, 0.1, 0.1, 0.9, 0.01, 0.99]), 
                Factor([Variable("Trav", [True, False]), Variable("Fraud", [True, False])], [0.01, 0.99, 0.004, 0.996]), 
                Factor([Variable("OC", [True, False]), Variable("Fraud", [True, False]), Variable("IP", [True, False])], [0.02, 0.98, 0.01, 0.99, 0.011, 0.989, 0.001, 0.999]), 
                Factor([Variable("OC", [True, False])], [0.6, 0.4]),
                Factor([Variable("OC", [True, False]), Variable("CRP", [True, False])], [0.1, 0.9, 0.001, 0.999])
                ]
factorListb1 = [Factor([Variable("Trav", [True, False])], [0.05, 0.95]), 
                Factor([Variable("Trav", [True, False]), Variable("Fraud", [True, False])], (0.01, 0.99, 0.004, 0.996))
                ]
resultVector = inference(factorListb1,[Variable("Fraud", [True, False])], [Variable("Trav", [True, False])], {})
print(resultVector)