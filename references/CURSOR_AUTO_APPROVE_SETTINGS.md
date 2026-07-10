# Cursor: Don’t require approving every single edit

These settings reduce how often Cursor asks you to approve each AI edit.

## What was set (in your User settings)

In **Cursor → Settings → Cursor Settings** (or **Cmd+,** then open the JSON via the icon), the following were added to your **User** `settings.json`:

- **`cursor.experimental.reviewWorkflow.enabled": false`**  
  Turns off the newer “review workflow” that can force a review step for more changes.

- **`cursor.fileReview.forceLegacyMode": true`**  
  Uses the older, simpler file-review behavior so you’re not forced through the new review flow for every change.

**File used:**  
`~/Library/Application Support/Cursor/User/settings.json`

## If you still have to approve too much

1. **Restart Cursor**  
   Fully quit and reopen Cursor so the settings take effect.

2. **Check for overrides**  
   Workspace or folder `.vscode/settings.json` or `.cursor` config can override User settings. Remove or adjust any `cursor.*` or `review.*` entries there if you want the same behavior everywhere.

3. **UI toggles**  
   In **Cursor → Settings → Features** (Chat & Composer), look for:
   - **Auto-Apply to files outside context**  
     When enabled, Composer can apply changes to files outside the current context without extra approval steps.
   - Any **Review** or **Apply**-related toggles  
     Disable or relax them if you want fewer confirmations.

4. **Optional: more “apply without review” behavior**  
   If Cursor adds or exposes more granular “auto apply” options in the future, enable those in the same Features / Chat & Composer section.

## Summary

- User settings were updated so you **don’t need to auto-approve every single edit** in the same way as before.
- Restart Cursor after changing these. If something still forces approval, check workspace settings and the Features toggles above.
