package transform;

import org.apache.beam.sdk.transforms.SimpleFunction;
import java.util.Map;

public class FormatOutputFn extends SimpleFunction<Map<String, String>, String> {

    @Override
    public String apply(Map<String, String> input) {
        String productName = input.get("product_name");
        String nutriScore = input.get("nutriscore_grade");
        return productName + ": " + nutriScore;
    }

}
