"""[CURRENCY DEFINITION EVENT] / [CURRENCY CONVERSION EVENT] dispatch-routing regression.

Closes the PR1 acceptance criterion of plans/QR_SELF_SERVE_CURRENCY_PLAN.md (thread 27015):
the two currency tags must route to their correct, DISTINCT GAS webhook actions, and must not be
conflated. `parseAndProcessCurrencyConversionLogs` is the conversion (double-entry) processor in
GAS project 1orWgdG..., NOT the definition handler -- this pins that so a future "fix" cannot
re-point either tag at the other's handler.
"""

from __future__ import annotations

from truesight_dao_client.server import dispatch


def _route_for(tag):
    for tags, targets, enqueue in dispatch.ROUTING:
        tag_tuple = tags if isinstance(tags, tuple) else (tags,)
        if tag in tag_tuple:
            return targets, enqueue
    raise AssertionError(f"no routing entry for {tag}")


def test_currency_definition_routes_to_definition_handler():
    targets, enqueue = _route_for("[CURRENCY DEFINITION EVENT]")
    assert targets == [
        ("CURRENCY_DEFINITION", "processCurrencyDefinitionsFromTelegramChatLogs")
    ]
    assert enqueue is False


def test_currency_conversion_routes_to_conversion_handler():
    targets, enqueue = _route_for("[CURRENCY CONVERSION EVENT]")
    assert targets == [
        ("CURRENCY_CONVERSION_PROCESSING", "parseAndProcessCurrencyConversionLogs")
    ]
    assert enqueue is False


def test_currency_tags_are_not_conflated():
    definition = _route_for("[CURRENCY DEFINITION EVENT]")[0]
    conversion = _route_for("[CURRENCY CONVERSION EVENT]")[0]
    assert definition != conversion
    assert definition[0][0] != conversion[0][0]  # distinct env keys
    assert definition[0][1] != conversion[0][1]  # distinct GAS action names


def test_dispatch_event_fires_definition_webhook(monkeypatch):
    monkeypatch.setenv(
        "DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION", "https://example.test/exec"
    )
    seen = {}
    monkeypatch.setattr(
        dispatch.webhook_trigger,
        "trigger",
        lambda url, action: seen.update(url=url, action=action) or True,
    )
    dispatch.dispatch_event(
        "[CURRENCY DEFINITION EVENT]\n- Currency: X\n--------\nMy Digital Signature: s"
    )
    assert seen.get("action") == "processCurrencyDefinitionsFromTelegramChatLogs"
    assert seen.get("url") == "https://example.test/exec"


def test_definition_event_does_not_enqueue_inventory_snapshot(monkeypatch):
    monkeypatch.setenv(
        "DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION", "https://example.test/exec"
    )
    called = {}
    monkeypatch.setattr(dispatch.webhook_trigger, "trigger", lambda *a, **k: True)
    monkeypatch.setattr(dispatch.inventory_snapshot, "publish", lambda: called.update(p=True))
    dispatch.dispatch_event("[CURRENCY DEFINITION EVENT]\n- Currency: X")
    assert called.get("p") is None


def test_routing_table_is_well_formed():
    tags_seen = []
    for tags, targets, enqueue in dispatch.ROUTING:
        assert isinstance(enqueue, bool)
        assert targets, "every route needs at least one target"
        for target in targets:
            assert isinstance(target, tuple) and len(target) == 2, f"bad target {target!r}"
            env_key, action = target
            assert isinstance(env_key, str) and env_key
            assert isinstance(action, str) and action
        tag_tuple = tags if isinstance(tags, tuple) else (tags,)
        for tag in tag_tuple:
            assert tag.startswith("[") and tag.endswith("]"), f"malformed tag {tag!r}"
            assert tag not in tags_seen, f"duplicate tag {tag!r}"
            tags_seen.append(tag)
