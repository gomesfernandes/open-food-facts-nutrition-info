package transform;

import generators.TestDataGenerator;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.testing.PAssert;
import org.apache.beam.sdk.testing.TestPipeline;
import org.apache.beam.sdk.transforms.Create;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

@RunWith(JUnit4.class)
public class LineSplitFnTest {

    @Test
    public void splitLineByTabAndIgnoreHeader() {
        final List<String> LINES = TestDataGenerator.generateDatasetContent();
        final Map<String, String> mapOfFirstLine = TestDataGenerator.generateDataMap1();
        final Map<String, String> mapOfSecondLine = TestDataGenerator.generateDataMap2();
        final List<Map<String, String>> mapResults = Arrays.asList(mapOfFirstLine, mapOfSecondLine);
        LineSplitFn lineSplitFn = new LineSplitFn();
        Pipeline p = TestPipeline.create();
        PCollection<String> rawLines = p.apply(Create.of(LINES));

        PCollection<Map<String, String>> output = rawLines.apply(ParDo.of(lineSplitFn));

        PAssert.that(output).containsInAnyOrder(mapResults);
    }

}
