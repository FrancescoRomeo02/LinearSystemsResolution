import numpy as np


def verify_accuracy(x_computed, x_true):
    """
    Calcola l'errore relativo (norma 2) tra la soluzione
    calcolata e quella attesa.

    Parameters
    ----------
    x_computed : ndarray
        Vettore della soluzione calcolata da un algoritmo numerico.
    x_true : ndarray
        Vettore della soluzione esatta o di riferimento.

    Returns
    -------
    float
        Errore relativo in norma 2 tra `x_computed` e `x_true`.
        Se `x_true` è quasi nullo, restituisce l'errore assoluto.

    Raises
    ------
    ValueError
        Se `x_computed` e `x_true` hanno dimensioni incompatibili.

    Notes
    -----
    L'errore relativo è definito come:
        ||x_computed - x_true||_2 / ||x_true||_2
    Se la norma di `x_true` è trascurabile (< 1e-14),
    il metodo ritorna l'errore assoluto.
    """
    if x_computed.shape != x_true.shape:
        raise ValueError(
            f"Mismatch of sizes, x_computed: {x_computed.shape}, x_true: {x_true.shape}"
        )

    norm_true = np.linalg.norm(x_true, ord=2)

    if norm_true < 1e-14:
        return np.linalg.norm(x_computed - x_true, ord=2)

    rel_error = np.linalg.norm(x_computed - x_true, ord=2) / norm_true
    return f"{rel_error:.4e}"