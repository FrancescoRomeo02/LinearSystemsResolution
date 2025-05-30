import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path


def plot_performance(results, matrix_name, output_dir="output/plots"):
    """
    Genera e salva grafici delle prestazioni degli algoritmi iterativi:
    - Errore relativo e tempo di esecuzione in funzione della tolleranza.
    - Confronto del consumo medio di memoria tra i metodi.

    Parameters
    ----------
    results : list
        Lista di oggetti `SolverResult` o simili, contenenti attributi:
        - method_name: nome dell'algoritmo.
        - tol: tolleranza usata.
        - max_iteration: iterazioni massime
        - method_result: classe `IterativeResult` che contiene:
            - solution: array della solution
            - iterations: numero di ietarzioni eseguite ` ` ` `
        - rel_error: errore relativo finale.
        - time_seconds: tempo impiegato.
        - memory_kb: memoria utilizzata (in KB).
    matrix_name : str
        Nome della matrice (utilizzato nei titoli e nomi dei file).
    output_dir : str, optional
        Cartella di output dove salvare i grafici. Default = "plots".

    Returns
    -------
    None

    Notes
    -----
    I grafici vengono salvati in PNG a 300 DPI.
    I valori dell’asse x (tolleranza) sono in scala logaritmica.
    La memoria è aggregata come media per metodo.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    methods = sorted(set(r.method_name for r in results))
    metrics = ["rel_error", "time_seconds", "iterations"]

    # Plot: Errore, Tempo e Iterazioni vs Tolleranza
    for metric in metrics:
        plt.figure(figsize=(10, 6))

        for method in methods:
            x_vals = [r.tol for r in results if r.method_name == method]

            if metric == "iterations":
                y_vals = [
                    r.method_result.iterations for r in results if
                    r.method_name == method]
            else:
                y_vals = [getattr(r, metric)
                          for r in results if r.method_name == method]

            sns.lineplot(x=x_vals, y=y_vals, marker='o', label=method)

        plt.xscale("log")
        if metric == "rel_error":
            plt.yscale("log")

        plt.xlabel("Tolleranza", fontsize=12)
        plt.ylabel(metric.replace("_", " ").title(), fontsize=12)
        plt.title(f"{metric.replace('_', ' ').title()} vs Tolleranza\n{
            matrix_name}", fontsize=14, weight='bold')
        plt.legend(title="Metodo")
        plt.grid(True)
        plt.tight_layout()

        filename = f"{matrix_name}_{metric}".replace(' ', '_')
        plt.savefig(Path(output_dir) / f"{filename}.png", dpi=300)
        plt.close()

    # Plot: Memoria media per metodo
    memory_data = {
        method: sum(r.memory_kb for r in results if r.method_name == method) /
        len([r for r in results if r.method_name == method])
        for method in methods
    }

    memory_df = pd.DataFrame({
        "Metodo": list(memory_data.keys()),
        "Memoria_KB": list(memory_data.values())
    })

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=memory_df,
        x="Metodo",
        y="Memoria_KB",
        hue="Metodo",
        palette="pastel",
        legend=False
    )

    plt.ylabel("Memoria media (KB)", fontsize=12)
    plt.title(f"Confronto Memoria tra Metodi\n{
              matrix_name}", fontsize=14, weight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()

    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    filename = f"{matrix_name}_memory_comparison".replace(' ', '_')
    plt.savefig(Path(output_dir) / f"{filename}.png", dpi=300)
    plt.close()

    # Plot: Iterazioni per metodo e tolleranza
    iterations_data = []
    
    for method in methods:
        for tol in sorted(set(r.tol for r in results)):
            method_tol_results = [r for r in results if r.method_name == method and r.tol == tol]
            if method_tol_results:
                for r in method_tol_results:
                    iterations_data.append({
                        'Metodo': method,
                        'Tolleranza': tol,
                        'Iterazioni': r.method_result.iterations
                    })
    
    iterations_df = pd.DataFrame(iterations_data)
    
    plt.figure(figsize=(12, 7))
    palette = sns.color_palette("husl", len(methods))
    ax = sns.barplot(
        data=iterations_df,
        x='Tolleranza',
        y='Iterazioni',
        hue='Metodo',
        palette=palette
    )
    
    tol_values = sorted(iterations_df['Tolleranza'].unique())
    plt.xticks(range(len(tol_values)), [f"{x:.0e}" for x in tol_values], rotation=45)
    
    plt.ylabel("Numero di Iterazioni", fontsize=12)
    plt.xlabel("Tolleranza", fontsize=12)
    plt.title(f"Confronto Numero di Iterazioni per Tolleranza\n{matrix_name}", 
              fontsize=14, weight='bold')
    plt.legend(title="Metodo", loc='upper right')
    plt.grid(axis='y')
    plt.tight_layout()
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', fontsize=8)
    
    filename = f"{matrix_name}_iterations_comparison".replace(' ', '_')
    plt.savefig(Path(output_dir) / f"{filename}.png", dpi=300)
    plt.close()