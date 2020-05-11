package transform;

import generators.TestDataGenerator;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import java.util.Map;

@RunWith(JUnit4.class)
public class RemoveEmptyNutriScoreFilterTest {

    public RemoveEmptyNutriScoreFilter removeEmptyNutriScoreFilter = new RemoveEmptyNutriScoreFilter();

    @Test
    public void returnTrueWhenNutriscoreGradeIsPresent() {
        final Map<String, String> mappedData = TestDataGenerator.generateDataMap1();
        mappedData.put("nutriscore_grade", "c");

        Boolean result = removeEmptyNutriScoreFilter.apply(mappedData);

        Assert.assertEquals(Boolean.TRUE, result);
    }

    @Test
    public void returnFalseWhenNutriscoreGradeIsAbsent() {
        final Map<String, String> mappedData = TestDataGenerator.generateDataMap1();

        Boolean result = removeEmptyNutriScoreFilter.apply(mappedData);

        Assert.assertEquals(Boolean.FALSE, result);
    }
}