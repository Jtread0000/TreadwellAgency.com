# Reception (office phone voice agent) — research handoff

**Status:** research only. No implementation exists in this repo.
**Purpose:** hand verified findings to the `~/phd-stack/reception` build thread so it
does not re-derive them. Every rate and policy statement below was checked against a
primary source on 2026-08-28; links included so they can be re-verified rather than
trusted.

---

## 1. Blocking finding: subscription auth for the brain

The decision to drive the agent with `claude -p` on a Pro/Max subscription conflicts
with Anthropic's Consumer Terms. Two independent statements:

Consumer Terms, prohibited uses:

> "Except when you are accessing our Services via an Anthropic API Key or where we
> otherwise explicitly permit it, to access the Services through automated or
> non-human means, whether through a bot, script, or otherwise."

And Anthropic's stated position on OAuth: subscription OAuth credentials are intended
exclusively for Claude Code and claude.ai. Using them in another product, tool, or
service violates the Consumer Terms. Developers building anything that calls Claude —
including via the Agent SDK — are directed to API key auth through the Console.

A phone line that answers itself and holds a conversation with a caller is automated
access under any reading. This is not a gray area and it is not a rate-limit question.

**What it costs to comply:** at ~200 conversation-minutes/month, metered API is
roughly **$2–9/month** depending on model (Haiku 4.5 ≈ $1.60, Sonnet 5 ≈ $3.60,
Opus 5 ≈ $9). Current published per-token rates: Opus 5 $5/$25 per MTok,
Sonnet 5 $2/$10, Haiku 4.5 $1/$5. Prompt caching on the static knowledge-base prefix
keeps the input side near the floor.

The "no API spend without approval" standing rule is a good rule. This is the request
for that approval, with the number attached. It is the cheapest line item in the system.

**Secondary problem, independent of terms:** `claude -p` spawns a CLI process per
turn — process start, auth handshake, full context resend, no warm connection. The
stated tolerance of "p50 > ~4s/turn" is already past the point where a phone call
feels broken; callers read ~1s of dead air as a dropped line. If that threshold is
kept, measure p95 too, and measure it on the Intel Mac under a real call, not warm.

---

## 2. Verified cost model (Twilio path)

Fixed:

| Item | Rate |
|---|---|
| Twilio local number | $1.15/mo |
| Pushover | $4.99 one-time per platform; 10k msgs/mo free |

Per minute:

| Component | Rate |
|---|---|
| Twilio inbound voice | $0.0085/min |
| Twilio outbound (transfer leg to cell) | $0.0140/min |
| ConversationRelay (managed STT+TTS+orchestration) | $0.0700/min |
| Call recording | $0.0025/min |
| Recording storage | $0.0005/min/mo |
| Transcription (batch / streaming) | $0.024 / $0.027 per min |

Twilio bills voice in 1-minute increments rounded up — a 25-second voicemail bills a
full minute.

The Media Streams path (what Reception is building) drops the $0.07/min
ConversationRelay fee and substitutes self-hosted STT/TTS. At 200 min/month that is
**~$14/month saved**, in exchange for owning VAD, endpointing, barge-in, and μ-law
framing. Reception has apparently already built barge-in, which is the expensive part,
so this trade has largely been paid for already.

---

## 3. Dead ends already checked — do not spend time here

**Google Voice.** No call-control API. No way to answer programmatically, receive
media, play audio, or transfer. The Workspace Voice API in the Admin SDK is
provisioning only. Personal Google Voice has no public API; the client libraries that
appear in search results are reverse-engineered against the web app and violate the
terms. Chaining GV → Twilio adds a caller-ID-destroying hop plus Google's spam
screening to save $1.15/month. Not viable.

**Sesame.** No public API. sesame.com is a personal-agent app plus eyewear hardware
slated for 2027 — no developer docs, no pricing, no signup. CSM-1B (Apache 2.0,
March 2025) is the 1B base model, not the model behind the Maya/Miles demo. Self-hosting
needs an always-warm GPU (~$100–300/mo) or cold-start latency that kills a call. JT
specifically likes these voices; the answer is that they are not purchasable today.

---

## 4. TTS notes relevant to the Kokoro choice

JT stated in the other thread that **af_heart is not his favorite voice.** Worth
knowing before it ships as the production voice.

Two things that cut against over-optimizing this:

- **Phone audio is 8kHz μ-law.** Narrowband strips most of the frequency range where
  TTS quality lives. The perceived gap between Kokoro and ElevenLabs is much smaller
  over a phone line than on monitors. Recommended cheap experiment: render the same
  greeting through both, downsample both to 8kHz μ-law and back, and A/B them. That
  settles the voice question empirically for ~20 minutes of work.
- **Kokoro throughput is hardware-dependent.** Published Apple Silicon figures are
  12–79x realtime (M1 Mini: 30s of audio in ~379ms). Reception measures **2.4x realtime
  on the Intel Mac** — 5–30x less headroom. At 2.4x a 6-second utterance takes ~2.5s to
  synthesize. Sentence-streaming hides most of that on the first sentence, but stacked
  on top of `claude -p` turn latency it is a real risk. Measure end-to-end
  caller-stops-speaking → first-audio-out, not TTS in isolation.

Available alternatives if the voice needs to change: ElevenLabs Flash v2.5 (~75ms TTFB,
best emotional range, bundled into ConversationRelay at no extra cost), Cartesia Sonic 3
(~40ms TTFA, $49/mo tier at this volume, not ConversationRelay-compatible).

---

## 5. Requirements from JT's original brief not visible in the Reception scope

Flagging as gaps to confirm, not as criticism — these may simply be v2.

1. **Live call screening and warm transfer.** JT's opening ask was that the agent can
   "connect the call to me if I want to accept." The mechanism: caller goes to hold,
   agent dials JT's cell with a whisper prompt ("Call from Dana Reyes about a late add —
   press 1 to accept, 2 to send to voicemail"), bridges on accept. The Reception scope
   list (hours, logistics, messages, appointment requests) has no transfer path. This is
   the single feature that most differentiates this from a smart answering machine.
2. **Pushover.** Explicitly requested, twice. Reception's artifacts are dashboard +
   JSON + wav. A dashboard JT has to go look at is not the same as a notification that
   reaches him while the caller is still on the line — the two are complementary, and
   the transfer flow depends on the push arriving during the call.
3. **Failure fallback.** A home-hosted service on a faculty line needs Twilio's
   **"Primary handler fails" URL** pointed at a static TwiML Bin that plays a message and
   records a voicemail. Without it, a sleeping Mac, an ISP blip, or a service restart
   gives callers dead air on JT's professional number. This is ~10 minutes of config and
   converts the worst-case failure from "broken" to "degraded."

---

## 6. Compliance and risk items

**Recording consent.** Reception records both legs to wav. Maryland is an all-party
consent state (Cts. & Jud. Proc. § 10-402), and this is a Maryland state university
line. The greeting must announce recording in its first sentence, before any caller
speech is captured. Confirm the institution's own policy too.

**FERPA.** Student voicemails, transcripts, and extracted messages are education-adjacent
records. Recommended: system prompt refuses grades/standing/individually identifiable
discussion and routes to email or office hours (Reception has this — good); plus a
**retention policy with automatic deletion** (transcripts and audio both), which is not
currently in the design. Indefinite local retention of student call audio is the exposure.

**Institutional approval.** Forwarding an official university line to a third-party
service may require clearance. This is the only item that can kill the project outright,
so it is worth asking early rather than after launch.

**Caller ID through the forward.** When a PBX forwards to an outside line, the call
often arrives showing the *university's* number, not the caller's. This breaks
whitelisting (ring known numbers straight through) and breaks callback from voicemail.
Reception's "always capture name + callback number" is the correct mitigation and should
stay regardless. **Test to run before building around it:** point a trial Twilio number
at a TwiML Bin that reads back `{{From}}`, forward the office line to it, call the office
line from a mobile, and hear which number comes through.

---

## 7. Public endpoint exposure

Reception asks JT to rule between Tailscale Funnel (scoped to the `/voice` WSS path) and
a ~$5 relay VPS. Both expose to the public internet; the standing "serve-never-funnel"
rule points at the relay. A third option is **Cloudflare Tunnel** — free, no port
forwarding, no static IP, stable hostname, TLS terminated, and it does not put a tailnet
node on the public internet.

Whichever is chosen, two hardening steps apply:

- **Validate Twilio's request signature** (`X-Twilio-Signature`) on every connection.
  Without it the endpoint accepts calls from anyone who finds the URL.
- **Allowlist Twilio's published IP ranges** at the relay/tunnel edge.

---

## 8. Where the surfaces should land

Reception has running code, a working local loop, and barge-in solved. This thread has
research and no implementation. **Reception should be the lead surface.** Nothing here
needs to be rebuilt — items 1–7 are inputs to that build, not a competing design.

## Sources

- Twilio US voice pricing — https://www.twilio.com/en-us/voice/pricing/us
- Twilio conversational AI pricing — https://www.twilio.com/en-us/products/conversational-ai/pricing
- ConversationRelay docs — https://www.twilio.com/docs/voice/twiml/connect/conversationrelay
- Anthropic Consumer Terms — https://www.anthropic.com/legal/consumer-terms
- Anthropic Help Center, subscription vs API — https://support.claude.com/en/articles/9876003
- Pushover pricing — https://pushover.net/pricing
- Cartesia pricing — https://cartesia.ai/pricing
- Sesame — https://www.sesame.com/
