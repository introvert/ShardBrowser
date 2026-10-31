// Phone profiles get Chrome for Android's API set through Blink's own switches.
import { test } from "node:test";
import assert from "node:assert/strict";
import {
  ANDROID_ONLY_BLINK_FEATURES,
  DESKTOP_ONLY_BLINK_FEATURES,
  androidBlinkSwitches,
} from "../dist/profile.js";

test("a phone turns off the desktop-only APIs", () => {
  const { switches, rest } = androidBlinkSwitches([]);
  assert.deepEqual(switches, [
    `--disable-blink-features=${DESKTOP_ONLY_BLINK_FEATURES.join(",")}`,
    `--enable-blink-features=${ANDROID_ONLY_BLINK_FEATURES.join(",")}`,
  ]);
  assert.deepEqual(rest, []);
});

test("the caller's blink switches are folded in and win", () => {
  const { switches, rest } = androidBlinkSwitches([
    "--disable-blink-features=AutomationControlled,OrientationEvent",
    "--lang=de",
    "--enable-blink-features=NotificationConstructor",
  ]);
  assert.deepEqual(rest, ["--lang=de"]);
  const off = switches[0].split("=")[1].split(",");
  assert.ok(off.includes("AutomationControlled") && off.includes("OrientationEvent") && off.includes("WebHID"));
  assert.ok(!off.includes("NotificationConstructor"));
  assert.deepEqual(switches.slice(1), ["--enable-blink-features=NotificationConstructor"]);
});
