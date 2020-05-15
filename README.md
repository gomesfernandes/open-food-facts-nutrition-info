
## Apache Beam pipeline in Java + Apache Airflow DAG

This project uses a dataset made available by [Open Food Facts](https://fr.openfoodfacts.org/data) 
under the [Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1.0/).

The original dataset can be found on the [Open Food Facts website](https://fr.openfoodfacts.org/data>) 
(French, under "Export CSV"), as well as on 
[data.gouv.fr](https://www.data.gouv.fr/fr/datasets/open-food-facts-produits-alimentaires-ingredients-nutrition-labels/).


### Overview

**Local run**: To run the pipeline locally on the manually downloaded dataset, compile and
run the Apache Beam pipeline (`src` folder and `pom.xml` file).

**Using Docker**: Running `docker-compose -f docker-compose.yml up -d` will set up an Apache Airflow webserver
with a UI accessible at `localhost:8080`. Triggering the open-food-facts-DAG will fetch the Open Food Facts 
dataset, compile and run the Apache Beam pipeline and clean up the results into a single file.