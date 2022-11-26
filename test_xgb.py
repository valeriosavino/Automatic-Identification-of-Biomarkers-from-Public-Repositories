import datetime
import numpy as np 
import pandas as pd 
import warnings
import pydotplus
import os
import psutil
import math
 
# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(process.cpu_times())
    return mem_info.rss

def createDecisionTree(t_ct, sample, crit, imagepath):
    mem_before = process_memory()
    warnings.filterwarnings('ignore')

    df_census = pd.read_csv('csv_input.csv')

    #tutte le colonne del file (tessuto, cellula, gene1,...,gene15k)
    if(t_ct):
        X = df_census.iloc[:,:-1]
    else:
        X = df_census.iloc[:,2:-1]
    #colonna del cancer da prevere
    y = df_census.iloc[:,-1]

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)

    from sklearn.tree import DecisionTreeClassifier

    #creazione del decision tree 
    clf = DecisionTreeClassifier(random_state=2, min_samples_leaf=sample, criterion=crit)
    clf.fit(X_train, y_train)
    #estrazione foglie
    leafs = clf.apply(X_train)    

    from sklearn import tree
    import graphviz 

    new_class_name = ["Sano", "Breast cancer", "Carcinoid", 
                    "Cervical Cancer", "Colorectal Cancer", "Endometrial Cancer",
                    "Glioma", "Head and Neck Cancer", "Liver Cancer", 
                    "Lung Cancer", "Lymphoma", "Melanoma", 
                    "Ovarian Cancer", "Pancreatic Cancer", "Prostate Cancer",
                    "Renal Cancer", "Skin Cancer", "Stomach Cancer", 
                    "Testis Cancer", "Thyroid Cancer", "Urothelial Cancer"]

    dot_data = tree.export_graphviz(clf, out_file=None, 
                          feature_names=list(X.columns), 
                          class_names=new_class_name,    
                          filled=True, 
                          rounded=True,  
                          special_characters=True, 
                          max_depth=None,
                          node_ids=True)  
    graph = pydotplus.graph_from_dot_data(dot_data)
    nodes = graph.get_node_list()

    k = -1
    n = sum(clf.tree_.value[0][0])
    hsum = 0
    l = []
    colors =  ('darkgrey','tomato','orange',
                'palegreen','aquamarine','pink',
                'lightblue','lightyellow','forestgreen',
                'indianred','deepskyblue','cadetblue',
                'violet','cyan','royalblue',
                'goldenrod','lightseagreen','chocolate',
                'plum','mediumpurple','lightcoral','thistle','lemonchiffon')

    for node in nodes:
        if node.get_name() not in ('node', 'edge'):
            if(node.get_name() != '"\\n"'):
                values = clf.tree_.value[int(node.get_name())][0]
                #colora solamente le foglie in cui è presente un solo elemento nei values con i samples
                if(max(values) == sum(values)): 
                    node.set_fillcolor(colors[np.argmax(values)])
                elif(int(node.get_name()) in leafs):
                    node.set_fillcolor(colors[-2])
                else:
                    node.set_fillcolor(colors[-1])
                if(max(values) == sum(values) or int(node.get_name()) in leafs):
                    k += 1
                    l.append(sum(values))
                    p = sum(values) / n
                    h = clf.tree_.impurity[int(node.get_name())]
                    hsum += p*h
    
    s = sum(l) / k
    den_var = 0
    for i in range(len(l)):
        den_var += math.pow(l[i]-s, 2)
    var = den_var / k
    std_var = math.sqrt(var)
    print("H = ", hsum)
    print("S = ", s)
    print("std_var = ", std_var)
    
    if(not os.path.exists("graphs")):
        os.mkdir("graphs")
    graph.write_png(imagepath)

    mem_after = process_memory()
    ram_usage = mem_after - mem_before
    print(ram_usage)


createDecisionTree(True,1,"gini","graphs/graph_completo_t_ct.png")
createDecisionTree(True,20,"gini","graphs/graph_20_t_ct.png")
createDecisionTree(True,30,"gini","graphs/graph_30_t_ct.png")
createDecisionTree(True,40,"gini","graphs/graph_40_t_ct.png")
createDecisionTree(True,50,"gini","graphs/graph_50_t_ct.png")

createDecisionTree(False,1,"gini","graphs/graph_completo_no_t_ct.png")
createDecisionTree(False,20,"gini","graphs/graph_20_no_t_ct.png")
createDecisionTree(False,30,"gini","graphs/graph_30_no_t_ct.png")
createDecisionTree(False,40,"gini","graphs/graph_40_no_t_ct.png")
createDecisionTree(False,50,"gini","graphs/graph_50_no_t_ct.png")

createDecisionTree(True,1,"entropy","graphs/graph_entropy_completo_t_ct.png")
createDecisionTree(True,20,"entropy","graphs/graph_entropy_20_t_ct.png")
createDecisionTree(True,30,"entropy","graphs/graph_entropy_30_t_ct.png")
createDecisionTree(True,40,"entropy","graphs/graph_entropy_40_t_ct.png")
createDecisionTree(True,50,"entropy","graphs/graph_entropy_50_t_ct.png")

createDecisionTree(False,1,"entropy","graphs/graph_entropy_completo_no_t_ct.png")
createDecisionTree(False,20,"entropy","graphs/graph_entropy_20_no_t_ct.png")
createDecisionTree(False,30,"entropy","graphs/graph_entropy_30_no_t_ct.png")
createDecisionTree(False,40,"entropy","graphs/graph_entropy_40_no_t_ct.png")
createDecisionTree(False,50,"entropy","graphs/graph_entropy_50_no_t_ct.png")