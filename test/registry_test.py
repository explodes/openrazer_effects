def test_registry_not_empty():
    from ore.registry.registry import REGISTRY
    assert len(REGISTRY) > 0
