
## Apache Beam pipeline in Java

The original dataset can be found here: <https://www.data.gouv.fr/fr/datasets/open-food-facts-produits-alimentaires-ingredients-nutrition-labels/>

This dataset is made available by [Open Food Facts](https://fr.openfoodfacts.org/data) 
under the [Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1.0/).
 


### Run options

Available run options : 
```
  --inputFile=<String>
    Default: openfood_sample.csv
    Path of the file to read from (local file or Google Cloud Storage bucket)
  --outputFile=<String>
    Default: results/open-food-facts-result
    Path of the file to write to (local file or Google Cloud Storage bucket)
```