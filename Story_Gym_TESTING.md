# Story Gym – Full Testing Documentation

## Overview

This document provides a structured and comprehensive testing process for the **Story Gym** Django application.

The purpose of this file is to verify that the application works correctly across:
- functionality
- usability
- responsiveness
- authentication
- permissions
- data-driven content
- defensive and edge-case behaviour

Unlike a static front-end project, Story Gym includes **database-backed features**, **user accounts**, **CRUD functionality**, **comments**, **ratings**, **search/filter/sort**, and a **password reset flow**. For this reason, testing covers both visual behaviour and Django-specific workflows.

This file is written in a **page-by-page format** so the testing process mirrors the actual user journey through the site.

---

## Test Setup (applies to every table below)

### Viewports (DevTools → Toggle device toolbar)
- **Large / Desktop:** 1280×800 (also spot-check 1440×900)
- **Medium / Tablet:** 768×1024 (Lenovo Tab M10 Plus preset)
- **Small / Mobile:** 360×800 (Android) and 390×844 (Samsung Galaxy S25 preset)

### Browsers
- Chrome (latest)
- Firefox (latest)
- Safari (if available)

### Common DevTools tools used
- **Elements → Styles/Computed**: check font size, line-height, spacing, overflow, fixed widths, and background behaviour
- **Console**: check JavaScript errors/warnings during page load and interactions
- **Network**: confirm CSS, JS, image assets, form posts, redirects, and password reset requests succeed or fail gracefully
- **Application / Storage**: confirm session-related behaviour where relevant
- **Lighthouse**: spot-check accessibility, best practices, and layout quality after major changes
- **Rendering/Emulation**: check zoom, DPR, reduced motion, and touch simulation

### Accounts used during testing
To test authentication and permissions correctly, three accounts should be prepared:

- **User A** – standard registered user
- **User B** – second standard registered user
- **Admin** – superuser account for `/admin/` checks

### Data setup used during testing
Before running the full test suite, prepare the following records:
- at least **2 published stories** by User A
- at least **1 published story** by User B
- at least **1 draft story**
- stories in **different genres**
- at least **1 story with no comments**
- at least **1 story with multiple comments**
- at least **1 story already rated**
- at least **1 repository search term that returns no results**

### Pass / Fail notes
- Use **Pass** only if the expected outcome is met exactly.
- Use **Fail** if the result differs from the expectation and note the issue clearly.
- If a test mostly works but exposes a visual or usability weakness, record it under **Known Issues / Improvements**.

---

## Global Cross-Page Checks (run on every page)

These checks apply to all templates that inherit from the shared base template.

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| GX-L-01 | Navbar visibility | Open each main page and inspect navbar alignment | Navbar renders consistently; no broken alignment; links readable |  |
| GX-L-02 | Auth-based nav state | Log out → inspect navbar; log in → inspect navbar again | Logged-out view shows Login/Register; logged-in view shows greeting + Logout + navigation links |  |
| GX-L-03 | Footer visibility | Scroll to footer on every page | Social icons visible, aligned, and not overlapping footer text |  |
| GX-L-04 | External link behaviour | Click Facebook / Instagram / X links | External links open correctly; original site remains intact |  |
| GX-L-05 | Favicon presence | Check browser tab icon on multiple pages | Favicon is visible; no broken default tab icon |  |
| GX-L-06 | Console cleanliness | Navigate through main pages with Console open | No recurring JS errors caused by counters, ratings, mesh, or page layout |  |
| GX-L-07 | Typography consistency | Compare headings, body text, buttons, and labels across templates | Consistent visual hierarchy with no abrupt style mismatches |  |
| GX-L-08 | Zoom resilience | Check key pages at 90%, 100%, 110%, and 125% browser zoom | No clipping, overlap, or unusable controls |  |
| GX-L-09 | Keyboard focus visibility | Tab through links, buttons, inputs, and selects | Visible focus state present; tab order follows page logic |  |
| GX-L-10 | Refresh behaviour | Hard refresh several pages | CSS, JS, and images reload correctly; no broken layout after refresh |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| GX-M-01 | Breakpoint transition | Resize from 820px → 768px → 740px | Layout adapts cleanly; navbar and content panels do not break |  |
| GX-M-02 | Navbar collapse | Use collapsed menu and open/close it repeatedly | Menu opens and closes reliably; links remain usable |  |
| GX-M-03 | Footer wrap | Inspect footer at tablet width | Icons remain clickable; footer text wraps neatly |  |
| GX-M-04 | Touch-target usability | Use touch simulation and tap nav links / buttons | Controls respond on first tap; no tiny hit areas |  |
| GX-M-05 | Horizontal overflow | Scroll all main pages horizontally and vertically | No unexpected horizontal scroll |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| GX-S-01 | No horizontal scroll anywhere | Swipe sideways on all key pages | No sideways overflow |  |
| GX-S-02 | Hamburger menu usability | Open and close mobile nav repeatedly | Menu behaves reliably; no trapped state |  |
| GX-S-03 | Tap-target size | Tap near edges of buttons and links | Taps register; controls are large enough for touch |  |
| GX-S-04 | Text wrapping | Check long titles, usernames, story titles, and form hints | Text wraps naturally; no clipped words or overlap |  |
| GX-S-05 | Performance feel | Navigate through several pages on mobile | No major lag, white flashes, or broken transitions |  |

---

## PAGE 1 — Home Page (`index.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| HP-L-01 | Page loads cleanly | Load home page → open DevTools Console | No console errors on initial load; page renders fully |  |
| HP-L-02 | Hero heading readability | Inspect the main `h1` and supporting paragraph | Heading readable; text does not overlap image or CTA block |  |
| HP-L-03 | Hero image display | Inspect hero image | Image loads correctly; no blur, distortion, or broken file |  |
| HP-L-04 | Main CTA routing | Click hero “Start here” button | Redirects correctly to Randomizer page |  |
| HP-L-05 | Feature cards visibility | Scroll to three article cards | All three cards visible, aligned, and evenly spaced |  |
| HP-L-06 | Feature card images | Inspect all three images | Images load correctly; no stretching or accidental cropping |  |
| HP-L-07 | Article card links | Click each “Read more” button | Opens the correct article page |  |
| HP-L-08 | Quote section layout | Inspect quote section and CTA | Quote readable; CTA card visible and balanced |  |
| HP-L-09 | Explore stories CTA | Click “Explore stories” | Opens repository page correctly |  |
| HP-L-10 | Flash message behaviour | Trigger a success message and return to home page | Message appears clearly and does not break layout spacing |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| HP-M-01 | Hero reflow | Set viewport to 768×1024 | Hero columns reflow cleanly; no overlap |  |
| HP-M-02 | CTA block fit | Inspect CTA content at tablet width | CTA remains readable; button fully visible |  |
| HP-M-03 | Feature card stacking | Inspect feature cards at tablet width | Cards stack or resize consistently; spacing remains balanced |  |
| HP-M-04 | Quote section fit | Inspect quote section at 768px | Text remains readable and centered |  |
| HP-M-05 | Join section spacing | Inspect final join section | Section remains visually balanced and usable |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| HP-S-01 | No horizontal scroll | Set 360×800 and swipe horizontally | No sideways scroll |  |
| HP-S-02 | Hero readability | Check H1, intro, and image without zoom | Readable; no huge text pushing content off-screen |  |
| HP-S-03 | Feature card stacking | Scroll to article cards | Cards stack vertically with consistent spacing |  |
| HP-S-04 | Button tap targets | Tap all home CTAs | Buttons respond on first tap |  |
| HP-S-05 | Section spacing on mobile | Scroll from hero to footer | No sections collapse into each other; no clipped text |  |

---

## PAGE 2 — “What’s New?” Article (`article_whats_new.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AWN-L-01 | Page loads cleanly | Open page and inspect Console | No console errors; page renders correctly |  |
| AWN-L-02 | Two-column layout | Inspect left and right columns | Columns align correctly; no overlap or imbalance |  |
| AWN-L-03 | Intro text readability | Read first content section | Paragraphs have good spacing and readable line length |  |
| AWN-L-04 | Overlay image section | Inspect “Be Part of the Journey” block | Overlay text remains readable over image |  |
| AWN-L-05 | Mailto link | Click email link | Default mail client opens correctly |  |
| AWN-L-06 | “Coming Soon” block | Inspect heading, paragraph, and image | Content aligned correctly; image not distorted |  |
| AWN-L-07 | Final quote styling | Scroll to quote block | Quote remains visually distinct and centered |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AWN-M-01 | Column reflow | Set 768×1024 | Columns stack or shrink cleanly; no overlap |  |
| AWN-M-02 | Overlay readability | Inspect overlay text at tablet width | Text remains legible and unclipped |  |
| AWN-M-03 | Mailto tap usability | Tap email link in touch simulation | Link easy to activate and visible |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AWN-S-01 | Mobile stacking | View page at 360px width | All sections stack cleanly; no horizontal overflow |  |
| AWN-S-02 | Overlay image block on mobile | Inspect image + overlay | Text remains inside overlay and readable |  |
| AWN-S-03 | Paragraph wrapping | Inspect all long text blocks | Lines wrap naturally; no overflow |  |

---

## PAGE 3 — “Prompts for Storytelling” Article (`article_prompts_story.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| APS-L-01 | Page loads cleanly | Open page and inspect Console | No console errors |  |
| APS-L-02 | Hero banner structure | Inspect hero title, image, and text block | Hero remains aligned; image and text box balanced |  |
| APS-L-03 | Two-card row layout | Inspect second row | Cards align evenly; mini image remains proportional |  |
| APS-L-04 | Light / dark card contrast | Inspect split section | Text contrast remains readable on all card styles |  |
| APS-L-05 | Final CTA button | Click final “Start here” button | Navigates to Randomizer page correctly |  |
| APS-L-06 | Tips card readability | Inspect “A Few Helpful Hints” section | Text readable; no overlap with surrounding panel |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| APS-M-01 | Hero reflow on tablet | Inspect hero at 768px | Hero components stack/reflow cleanly |  |
| APS-M-02 | Card row reflow | Inspect multi-card rows | Cards remain readable; no squeezed text |  |
| APS-M-03 | Bottom split layout | Inspect final section | CTA remains visible and well spaced |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| APS-S-01 | No horizontal scroll | View at 360px and swipe sideways | No sideways overflow |  |
| APS-S-02 | Section stacking | Scroll through all rows | All boxes stack in a readable order |  |
| APS-S-03 | CTA tap usability | Tap “Start here” in final CTA | Button works on first tap |  |

---

## PAGE 4 — “Writing Tips” Article (`article_writing_tips.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AWT-L-01 | Page loads cleanly | Open page and inspect Console | No console errors |  |
| AWT-L-02 | Hero split layout | Inspect hero title and overlay text box | Both sides align well against background image |  |
| AWT-L-03 | Side quote section | Inspect quote-line section | Quote remains centered and visually clear |  |
| AWT-L-04 | Main text block readability | Read central content area | Comfortable line spacing and no crowding |  |
| AWT-L-05 | Four-box grid | Inspect all four boxes | Cards align correctly; subtitles and lists readable |  |
| AWT-L-06 | Final quote block | Inspect bottom quote section | Quote remains centered and distinct |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AWT-M-01 | Hero stack/reflow | Set viewport 768×1024 | Hero reflows cleanly with no clipping |  |
| AWT-M-02 | Split-section stacking | Inspect mid-row layout | Quote section and text section stack or resize correctly |  |
| AWT-M-03 | Four-box readability | Inspect box content at tablet width | Text remains readable; no overflow in list items |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AWT-S-01 | No horizontal scroll | View at 360px and swipe sideways | No sideways overflow |  |
| AWT-S-02 | Box stacking order | Scroll down the full page | Boxes stack in a logical and readable sequence |  |
| AWT-S-03 | List readability on mobile | Inspect list items in grid section | Bullets and text remain readable without overlap |  |

---

## PAGE 5 — Login Page (`login.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| LP-L-01 | Page loads cleanly | Open login page → Console | No console errors; form renders correctly |  |
| LP-L-02 | Label/input alignment | Inspect username and password fields | Labels aligned correctly with inputs; no clipping |  |
| LP-L-03 | Empty submit handling | Submit with both fields empty | Form rejects invalid login; user remains on page |  |
| LP-L-04 | Invalid credentials | Enter wrong username/password | Error message shown; login blocked |  |
| LP-L-05 | Valid login flow | Enter valid User A credentials | User logs in successfully and redirect works |  |
| LP-L-06 | Forgot password link | Click “Forgot password?” | Redirects correctly to password reset form |  |
| LP-L-07 | Register link | Click “Create account” | Redirects correctly to register page |  |
| LP-L-08 | Autocomplete behaviour | Click into username/password fields | Browser respects autocomplete attributes appropriately |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| LP-M-01 | Layout collapse | Set viewport to 768×1024 | Two-column panel reflows cleanly into stacked layout |  |
| LP-M-02 | Form width | Inspect input width at tablet size | Inputs fit panel without overflow |  |
| LP-M-03 | Button alignment | Inspect login and signup buttons | Buttons remain centered and fully visible |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| LP-S-01 | Mobile usability | Open login page at 360px width | Form fully usable without horizontal scroll |  |
| LP-S-02 | Keyboard overlap | Focus username and password fields | Inputs remain visible when mobile keyboard appears |  |
| LP-S-03 | Full-width buttons | Inspect buttons on mobile | Buttons expand appropriately and remain tappable |  |

---

## PAGE 6 — Register Page (`register.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| RP-L-01 | Page loads cleanly | Open register page → Console | No console errors; form renders correctly |  |
| RP-L-02 | Form hint readability | Inspect hints for username, password, email, and DOB | Hints readable and visually associated with inputs |  |
| RP-L-03 | Empty submit handling | Submit form with all fields blank | Form errors shown; account not created |  |
| RP-L-04 | Username validation | Enter invalid username / existing username | Relevant validation message shown |  |
| RP-L-05 | Password mismatch | Enter different values in password fields | Validation error shown; registration blocked |  |
| RP-L-06 | Weak/invalid password | Enter password failing project rules | Validation error shown |  |
| RP-L-07 | Invalid email | Enter malformed email address | Validation error shown |  |
| RP-L-08 | DOB age restriction | Enter DOB below 18 or above 99 boundary if validation exists | Invalid age rejected with appropriate message |  |
| RP-L-09 | Valid registration | Enter complete valid data | New user account created successfully |  |
| RP-L-10 | Post-register redirect/message | Complete registration and follow redirect | Success message visible; user flow continues correctly |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| RP-M-01 | Panel fit on tablet | Inspect register panel at 768px | Panel fits viewport; no clipped text |  |
| RP-M-02 | Form spacing | Inspect vertical spacing between fields | Inputs and errors remain separated and readable |  |
| RP-M-03 | Date input usability | Tap date input / use picker | Date field remains usable and visible on tablet |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| RP-S-01 | Mobile form fit | Open register page on 360px width | All inputs fit screen; no horizontal overflow |  |
| RP-S-02 | Error message wrapping | Trigger multiple field errors | Error messages wrap cleanly and remain readable |  |
| RP-S-03 | Date picker visibility | Use mobile date picker | Native picker opens and closes correctly |  |

---

## PAGE 7 — Password Reset Request (`password_reset_form.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRF-L-01 | Page loads cleanly | Open reset form page | No console errors; form visible |  |
| PRF-L-02 | Empty submit handling | Submit with no email | Validation error shown or browser blocks invalid input |  |
| PRF-L-03 | Invalid email format | Enter malformed email and submit | Error shown; request blocked |  |
| PRF-L-04 | Existing email flow | Submit valid email attached to account | Redirects to “check your email” page |  |
| PRF-L-05 | Non-existing email flow | Submit email not linked to account | Same generic success page shown; no account leakage |  |
| PRF-L-06 | Back-to-login CTA | Click “Back to login” | Returns to login page correctly |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRF-M-01 | Layout collapse | Inspect reset form at tablet width | Panel stacks/reflows cleanly |  |
| PRF-M-02 | Input width | Inspect email field | Input fits panel without overflow |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRF-S-01 | Mobile fit | Open form at 360px width | No horizontal scroll; field and button fully visible |  |
| PRF-S-02 | Tap usability | Tap email field and submit button | Controls easy to use on mobile |  |

---

## PAGE 8 — Password Reset “Email Sent” (`password_reset_done.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRD-L-01 | Confirmation page load | Complete password reset request flow | “Check your email” page loads correctly |  |
| PRD-L-02 | Messaging clarity | Read explanatory text | Text is clear and does not reveal whether account exists |  |
| PRD-L-03 | Back to login CTA | Click “Back to login” | Redirects correctly to login page |  |

### Medium / Small Screen

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRD-R-01 | Responsive panel fit | View on tablet and mobile | Layout remains readable and centered |  |

---

## PAGE 9 — Password Reset Confirm (`password_reset_confirm.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRC-L-01 | Valid link form display | Open a valid password reset link | New password form appears |  |
| PRC-L-02 | Empty submit handling | Submit with blank password fields | Errors shown; password not changed |  |
| PRC-L-03 | Mismatched passwords | Enter different values in two fields | Validation error shown |  |
| PRC-L-04 | Invalid password rules | Enter invalid password according to Django rules | Validation error shown |  |
| PRC-L-05 | Successful reset | Enter valid matching password twice | Password changed successfully |  |
| PRC-L-06 | Invalid / expired link branch | Open expired or malformed reset link | “Invalid or expired” message displayed; request-new-link CTA visible |  |
| PRC-L-07 | Request new link CTA | Click “Request a new link” | Redirects to reset form page |  |

### Medium / Small Screen

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRC-R-01 | Responsive form fit | View valid and invalid-link states on tablet/mobile | Layout remains readable; buttons usable |  |

---

## PAGE 10 — Password Reset Complete (`password_reset_complete.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRCOMP-L-01 | Completion page load | Finish successful password reset | “Password changed” page loads correctly |  |
| PRCOMP-L-02 | Login CTA | Click “Log in” | Redirects correctly to login page |  |

### Medium / Small Screen

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRCOMP-R-01 | Responsive fit | View page on tablet/mobile | Layout remains centered and readable |  |

---

## PAGE 11 — Randomizer (`randomizer.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| RZ-L-01 | Initial state page | Open randomizer without existing words in session | Intro page with “Start” button is shown |  |
| RZ-L-02 | Generate words flow | Click “Start” | Random prompt words are generated and result page appears |  |
| RZ-L-03 | Word count completeness | Inspect generated result card | Exactly six prompt elements display |  |
| RZ-L-04 | Visual spacing of words | Inspect randomizer word pills | Words wrap neatly; no overlap or clipping |  |
| RZ-L-05 | Write now CTA | Click “Write now” | Redirects correctly to story writing page |  |
| RZ-L-06 | Draw again behaviour | Click “Draw again” | New set of words appears; page does not crash |  |
| RZ-L-07 | Multiple rapid re-draws | Click “Draw again” repeatedly | No layout break, JS error, or duplicate-button bug |  |
| RZ-L-08 | No-session fallback | Clear session / open flow fresh | App safely shows initial state rather than broken result view |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| RZ-M-01 | Intro panel fit | Inspect intro layout on tablet | Panel remains centered and readable |  |
| RZ-M-02 | Result card fit | Generate words and inspect card | Word chips wrap correctly; buttons remain visible |  |
| RZ-M-03 | Button stacking | Inspect action cards at tablet width | Action buttons remain usable and aligned |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| RZ-S-01 | Mobile intro fit | Open initial randomizer page at 360px width | No horizontal scroll; content centered |  |
| RZ-S-02 | Word wrapping on mobile | Generate words and inspect result | Long/random words wrap cleanly within pills and card |  |
| RZ-S-03 | Action buttons on mobile | Tap “Write now” and “Draw again” | Buttons are large enough and respond on first tap |  |

---

## PAGE 12 — Story Editor / Write Page (`my_story.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| MS-L-01 | Page load with prompt words | Open story editor after using randomizer | Prompt words display correctly in header |  |
| MS-L-02 | Title input visibility | Inspect title field | Field visible, usable, and styled consistently |  |
| MS-L-03 | Genre select visibility | Inspect genre dropdown | Dropdown visible, labelled, and usable |  |
| MS-L-04 | Textarea usability | Click into story textarea and type long text | Textarea accepts input; no layout shift |  |
| MS-L-05 | Character counter works | Type into story field and observe counter | Counter updates in real time |  |
| MS-L-06 | Save draft flow | Use “Save for later” | Story saved as draft; no crash; success flow works |  |
| MS-L-07 | Publish flow | Use “Send to the world” | Story saved/published successfully |  |
| MS-L-08 | Clear story flow | Use “Nope, clear all” | Story content clears or expected flow executes safely |  |
| MS-L-09 | Draft-to-published edit branch | Open an existing published story in edit mode | Correct button state shown for editing/published branch |  |
| MS-L-10 | Edit mode delete button | Open existing story in edit mode | Delete button visible only where expected |  |
| MS-L-11 | Empty submission handling | Submit without required content/title as applicable | Validation prevents bad submission |  |
| MS-L-12 | Spaces-only input | Enter only spaces and attempt submit | Validation prevents invalid content if implemented |  |
| MS-L-13 | Long content stress test | Paste very long story text | Layout remains usable; textarea and counter behave |  |
| MS-L-14 | Special characters/emoji | Enter punctuation, quotes, HTML-like text, emoji | Input accepted/displayed safely without breaking layout |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| MS-M-01 | Editor panel fit | Inspect story editor at 768px | Main panel fits cleanly with no clipping |  |
| MS-M-02 | Counter placement | Type text and inspect counter location | Counter remains anchored in visible position |  |
| MS-M-03 | Button wrapping | Inspect footer action buttons | Buttons wrap cleanly without overlap |  |
| MS-M-04 | Textarea height | Inspect textarea on tablet | Height remains usable for writing |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| MS-S-01 | Mobile editor fit | Open story editor on mobile | No horizontal scroll; title and textarea visible |  |
| MS-S-02 | Keyboard behaviour | Focus story textarea on mobile | Input remains visible when mobile keyboard appears |  |
| MS-S-03 | Full-width action buttons | Inspect footer buttons on mobile | Buttons stack vertically and remain tappable |  |
| MS-S-04 | Prompt header wrapping | Inspect generated words header on mobile | Long prompt line wraps without overflow |  |

---

## PAGE 13 — Story Preview + Comments (`preview_story.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PV-L-01 | Story title display | Open preview page for published story | Title visible and centered correctly |  |
| PV-L-02 | Story meta block | Inspect generated words, genre, author, and date | Metadata displays correctly and wraps safely |  |
| PV-L-03 | Story content rendering | Inspect main story box | Story displays with preserved line breaks and readable spacing |  |
| PV-L-04 | Empty-comments state | Open story with no comments | “No comments yet.” message shown cleanly |  |
| PV-L-05 | Logged-out comment state | Log out and open preview page | Comment form hidden; login/register CTA shown instead |  |
| PV-L-06 | Logged-in comment state | Log in and open preview page | Comment form visible and usable |  |
| PV-L-07 | Comment character counter | Type into comment field | Counter updates in real time |  |
| PV-L-08 | Star rating UI | Click stars in rating widget | Visual stars update to selected rating |  |
| PV-L-09 | Submit valid comment | Enter text and submit | Comment appears in list after submit |  |
| PV-L-10 | Empty comment submit | Submit blank comment | Validation blocks submission |  |
| PV-L-11 | Spaces-only comment | Submit only spaces | Validation blocks submission if implemented |  |
| PV-L-12 | Edit comment mode | Open own comment for editing | Form switches into edit mode; Cancel button visible |  |
| PV-L-13 | Cancel edit | Click Cancel while editing | Returns to normal preview page state |  |
| PV-L-14 | Delete own comment | Delete own comment | Comment removed successfully |  |
| PV-L-15 | Own comment action visibility | Inspect comments authored by logged-in user | Edit/Delete controls visible only on own comments |  |
| PV-L-16 | Other users’ comment protection | Log in as another user and inspect comments | Edit/Delete controls absent for comments not owned by current user |  |
| PV-L-17 | Story author rating restriction | Open own story as author | “You cannot rate your own story” message shown |  |
| PV-L-18 | Repeat rating restriction | Rate a story, then return | Repeat rating prevented according to app rules |  |
| PV-L-19 | Many comments stress test | Open story with many comments | Comment list remains readable and scrollable without layout break |  |
| PV-L-20 | Long comment text stress test | Add long comment text | Comment wraps safely; no overflow |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PV-M-01 | Preview panel fit | Inspect story preview at 768px | Story panel remains readable and centered |  |
| PV-M-02 | Comments grid collapse | Inspect comments area | Two-column comment layout collapses cleanly to one column |  |
| PV-M-03 | Rating control fit | Use star rating UI at tablet width | Stars remain visible and tappable |  |
| PV-M-04 | Action button fit | Inspect Edit/Delete buttons in comment list | Buttons remain visible and aligned |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| PV-S-01 | Story meta wrapping | Inspect metadata block on mobile | Metadata stacks without overlap |  |
| PV-S-02 | Story box readability | Scroll story content on mobile | Content remains readable; no clipped paragraphs |  |
| PV-S-03 | Comment form usability | Type comment on mobile | Textarea usable; keyboard does not hide essential controls |  |
| PV-S-04 | Rating/tap usability | Tap star rating on mobile | Stars respond correctly to touch |  |
| PV-S-05 | Comment buttons on mobile | Inspect Edit/Delete buttons | Buttons remain usable and not too small |  |

---

## PAGE 14 — Repository (`repo.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| REPO-L-01 | Page loads cleanly | Open repository page → Console | No console errors; page renders fully |  |
| REPO-L-02 | Latest story block | Inspect latest published story preview | Latest story data displays correctly; read-more CTA visible |  |
| REPO-L-03 | No-latest fallback | Test state with no published stories if possible | Friendly fallback message shown |  |
| REPO-L-04 | Search field usability | Type query into title search field | Input accepts text and remains aligned |  |
| REPO-L-05 | Search with matching result | Submit search for known existing story title | Matching stories displayed correctly |  |
| REPO-L-06 | Search with no result | Submit query with no matches | “No results found” message shown correctly |  |
| REPO-L-07 | Sort newest | Select “Newest” and submit | Stories ordered newest first |  |
| REPO-L-08 | Sort oldest | Select “Oldest” and submit | Stories ordered oldest first |  |
| REPO-L-09 | Sort liked | Select “Most liked” and submit | Stories ordered by average rating/likes as implemented |  |
| REPO-L-10 | Genre filter | Select genre and submit | Only matching stories displayed |  |
| REPO-L-11 | Combined search + filter | Use search + sort + genre together | Combined filtering works without breaking layout |  |
| REPO-L-12 | Clear button visibility | Apply query/sort and inspect clear button | Clear button appears when expected |  |
| REPO-L-13 | Clear filter action | Click clear button | Returns repository to default state |  |
| REPO-L-14 | Story row layout | Inspect repository rows with long titles | Titles wrap safely; metadata remains aligned |  |
| REPO-L-15 | Rating display | Inspect rows with and without ratings | Rated stories show value correctly; unrated show fallback text |  |
| REPO-L-16 | “More” CTA | Click More on a story row | Opens story preview page correctly |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| REPO-M-01 | Two-column panel collapse | Inspect repository at tablet width | Latest story and repository sections stack cleanly |  |
| REPO-M-02 | Search form reflow | Inspect search/sort/filter controls | Controls remain aligned and readable |  |
| REPO-M-03 | Story row wrapping | Inspect rows at tablet width | Title, author, date, and genre wrap without overlap |  |
| REPO-M-04 | Latest story text area | Inspect preview block | Text remains readable with no clipping |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| REPO-S-01 | Mobile repository fit | Open page on 360px width | No horizontal overflow |  |
| REPO-S-02 | Filter controls stacking | Inspect search/sort/filter row | Controls stack vertically and remain usable |  |
| REPO-S-03 | Story meta mobile layout | Inspect repository rows | Metadata rearranges cleanly; More button still accessible |  |
| REPO-S-04 | Search and clear on mobile | Search and then clear results | Both actions usable on touch devices |  |

---

## PAGE 15 — Account Page (`account.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AC-L-01 | Auth protection | Open account page while logged out | Access blocked or redirected to login as expected |  |
| AC-L-02 | Welcome header | Log in and open account page | Username shown correctly in welcome heading |  |
| AC-L-03 | User repository list | Inspect stories list | User’s own stories appear correctly with dates/status |  |
| AC-L-04 | Empty repository fallback | Test account with no stories | “You do not have any stories yet.” shown cleanly |  |
| AC-L-05 | Published story actions | Inspect published story row | Open/Edit/Delete buttons visible where expected |  |
| AC-L-06 | Draft story actions | Inspect draft story row | Continue draft + Delete visible where expected |  |
| AC-L-07 | Delete confirmation | Use delete form on one story | Confirmation prompt appears before delete submits |  |
| AC-L-08 | Latest published story card | If user has latest published story, inspect extra card | View-latest CTA appears only when condition is met |  |
| AC-L-09 | “Start here” CTA | Click “Start here” in right-hand card | Redirects to randomizer page |  |
| AC-L-10 | “Get inspired” CTA | Click repository inspiration CTA | Redirects to public story repository |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AC-M-01 | Layout collapse | Inspect account layout at tablet width | Main columns reflow cleanly |  |
| AC-M-02 | Story row fit | Inspect account rows on tablet | Date, title, and action buttons remain readable |  |
| AC-M-03 | Right card stacking | Inspect account CTA cards | Cards stack properly and remain balanced |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| AC-S-01 | Mobile fit | Open account page on 360px width | No horizontal scroll; content centered |  |
| AC-S-02 | Story action buttons | Inspect story rows on mobile | Buttons remain visible and tappable |  |
| AC-S-03 | Empty-state readability | Inspect no-story state on mobile | Fallback message remains readable and centered |  |

---

## PAGE 16 — Custom 404 Page (`404.html`)

### Large Screen (Desktop ≥ 1024px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| E404-L-01 | Trigger 404 via invalid route | Open a non-existent internal URL | Custom 404 page loads correctly |  |
| E404-L-02 | Branding / visual consistency | Inspect 404 page styling | Page remains visually consistent with overall project style |  |
| E404-L-03 | Countdown visible | Inspect countdown area | Countdown text visible and readable |  |
| E404-L-04 | Countdown decreases | Wait and observe seconds value | Countdown decreases each second |  |
| E404-L-05 | Auto-redirect | Wait until countdown completes | User is redirected to homepage |  |
| E404-L-06 | Manual recovery link | Click homepage return link | Redirects immediately to homepage |  |

### Medium Screen (Tablet ~768px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| E404-M-01 | Typography scaling | Inspect page at 768px width | “404” and supporting text remain readable and centered |  |
| E404-M-02 | Countdown and link fit | Inspect countdown and manual link | Both remain visible and unclipped |  |

### Small Screen (Mobile ≤ 414px)

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| E404-S-01 | Mobile layout | View 404 page at 360px | No horizontal scroll; content centered |  |
| E404-S-02 | Countdown legibility | Inspect countdown on mobile | Readable without zoom; no overlap |  |
| E404-S-03 | Manual link tap | Tap homepage recovery link | Returns to homepage correctly |  |

---

## Django CRUD & Permission Testing

This section tests application rules that are not limited to one template, but are essential for a database-backed project.

### Story CRUD

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| CRUD-ST-01 | Create story | Generate random words → write story → publish | New story is stored and visible in repository/preview |  |
| CRUD-ST-02 | Save draft | Create story and choose draft action | Story saved as draft and shown correctly on account page |  |
| CRUD-ST-03 | Update own story | Edit a story owned by User A | Changes saved and reflected immediately |  |
| CRUD-ST-04 | Delete own story | Delete a story owned by User A | Story removed successfully |  |
| CRUD-ST-05 | Back button after delete | Delete story then use browser Back | Deleted story does not reappear as valid content |  |
| CRUD-ST-06 | Deleted story URL | Delete story then open old preview URL | 404 or safe handling shown; no broken internal error |  |
| CRUD-ST-07 | Create story while logged out | Try to access write flow while logged out | Access blocked or redirected to login |  |
| CRUD-ST-08 | Edit other user’s story via URL | Log in as User B and open User A’s edit URL | Access denied, redirected, or 404 |  |
| CRUD-ST-09 | Delete other user’s story via URL | Log in as User B and submit delete for User A story | Access denied, redirected, or 404 |  |
| CRUD-ST-10 | Draft/published state branch | Change story state between draft and published | Correct actions and visibility update across pages |  |

### Comment CRUD / Rating Rules

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| CRUD-CM-01 | Create comment | Logged in as User B, comment on User A story | Comment saved and appears correctly |  |
| CRUD-CM-02 | Edit own comment | Edit comment as its author | Comment updates successfully |  |
| CRUD-CM-03 | Delete own comment | Delete own comment | Comment removed successfully |  |
| CRUD-CM-04 | Edit other user’s comment | Log in as another user and inspect comment actions | Edit control absent or access denied |  |
| CRUD-CM-05 | Delete other user’s comment | Submit delete attempt for another user comment | Access denied or action unavailable |  |
| CRUD-CM-06 | Rate another user’s story | Submit comment with rating on another user story | Rating saved and reflected in repository average |  |
| CRUD-CM-07 | Rate own story | Open own story preview | Rating blocked with explanatory message |  |
| CRUD-CM-08 | Re-rate same story | Rate story once, then revisit | Repeat rating prevented according to app rules |  |

---

## JavaScript Testing

This section tests behaviours controlled by `main.js`.

### Triangle Mesh Background

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| JS-MESH-01 | Mesh script loads | Open any page using base template with Console open | `main.js` loads without runtime errors |  |
| JS-MESH-02 | SVG renders | Inspect background visually | Triangle mesh is visible behind content |  |
| JS-MESH-03 | Mouse interaction | Move mouse across screen on desktop | Nearby triangle strokes increase in visibility / opacity |  |
| JS-MESH-04 | No interference with content | Click links/buttons over mesh background | Background does not block interaction with page elements |  |
| JS-MESH-05 | Resize resilience | Resize browser window repeatedly | Mesh remains present; no visible script break |  |

### Character Counters

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| JS-COUNT-01 | Story counter initial state | Open story editor | Story counter shows current value on load |  |
| JS-COUNT-02 | Story counter update | Type into story textarea | Counter increments live |  |
| JS-COUNT-03 | Comment counter initial state | Open story preview comment form | Comment counter shows current value on load |  |
| JS-COUNT-04 | Comment counter update | Type into comment textarea | Counter increments live |  |
| JS-COUNT-05 | Safe fallback on unrelated pages | Open pages without story/comment textarea | No JS errors caused by missing elements |  |

### Star Rating Widget

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| JS-RATE-01 | Widget loads where eligible | Open comment form on a story user can rate | Star row appears only when rating is allowed |  |
| JS-RATE-02 | Click interaction | Click 1–5 stars in sequence | Star visuals update to selected value |  |
| JS-RATE-03 | Hidden input linkage | Submit a rating after clicking stars | Submitted rating matches selected star value |  |
| JS-RATE-04 | Safe fallback on pages without rating widget | Open unrelated pages | No JS errors caused by missing rating elements |  |

---

## CSS / Visual Quality Testing

This section focuses on global CSS behaviour and page polish rather than business logic alone.

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| CSS-01 | Global word wrapping | Inspect long story titles, usernames, and comments | Text wraps instead of overflowing containers |  |
| CSS-02 | Button hover/active states | Hover and click primary buttons across pages | Visual state changes are consistent and readable |  |
| CSS-03 | Navbar underline animation | Hover nav links | Underline animation works smoothly |  |
| CSS-04 | Main surface background | Inspect `.main-surface` pages | Dark surface panel appears consistently and centers content |  |
| CSS-05 | Image scaling | Inspect images across home/article/story pages | Images preserve aspect ratio and do not distort |  |
| CSS-06 | Panel shadows/borders | Inspect cards and dark panels | Borders and shadows remain subtle but visible |  |
| CSS-07 | Mobile button width | Inspect buttons on small screens | Buttons expand or stack appropriately |  |
| CSS-08 | Overflow handling | Inspect long content on mobile and tablet | No clipped text or unmanaged overflow |  |

---

## Security / Defensive Behaviour Testing

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| SEC-01 | Logged-out access to protected pages | Attempt to open account / write / edit pages while logged out | User is redirected or blocked appropriately |  |
| SEC-02 | URL tampering for story edit | Manually change story ID in edit URL to another user story | Access denied or 404 |  |
| SEC-03 | URL tampering for story delete | Submit delete on another user’s story | Access denied or safe handling |  |
| SEC-04 | URL tampering for comment edit/delete | Try direct URLs/actions for another user’s comment | Access denied or action unavailable |  |
| SEC-05 | CSRF-sensitive forms | Submit POST actions through normal interface | CSRF-protected forms work correctly; no accidental anonymous mutations |  |
| SEC-06 | Password reset account privacy | Submit existing and non-existing emails | Response does not reveal whether account exists |  |
| SEC-07 | HTML/script-like input | Enter `<script>` or HTML-like text in comment/story fields | Content does not execute as code; page remains safe |  |
| SEC-08 | Emoji and special characters | Submit emoji, quotes, ampersands, punctuation | Content displays correctly without breaking layout |  |

---

## Browser Behaviour / Recovery Testing

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| BR-01 | Refresh after submit | Submit comment/story then refresh page | No duplicate submission or broken state |  |
| BR-02 | Back after delete | Delete story or comment then use browser Back | Deleted content does not become valid again |  |
| BR-03 | Multi-tab editing | Open same story edit page in two tabs and save different changes | Behaviour remains stable; final saved state consistent |  |
| BR-04 | Session continuity | Generate words, navigate to story editor, then continue workflow | Prompt/session data remains available where expected |  |
| BR-05 | Invalid object ID | Manually visit non-existent story ID | Safe error handling (404 or equivalent) |  |

---

## Empty-State & Edge-Case Testing

| Test ID | What to test | Test steps (very specific) | Expected result | Pass / Fail |
|---|---|---|---|---|
| EDGE-01 | No published stories | Test repository when no published stories exist | Friendly fallback message shown |  |
| EDGE-02 | No user stories | Open account page for user with no stories | Friendly empty-state message shown |  |
| EDGE-03 | No comments | Open story with no comments | Clean “No comments yet.” state shown |  |
| EDGE-04 | Very long title | Create story with very long title | Title wraps safely in preview/repository/account |  |
| EDGE-05 | Very long comment | Submit long comment | Comment wraps safely; no layout break |  |
| EDGE-06 | Search with empty result | Search non-existent title | Clear “No results found” state shown |  |
| EDGE-07 | Genre with no matching stories | Filter by genre that currently has no stories | Clean empty-state result shown |  |
| EDGE-08 | Repeated randomizer use | Generate words many times | No performance collapse or broken UI |  |

---

## Validation Testing

### HTML Validation
All rendered HTML pages should be checked using the **W3C HTML Validator**.

Recommended pages to validate:
- Home
- Login
- Register
- Randomizer
- Story editor
- Story preview
- Repository
- Account
- Article pages
- 404 page

### CSS Validation
Custom CSS should be checked with the **W3C CSS Validator**.

Recommended files:
- `global.css`
- `pages.css`

### Python / Django Validation
Python files should be checked for:
- PEP8 compliance
- readable naming
- consistent indentation
- absence of unused imports
- absence of commented-out dead code in production version

### JavaScript Validation
`main.js` should be checked with:
- ESLint or JSHint
- browser Console during real interactions

---

## Lighthouse Testing

Run Lighthouse on the live site for key pages and record the results below.

| Page | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| Home |  |  |  |  |
| Randomizer |  |  |  |  |
| Story Editor |  |  |  |  |
| Story Preview |  |  |  |  |
| Repository |  |  |  |  |
| Login |  |  |  |  |

---

## Bugs Found & Fixed

Use this section to document real bugs clearly and honestly.

| Bug | Cause | Fix | Result |
|---|---|---|---|
| Example: Genre filter not applying correctly | Selected genre value was not being compared correctly in the view/template logic | Corrected comparison and confirmed selected option persists in template | Fixed |
|  |  |  |  |
|  |  |  |  |

---

## Known Issues / Improvements

This section should be used for minor issues that do not break the application but could be improved later.

| Issue | Impact | Planned improvement |
|---|---|---|
|  |  |  |
|  |  |  |

---

## Testing Summary

Story Gym was tested across **desktop, tablet, and mobile** layouts using a combination of:
- manual interaction testing
- responsive inspection
- edge-case checks
- Django workflow checks
- CRUD and permission testing
- JavaScript behaviour testing
- defensive/security-aware validation

The application was tested not only for the **happy path**, but also for:
- invalid inputs
- protected-route access
- URL tampering attempts
- empty-state rendering
- repeated actions
- long-content resilience
- cross-device usability

This testing approach demonstrates that Story Gym is not only visually styled, but also **functionally structured, defensive in behaviour, and appropriate for a database-backed full-stack application**.
