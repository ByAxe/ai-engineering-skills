package org.acme;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.Executors;

@Path("/risks")
@ApplicationScoped
@Named("risky")
public class RiskyResource {
    @Inject
    EntityManager entityManager;

    Map<String, Object> mutableState = new HashMap<>();
    private final ThreadLocal<byte[]> requestBuffer = ThreadLocal.withInitial(() -> new byte[1024]);

    public record Digest(byte[] bytes) {}
    public record SearchResult(List<String> hits) {}

    @GET
    public Uni<List<String>> list() {
        var values = List.of("a", "b").stream().toList();
        values.add("fallback");
        Files.readAllBytes(Path.of("report.txt"));
        return Uni.createFrom().item(values);
    }

    public BigDecimal price() {
        return new BigDecimal(0.1);
    }

    public byte[] bytes() {
        return "payload".getBytes();
    }

    public String unsafeOptional(Optional<String> value) {
        return value.get();
    }

    public long parallelCount() {
        return new ArrayList<>(List.of("a", "b")).parallelStream().count();
    }

    public void detachedExecutor() {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            synchronized (this) {
                executor.submit(() -> requestBuffer.get().length);
            }
        }
    }

    public void swallow() {
        try {
            throw new IllegalStateException("fixture");
        } catch (Exception ignored) {
        }
        System.out.println("fixture");
    }

    @Transactional
    private void persistInternally() {
        entityManager.flush();
    }
}
