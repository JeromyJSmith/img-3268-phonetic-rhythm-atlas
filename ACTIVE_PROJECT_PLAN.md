# Active project workspace plan

Goal: changing the active project changes the whole app, not only Analyze/Play.

1. Add one active-project controller and an app-wide selector: demo, saved project,
   or empty/new. Save the current project before changing context.
2. Render project-specific overview, media/watch, pads, microscope, rhythm,
   lyrics, style prompts, events and comparison states. Retain the original
   prepared report only in explicitly selected demo mode.
3. Stop outgoing playback/voices; route transport and keyboard controls to the
   active source. Clear unavailable media, scores and phonetics. Audio-only
   projects must not display the demo video.
4. Persist project-owned lyrics, style intent/prompt, imported timed annotations
   and sampler settings. Keep old v1 projects readable using optional content
   defaults; do not change the IndexedDB object-store layout.
5. Provide honest missing-analysis states, editable text and validated timed
   annotation import. Automatic ASR/narrow IPA is not implemented by a tab switch;
   do not fabricate it or show the demo's annotations as the new song's results.
6. Verify source/unit tests and browser project A/B/demo/new switching, save and
   reload, transport, captions and missing-result states. Deploy on GitHub Pages
   and verify the main URL after deployment.

Acceptance: the name, media, events, lyric/prompt text and Play source all agree
with the active project. Returning to a saved project restores its own content.
Original-demo results only appear when Original demo is selected.
