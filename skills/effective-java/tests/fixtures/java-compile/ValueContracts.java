import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public final class ValueContracts {
    public static final class Digest {
        private final byte[] bytes;

        public Digest(byte[] bytes) {
            this.bytes = Objects.requireNonNull(bytes, "bytes").clone();
        }

        public byte[] bytes() {
            return bytes.clone();
        }

        @Override
        public boolean equals(Object other) {
            return other instanceof Digest digest && Arrays.equals(bytes, digest.bytes);
        }

        @Override
        public int hashCode() {
            return Arrays.hashCode(bytes);
        }
    }

    public record SearchResult(List<String> hits) {
        public SearchResult {
            hits = List.copyOf(hits);
        }
    }

    public static void main(String[] args) {
        byte[] source = {1, 2, 3};
        Digest first = new Digest(source);
        Digest second = new Digest(new byte[] {1, 2, 3});
        source[0] = 9;
        byte[] exposed = first.bytes();
        exposed[1] = 9;
        assert first.equals(second);
        assert first.hashCode() == second.hashCode();
        assert Arrays.equals(first.bytes(), new byte[] {1, 2, 3});

        var search = new SearchResult(List.of("a", "a", "b"));
        assert search.hits().equals(List.of("a", "a", "b"));
        try {
            search.hits().add("c");
            throw new AssertionError("expected unmodifiable list");
        } catch (UnsupportedOperationException expected) {
            // Contract proven.
        }
    }
}
