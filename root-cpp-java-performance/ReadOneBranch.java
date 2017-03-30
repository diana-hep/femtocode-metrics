import hep.io.root.core.RootInput;
import hep.io.root.*;
import hep.io.root.interfaces.*;

public class ReadOneBranch {
    final static long itemsPerPrint = 100000L;
    static long lastTime = 0L;
    static long items = 0;

    private static void printout() {
        long now = System.nanoTime();
        System.out.println(String.format("%g ns/item", 1.0 * (now - lastTime) / itemsPerPrint));
        lastTime = now;
    }

    public static void main(String[] args) throws java.io.IOException, RootClassNotFound {
        String[] fileNames = {"Mu_Run2010B-Apr21ReReco-v1_AOD.root", "copy2.root", "copy3.root", "copy4.root", "copy5.root"};
        for (String fileName : fileNames) {
            System.out.println(fileName);

            double total = 0.0;

            RootFileReader reader = new RootFileReader(fileName);
            TTree tree = (TTree)reader.get("Events");

            TBranch branch = tree.getBranch("recoTracks_generalTracks__RECO.").getBranchForName("obj").getBranchForName("chi2_");
            TLeaf leaf = (TLeaf)branch.getLeaves().get(0);

            long[] startingEntries = branch.getBasketEntry();
            System.out.println(String.format("number of TBaskets %d", startingEntries.length - 1));
            
            lastTime = System.nanoTime();
            items = 0;

            for (int i = 0;  i < startingEntries.length - 1;  i++) {
                long endEntry = startingEntries[i + 1];

                // all but the last one
                for (long entry = startingEntries[i];  entry < endEntry - 1;  entry++) {
                    RootInput in = branch.setPosition(leaf, entry + 1);
                    long endPosition = in.getPosition();
                    in = branch.setPosition(leaf, entry);
                    while (in.getPosition() < endPosition) {
                        total += in.readFloat();

                        items += 1;
                        if (items % itemsPerPrint == 0) printout();
                    }
                }

                // the last one
                RootInput in = branch.setPosition(leaf, endEntry - 1);
                long endPosition = in.getLast();
                while (in.getPosition() < endPosition) {
                    total += in.readFloat();

                    items += 1;
                    if (items % itemsPerPrint == 0) printout();
                }
            }

            System.out.println(String.format("check total %g == 1.55104e+07 (%s)", total, Math.abs(total - 1.55104e+07) > 1e-12*1.55104e+07 ? "true" : "false"));
        }
    }
}
