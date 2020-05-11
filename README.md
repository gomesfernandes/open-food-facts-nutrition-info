
## Apache Beam pipeline in Java + Apache Airflow DAG

This project uses a dataset made available by [Open Food Facts](https://fr.openfoodfacts.org/data) 
under the [Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1.0/).

The original dataset can be found on the [Open Food Facts website](https://fr.openfoodfacts.org/data>) 
(French, under "Export CSV"), as well as on 
[data.gouv.fr](https://www.data.gouv.fr/fr/datasets/open-food-facts-produits-alimentaires-ingredients-nutrition-labels/).


### Code overview

`src` and contains de Java source code for the Apache Beam pipeline

`dags` contains the Python source code to build the Apache Airflow DAG that fetches the Open Food Facts dataset, 
runs the Apache Beam pipeline (todo) and cleans up the results into a single file.