import numpy as np
import pandas as pd

# Gráficos
# ------------------------------------------------------------------------------
import matplotlib.pyplot as plt

# Preprocesado y modelado
# ------------------------------------------------------------------------------
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
from sklearn.tree import export_text
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

# Configuración warnings
# ------------------------------------------------------------------------------
import warnings
warnings.filterwarnings('once')


def obtainData():

    # Se unen todos los datos (predictores y variable respuesta en un único dataframe)
    boston = load_boston(return_X_y=False)
    datos = np.column_stack((boston.data, boston.target))
    datos = pd.DataFrame(datos, columns=np.append(boston.feature_names, "MEDV"))
    datos.head(10)

    # División de los datos en train y test
    # ------------------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        datos.drop(columns="MEDV"),
        datos['MEDV'],
        random_state=123
    )
    # Creación del modelo
    # ------------------------------------------------------------------------------
    modelo = DecisionTreeRegressor(
        max_depth=3,
        random_state=123
    )

    # Entrenamiento del modelo
    # ------------------------------------------------------------------------------
    modelo.fit(X_train, y_train)

    # Estructura del árbol creado
    # ------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5))

    plot = plot_tree(
        decision_tree=modelo,
        feature_names=datos.drop(columns="MEDV").columns,
        class_names='MEDV',
        filled=True,
        impurity=False,
        fontsize=10,
        precision=2,
        ax=ax
    )

    texto_modelo = export_text(
        decision_tree=modelo,
        feature_names=list(datos.drop(columns="MEDV").columns)
    )

    importancia_predictores = pd.DataFrame(
        {'predictor': datos.drop(columns="MEDV").columns,
        'importancia': modelo.feature_importances_}
    )

    importancia_predictores.sort_values('importancia', ascending=False)

    # Pruning (const complexity pruning) por validación cruzada
    # ------------------------------------------------------------------------------
    # Valores de ccp_alpha evaluados
    param_grid = {'ccp_alpha': np.linspace(0, 80, 20)}

    # Búsqueda por validación cruzada
    grid = GridSearchCV(
        # El árbol se crece al máximo posible para luego aplicar el pruning
        estimator=DecisionTreeRegressor(
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=123
        ),
        param_grid=param_grid,
        cv=10,
        refit=True,
        return_train_score=True
    )

    grid.fit(X_train, y_train)

    fig, ax = plt.subplots(figsize=(6, 3.84))
    scores = pd.DataFrame(grid.cv_results_)
    scores.plot(x='param_ccp_alpha', y='mean_train_score',
                yerr='std_train_score', ax=ax)
    scores.plot(x='param_ccp_alpha', y='mean_test_score',
                yerr='std_test_score', ax=ax)
    ax.set_title("Error de validacion cruzada vs hiperparámetro ccp_alpha")

    grid.best_params_

    # Estructura del árbol final
    # ------------------------------------------------------------------------------
    modelo_final = grid.best_estimator_

    fig, ax = plt.subplots(figsize=(7, 5))
    plot = plot_tree(
        decision_tree=modelo_final,
        feature_names=datos.drop(columns="MEDV").columns,
        class_names='MEDV',
        filled=True,
        impurity=False,
        ax=ax
    )

    # Error de test del modelo inicial
    # -------------------------------------------------------------------------------
    predicciones = modelo.predict(X=X_test)

    rmse = mean_squared_error(
        y_true=y_test,
        y_pred=predicciones,
        squared=False
    )
    
    rmse_inicial = rmse

    # Error de test del modelo final (tras aplicar pruning)
    # -------------------------------------------------------------------------------
    predicciones = modelo_final.predict(X=X_test)

    rmse = mean_squared_error(
        y_true=y_test,
        y_pred=predicciones,
        squared=False
    )

    rmse_final = rmse

    return {
        'textoModelo': str(texto_modelo),
        'rmseInicial': str(rmse_inicial),
        'rmseFinal': str(rmse_final)
    }