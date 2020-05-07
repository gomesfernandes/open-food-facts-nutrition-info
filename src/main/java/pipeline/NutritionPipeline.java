package pipeline;

import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.ParDo;
import transform.FormatOutputFn;
import transform.LineSplitFn;
import transform.RemoveEmptyNutriScoreFilter;

/**
 * Defines the main Apache Beam pipeline for processing the Open Food Facts dataset
 */
public class NutritionPipeline {

    public static void main(String[] args) {
        PipelineOptionsFactory.register(NutritionPipelineOptions.class);
        NutritionPipelineOptions options = PipelineOptionsFactory
                                            .fromArgs(args)
                                            .withValidation()
                                            .as(NutritionPipelineOptions.class);
        Pipeline p = Pipeline.create(options);

        p.apply(TextIO.read().from(options.getInputFile()))
            .apply(ParDo.of(new LineSplitFn()))
            .apply(Filter.by(new RemoveEmptyNutriScoreFilter()))
            .apply(MapElements.via(new FormatOutputFn()))
            .apply(TextIO.write().to(options.getOutputFile()));

        p.run().waitUntilFinish();
    }

}
