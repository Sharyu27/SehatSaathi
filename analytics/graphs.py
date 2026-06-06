import pandas as pd
import matplotlib.pyplot as plt
from database.db import get_logs

def generate_graph():
    data = get_logs()

    if not data:
        print("No data available")
        return

    df = pd.DataFrame(data)

    counts = df['status'].value_counts()
    counts.plot(kind='bar')

    plt.title("Medicine Adherence")
    plt.xlabel("Status")
    plt.ylabel("Count")

    plt.show()