# Final owner handoff — 2026-11-10

## Reviewable packet

- `writeup/preview.html`: standalone manuscript preview, all six images embedded.
- `writeup/notebook_preview.html`: redesigned notebook reading preview, code hidden and reports collapsible.
- `writeup/kaggle_upload.zip`: exact editor title/description/body, six ordered PNGs and upload guide.
- `writeup/reviewer_brief.md`: questions ready for an optional outside cold read.
- `reports/writeup_judging_review.md`: internal rubric review, resolved wording issues and claim sources.
- `writeup/writeup.md`: complete manuscript and nine-row table; 1,926 conservative words.
- `writeup/submission_packet.zip`: manuscript, preview, notebook/metadata, six PNGs,
  evaluation CSV and verification/source notes. No raw or intermediate data.
- `notebooks/submission.ipynb`: standalone nine-CSV rebuild, with saved report outputs from verified cloud results.
- Notebook target: https://www.kaggle.com/code/oppenheimer6th/combine-movement-to-nfl-decisions-an-evidence-map .
  Redesigned public version 4 (notebook ID 144208320) is verified by API with ten clean report outputs and six figures. Full clean Kaggle execution was version 3 (979.82 s; sampled peak 1107.0 MiB). Exact proof: `kaggle_execution.json`. Check actual browser access/rendering.

Full clean local run: 523.08 seconds; largest sampled stage RSS 1,183 MiB. All 402 numeric comparisons, 25 cohort scores and 12 tests pass. No frozen prediction source/model/sample changed. Reported results and figure captions retain uncertainty, prior 2025 exposure and selected-subset limitations. Official field/track/rules checks: `official_sources.md`.

## Owner UI steps

The project's recorded allocation leaves final terms, track confirmation and Kaggle Submit
with the owner. Preparation and notebook publication are separate from competition submission.

1. Read the preview and inspect notebook execution/outputs under **oppenheimer6th**, the
   account confirmed November 10. Complete a fresh-kernel owner execution check if practical.
2. Open the competition Writeup editor. Choose **University Track** (ID 7289), which requires
   every team member to be an undergraduate. Confirm your actual status and any evidence request.
3. Unzip `writeup/kaggle_upload.zip`. Copy the exact title/description from its README or
   `editor_fields.json` and paste `WRITEUP.md` as the body. Upload its six numbered PNGs and
   replace local image paths with editor-generated links. Keep the one evaluation table.
4. Attach the exact public Kaggle notebook using its code URL. Preview the saved draft and
   verify figures, table, citations and attachment. A local HTML preview cannot prove the
   Kaggle editor's upload/attachment rendering.
5. Review any presented terms and submit the team's one final Writeup when satisfied, by
   the internal December 28 deadline (hard deadline January 6, 2027, 23:59 UTC).
6. Save the writeup URL/submission confirmation and notebook version, then update
   `reports/submission_checklist.md`. Do not mark submission complete before confirmation.

No further hypothesis search, route-gate weakening or post-evaluation tuning is needed.
Keep November 20 as the final claim review checkpoint; later changes address presentation,
documented errors or already specified checks.

## Writeup revision — November 10

The revised introduction and worked receiver conversation explain concrete drill/film questions.
Cohort consistency does not certify an individual player, and the map is a proposed aid with
untested decision usefulness. The upload package counts title, description and body together
and remains below 2,000 words. All six figures and the generated nine-row table are retained.
No Writeup draft was saved on Kaggle: the available SDK Writeup methods are read-only and
this session has no browser editor tool. Final image upload, notebook attachment and owner
track/terms/Submit remain in the UI.
