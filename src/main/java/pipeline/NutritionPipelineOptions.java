package pipeline;

import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.PipelineOptions;

public interface NutritionPipelineOptions extends PipelineOptions {
    @Description("Path of the file to read from (local file or Google Cloud Storage bucket)")
    @Default.String("openfood_sample.csv")
    String getInputFile();
    void setInputFile(String value);

    /** Set this required option to specify where to write the output. */
    @Description("Path of the file to write to (local file or Google Cloud Storage bucket)")
    @Default.String("results/open-food-facts-result")
    String getOutputFile();
    void setOutputFile(String value);
}
