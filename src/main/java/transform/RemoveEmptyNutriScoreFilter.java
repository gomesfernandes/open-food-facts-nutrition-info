package transform;

import org.apache.beam.sdk.transforms.SerializableFunction;
import org.apache.commons.lang3.StringUtils;

import java.util.Map;

public class RemoveEmptyNutriScoreFilter implements SerializableFunction<Map<String, String>, Boolean> {

    @Override
    public Boolean apply(Map<String, String> input) {
        return StringUtils.isNotEmpty(input.get("nutriscore_grade"));
    }

}
