package transform;

import generators.TestDataGenerator;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import java.util.Map;

@RunWith(JUnit4.class)
public class FormatOutputFnTest {

    public FormatOutputFn formatter = new FormatOutputFn();

    @Test
    public void formatToReadableOutput() {
        final Map<String, String> mappedData = TestDataGenerator.generateDataMap1();

        String formattedOutput = formatter.apply(mappedData);

        Assert.assertEquals("Vitória crackers: ", formattedOutput);
    }
}
