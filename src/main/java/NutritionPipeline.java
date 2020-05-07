import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptionsFactory;

public class NutritionPipeline {

    public static void main(String[] args) {
        PipelineOptionsFactory.register(NutritionPipelineOptions.class);
        NutritionPipelineOptions options = PipelineOptionsFactory
                                            .fromArgs(args)
                                            .withValidation()
                                            .as(NutritionPipelineOptions.class);
        Pipeline p = Pipeline.create(options);

        p.apply(TextIO.read().from(options.getInputFile()))
            .apply(TextIO.write().to(options.getOutputFile()));

        p.run().waitUntilFinish();
    }
}
