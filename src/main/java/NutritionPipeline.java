import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;

public class NutritionPipeline {

    public static void main(String[] args) {

        PipelineOptions options = PipelineOptionsFactory.create();

        Pipeline p = Pipeline.create(options);

        p.apply(TextIO.read().from("openfood_sample.csv"))
            .apply(TextIO.write().to("result"));

        p.run().waitUntilFinish();
    }
}
