import streamlit as st
import os
import numpy as np
import pandas as pd
import random
from deap import base, creator, tools, algorithms
import random
import matplotlib.pyplot as plt

#GA算法代码部分
def Business_Optimizer_GA(Brand_Product_with_limit,Budget,random_state=0):

    def create_individual():
        return [random.randint(0, purchase_limit[i]) for i in range(len(purchase_limit))]

    def evaluate(individual):
        expected_profit = sum(individual[i] * NetProfits[i] * sell_pct[i] for i in range(n_items))
        total_cost = sum(individual[i] * Costs[i] for i in range(n_items))

        # Penalize solutions that exceed the capacity
        if total_cost > Budget:
            return (0,)  # Return 0 fitness if constraint is violated

        return (expected_profit,)

    # set random seed
    if random_state!=0:
        seed_value = random_state
        random.seed(seed_value)
        np.random.seed(seed_value)

    # Define the items' values and weights for the knapsack problem
    NetProfits = Brand_Product_with_limit['NetProfit'].values  # The value of each item
    Costs = Brand_Product_with_limit['TaxIncCost'].values  # The Cost of each item
    sell_pct = Brand_Product_with_limit['sell_pct'].values # The sell_pct of each item


    n_items = len(NetProfits)  # Number of items

    # Define the fitness function, aiming for maximization
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Individual generator: Create a random binary array representing item selection
    purchase_limit = Brand_Product_with_limit['purchase_limit'].values

    # Register tools in the toolbox
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register genetic algorithm operators
    toolbox.register("mate", tools.cxTwoPoint)  # Two-point crossover
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)  # Bit flip mutation with 5% probability
    toolbox.register("select", tools.selTournament, tournsize=3)  # Tournament selection
    toolbox.register("evaluate", evaluate)

    # Main function to run the genetic algorithm
    # Create the population with N individuals
    pop = toolbox.population(n=10000)

    # Set crossover probability, mutation probability, and number of generations
    cxpb, mutpb, ngen = 0.5, 0.2,50
    best_fitness_values = []
    best_value_now = 0

    # GA
    for gen in range(ngen):
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        pop = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, pop))

        # crossover and  mutation
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        # record best
        best_individual = tools.selBest(pop, k=1)[0]
        best_value_1 = best_individual.fitness.values[0]

        if best_value_1>best_value_now:
            best_value_now = best_value_1

        best_fitness_values.append(best_value_now)

        # print(f"Generation {gen + 1}: Best expected_profit = {best_individual.fitness.values[0]}")

    # Output the best individual and its total value
    best_individual = tools.selBest(pop, k=1)[0]
    expected_profit = sum(best_individual[i] * NetProfits[i]* sell_pct[i] for i in range(n_items))
    total_cost = sum(best_individual[i] * Costs[i] for i in range(n_items))

    # print("Best individual is:",best_individual)
    # print("Best expected_profit:", expected_profit)
    # print("Total cost:", total_cost)

    Brand_Product_GA = Brand_Product_with_limit.copy()
    Brand_Product_GA['GA'] = best_individual

    return {
        'data': Brand_Product_GA,  # 这是一个 DataFrame
        'best_profit': expected_profit,
        'total_cost': total_cost
    }


#页面部分
st.title("Intelligent Stocking Assistant")
st.markdown("""
    Welcome to the smart stocking recommendation platform, which makes it easy to find the best brand stocking solution for your budget!
""")

# User role based upload folder
if st.session_state.role == "Admin":
    UPLOAD_FOLDER = "UI/a_data"
else:
    UPLOAD_FOLDER = "UI/c_data"

# File upload section
if os.path.isdir(UPLOAD_FOLDER) and os.listdir(UPLOAD_FOLDER):
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    uploaded_files = ["Select File"] + uploaded_files
    selected_file = st.selectbox("Please select the file to visualize here:", uploaded_files)
    df = None
    if selected_file != "Select File":
        file_path = os.path.join(UPLOAD_FOLDER, selected_file)
        if selected_file.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif selected_file.endswith(".xlsx"):
            df = pd.read_excel(file_path)

        # Required columns for analysis
        # required_columns = ["MemID", "MemGen_x", "MemAge_x", "MemDuration_M_x", "ASPT_x", "MaxSPT_x", "MinSPT_x", 
        #                     "ANT_x", "APDR_x", "APinFavShop_x", "ATRinFavShop_x", "NGinFavShop_x", 
        #                     "NFavinFavShop_x", "MemGen_y", "MemAge_y", "MemDuration_M_y", "ASPT_y", 
        #                     "MaxSPT_y", "MinSPT_y", "ANT_y", "APDR_y", "APinFavShop_y", "ATRinFavShop_y", 
        #                     "NGinFavShop_y", "NFavinFavShop_y", "ProdName"]
        required_columns = ["QtySold"]
        

        # Analysis button with style
        # if st.button("🔍 Analyze", key="analyze_button"):
        # st.header("🌟 SVIP Spotlight and Product Recommendations")
        if df is not None:
            if all(col in df.columns for col in required_columns):
                # st.success("The file is loaded successfully!")
                default_budget = 100000
                budget = st.number_input("Please enter a budget (default is 100000):", value = 100000)
                if st.button("Submit"):
                    if budget is None or budget == 0 or budget <= 0:
                        st.warning("The budget must be greater than 0. The default value of 100000 has been used.")
                        budget = default_budget
                    brand_value = df['CntName'].iloc[0]
                    st.write(f"For Brand: ***{brand_value}***")
                    st.write(f"If your budget is: **{budget}**")
                    st.toast("Please wait a moment while the results are being generated!")
                    # 调用函数并接收返回值
                    result = Business_Optimizer_GA(df, budget, random_state=66)
                    # 访问数据
                    data = result['data']           # 这是一个 DataFrame
                    best_profit = result['best_profit']
                    total_cost = result['total_cost']
                    selected_columns = data[['ProdID', 'ProdName', 'GA']].rename(
                        columns={
                            'ProdID': 'Product ID',
                            'ProdName': 'Product Name',
                            'GA': 'purchase quantity'
                        }
                    )
                    st.write("The most recommended brand stocking programs are listed below:")
                    st.dataframe(selected_columns)
                    st.write(f"The optimal profit is expected to be: **{best_profit}**")
                    st.write(f"The total cost will be: **{total_cost}**")
            else:
                st.warning(f"The selected file does not contain the required columns: {', '.join(required_columns)}. Please upload a file with the correct format.", icon="⚠️")
        else:
            st.warning("Please select a valid file before clicking 'Analyze'.", icon="⚠️")
else:
    st.warning("Please upload one or more files in the upload files section to get started!", icon="⚠️")

