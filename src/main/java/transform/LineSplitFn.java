package transform;

import dataset.Dataset;
import org.apache.beam.sdk.transforms.DoFn;

import java.util.HashMap;
import java.util.Map;

/**
 * Split the tab-seperated values to a Map, using the predefined {@link Dataset} header.
 * The line containing the header itself is ignored.
 */
public class LineSplitFn extends DoFn<String, Map<String, String>> {

    private static final String SPLIT_SYMBOL = "\t";

    @ProcessElement
    public void processElement(@Element String input, OutputReceiver<Map<String, String>> receiver) {
        String[] tokens = input.split(SPLIT_SYMBOL);
        if (Dataset.HEADER[0].equals(tokens[0])) {
            //ignore header
            return;
        }
        Map<String, String> datasetMap = new HashMap<>();
        for (int i=0; i<tokens.length; i++) {
            datasetMap.put(Dataset.HEADER[i], tokens[i]);
        }
        receiver.output(datasetMap);
    }

}
