# 独立判定用50件（LLMの回答は含まない）

判定手引き `validation/codebook.md` を読み、各報告のタイトルと収録本文だけで判断する。
`human_answers.json` の is_actual_bug、primary_category、issue_domain、confidence、rationale を記入する。
development_labels.jsonl は回答が終わるまで開かない。画像・動画の中身や現在のGitHub本文では補完しない。
判断できないときは unknown とし、理由を残す。画像等の5項目は今回は記入不要。

## 1. Pulled bodies are not woken up when the puller moves

space-wizards/space-station-14#1717

````text
I still seem to have some waking issues even with this fix, when pulling.

_Originally posted by @PJB3005 in https://github.com/space-wizards/RobustToolbox/pull/1235#issuecomment-674535397_
````

## 2. Whirlpool sounds are broken

vcmi/vcmi#1749

````text
**Describe the bug**
Both ambient sounds while hero is next to whirlpool and visitation sounds are somehow broken - they either disappear completely or play at completely different volume

**To Reproduce**
Steps to reproduce the behavior:
1. Launch map Carpe Diem
2. Use vcmihanar / vcmiainur and reach harbor to north-west from starting position
3. Get on ship and sail to whirlpool in south-east corner of map
4. Listen to sounds

**Expected behavior**
- ambient sounds near whirlpool play as usual
- visitation sound plays as usual

**Actual behavior**
- ambient sounds seems to disappear completely once you're off favorable winds
- whirlpool visit sound starts playing at very low volume
- sailing away sometimes leads to whirlpool volume getting louder

**Did it work earlier?**
Unknown

**Version**
- vcmi beta 1.2
- reproduced both on Windows and Linux systems
````

## 3. Reconfigured fast-forward key is not interpreted as character input for dialogs

endless-sky/endless-sky#4880

````text
**Describe the bug**
When rebound to a character allowed in names / dialogs, the fast forward command key toggles the game's state, rather than being used as a character literal.

**To Reproduce**
Steps to reproduce the behavior:
1. Rebind FF to `t` 
2. Open the ship info panel
3. Click the ship. Name field
4. Try to enter the character in question, e.g. attempt to set the name "Tilted Terror"

**Expected behavior**
The FF command key should only be intercepted while in-flight

**Screenshots**
n/a

**System (please complete the following information):**
 - Version: 0.9.11

**Link to save file**
n/a

**Additional context**
Reported on discord: 
https://discordapp.com/channels/251118043411775489/536900466655887360/684680299401052226

Caused by #4741 
````

## 4. Draft packs are being passed right-&gt;left-&gt;right, table image shows them being passed left-&gt;right-&gt;left

magefree/mage#8075

````text
Since the 1.4.49v1 update drafts packs are being passed backwards, going right->left->right instead of the traditional left->right->left. However, the table image still shows them passing left->right->left.

I believe the bug causing them to be passed in the wrong direction is here...
https://github.com/magefree/mage/blob/06ae494c5b0695d8a5ca8af5bf7b97abfb4fbf85/Mage/src/main/java/mage/game/draft/BoosterDraft.java#L27-L31

... as `((boosterNum + 1) % 2 == 1)` would be false for odd numbered packs.

(That function starts counting boosters from 1, other places seem to count from 0... very confusing!)

````

## 5. Neutral army skips the turn while fighting with them by using Battle AI

vcmi/vcmi#3550

````text
**Describe the bug**
While fighting with neutral army, their creatures often do nothing and skip the turn, if using battle AI for them.


**To Reproduce**
Steps to reproduce the behavior:
1. Set neutral AI as Battle AI.
2. Battle with a neutral army without flying and range creatures
3. See error

**Expected behavior**
They will wait and close to player's army in the end of this turn.

**Actual behavior**
 If AI creatures cannot enter the attack range within one turn, they will skip the turn automatically.

**Did it work earlier?**
It worked well in 1.42.

**Version**
 - OS: Windows
 - Version: 1.44

````

## 6. There are two light blue towels

space-wizards/space-station-14#33068

````text
**Screenshots**
<!-- If applicable, add screenshots to help explain your problem. -->

![image](https://github.com/user-attachments/assets/51e27413-5cf6-4e08-906c-caf646278558)

````

## 7. [1846] Cannot payout if at top of Market

tobymao/18xx#1163

````text
When clicking the pay out button, nothing happens because IC is already at the max stock price and so price cannot change. It should be able to pay out but not increase in price. Game continues as normal if IC witholds, so it seems to be the top of market issue. https://www.18xx.games/game/4737
````

## 8. Game links in /blog aren&#x27;t automatically embedded anymore

lichess-org/lila#11862

````text
Due to https://github.com/lichess-org/lila/commit/c7044679ef9942d7c2f34f64fad6191bc91e3c0c I guess.

Blog posts need to pre-expand them server-side like ublogs and the forum do.
````

## 9. &quot;Blood lust&quot; spell animation over &quot;mirrored&quot; unit is missing

ihhub/fheroes2#790

````text
No animation, while casting "Blood lust"spell over clone, made my "Mirror Image" spell.
````

## 10. Admin PDA inserts into slimes when health analyzing 

space-wizards/space-station-14#29412

````text
## Description
<!-- Explain your issue in detail. Issues without proper explanation are liable to be closed by maintainers. --> 

when in aghost health analyzing pdas will insert into a slimes internal storage rather than scan them


**Reproduction**
<!-- Include the steps to reproduce if applicable. --> 
this is NOT an issue with pdas while adminned as a urist. This problem occurs exclusively when scanning a slime as a ghost. It's possible that being adminned is irrelevant and the issue is the ghost part, but the only ghosts with hands are admins so *shrugs*

**Additional context**
<!-- Add any other context about the problem here. Anything you think is related to the issue. --> 
I talked briefly with Shadowcommander about this in the discord and he mentioned it was possibly due to the bypassing of certain "checks" when ghosted or adminned (or both?)

````

## 11. Some prone enemies force the game to freeze and become untouchable

ja2-stracciatella/ja2-stracciatella#1822

````text
[//]: # (Thank you for taking the time to report an issue or propose an enhancement. Questions are also welcome.)
[//]: # (If you have more than one item to report, please open separate issues!)

[//]: # (This text will not be visible and you can freely delete it. Check the Preview tab for a cleaner look.)

### What is wrong
prone enemies in sectors are unable to be interacted with force the game into a time clock freeze 

[//]: # (For bugs, please fill in this table [otherwise delete it]. The lines don't have to stay aligned.)

| JA2S version | Game version        | Vanilla bug? | Used to work? |
| ------------ | ------------------- | ------------ | ------------- |


V0.20.0-git+439a6d3(build  (04.12.02) |   JA2 Gold | no | yes 

[//]: # (Please also include:)


save files https://ufile.io/ihr85yt1 all of them but quicksave.sav. Run into the building in alma and try to interact with the prone soldier

OS: Windows 10 enterprise IOT LTSC 21H2
//]: # (- how to reproduce the bug and, if possible, a save game)
[//]: # (- the operating system)
[//]: # (- in case you know, for enhancements, if this feature was already added by some other source mod like 1.13)

[//]: # (When pasting backtraces or any other logs with hashed enumerations, please format it as a code block.)
[//]: # (You can do that by selecting it and clicking the "<>" icon or manually putting three backticks [```] at each end.)
[ja2.log](https://github.com/ja2-stracciatella/ja2-stracciatella/files/11406066/ja2.log)


````

## 12. Campaign info window, flickering buttons when pressing mouse on a button&#x27;s shadow

ihhub/fheroes2#4499

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Linux

### Describe the bug

When pressing the left mouse button on the shadow of any of the buttons in the Campaign info window the button switches rapidly between pressed and released state, until the mouse press is released or the mouse pointer is moved away from the button.  (I've tried to record the video, but unfortunately the flickering is not visible on the recording.)

The reason for the issue seems to be that the (pre-rendered) shadow is part of the released button sprite, but the pressed sprite doesn't include the shadow and therefore has smaller area (e.g. `CAMPXTRE` sprites 0 and 1 — the two states of the "View Intro" button):

![image](https://user-images.githubusercontent.com/489601/138827756-935f025f-3b56-4045-b1c5-fc276b738e6e.png) ![image](https://user-images.githubusercontent.com/489601/138828311-1331c475-ee3a-4076-99bf-2dbe7db0c6d1.png)

It doesn't hurt that clicking the button shadow activates the button, IMO, but the flickering is not nice.  We could, if we like it, extend the clickable area of the pressed button to match that of the released one: that would eliminate the flickering.

### Save file

No save file is needed.

### Additional info

_No response_
````

## 13. D2K - Almost all weapons are blocked by walls

openra/openra#12756

````text
In original game only Combat Tank and Devastator bullets were blocked by walls and turrets. On our OpenRA D2K mod, Weapons except Turrets, Siege Tank, Missile Tank, Sonic Tank and Deviator are blocked.

Also looks like Devastator has unnecessarily `Blockable: true` on it.
````

## 14. 1893 AGV giving a share to the wrong player

tobymao/18xx#5807

````text
When I bought a 5th share of AGV, it gave it to another player in game#46583. It shows me as president with 40% and the other player has 50% though.
````

## 15. Campaign scenario selection, scenario description translation language sticks after switching once

ihhub/fheroes2#4941

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Linux

### Describe the bug

1. Start the game and switch the language, for example, to French:
   ![image](https://user-images.githubusercontent.com/489601/150628658-6e8e00a2-77a9-413d-9e74-582e5a150b4b.png)

2. Start a new campaign, observe the correct translation use:
   ![image](https://user-images.githubusercontent.com/489601/150628677-7c7a50f8-a11c-45b4-be50-c66648189b7b.png)

3. Cancel the campaign and switch the language, e.g. back to English:
   ![image](https://user-images.githubusercontent.com/489601/150628709-fddaecd8-4818-408e-884e-d1014a322214.png)

4. Start a new campaign again, observe the bug — mixed languages:
   ![image](https://user-images.githubusercontent.com/489601/150628507-ebbc7f22-6559-4205-a43e-0e5f6e2704a7.png)

Switching the languages further only seems to affect the bonus choice (translated correctly), but not the scenario description text: this sticks until the game is restarted.

### Save file

No save file is needed to reproduce.

### Additional info

_No response_
````

## 16. 1860: Game allows insolvent company to lay track with terrain costs

tobymao/18xx#3802

````text
See the title.

Per the 1860 rules, p. 13, "An insolvent company must retain revenue, may not place base tokens, **and may not upgrade track or build track that would incur a cost**. "

https://18xx.games/game/26419?action=241

I just was able to lay a terrain track as the IOW (currently insolvent), just to try it.   I "did the right thing" in the game and did NOT lay it, but hopefully you can find the bug.   Here's a screenshot just in case:

![image](https://user-images.githubusercontent.com/66023744/107715179-b4dccf80-6c9c-11eb-9e35-aff78c841edd.png)

````

## 17. Failed to build with latest nightly rustc.

thomas-mauran/chess-tui#117

````text
<!--
Hi there, sorry `chess-tui` is not working as expected.
Please fill this bug report conscientiously.
A detailed and complete issue is more likely to be processed quickly.
-->

## Description
Failed to build with latest rustc due to deprecated feature `[stdsimd]` in `ahash`. Successfully built when use `rustc 1.78.0-nightly (b11fbfbf3 2024-02-03)` (an older nightly version) or stable rustc.
<!--
A clear and concise description of what the bug is.
-->

## To Reproduce
```shell
rustup update
rustup default nightly # should be 1.85.0 in 2024-12-04
git clone https://github.com/thomas-mauran/chess-tui
cd chess-tui
cargo build --release
```
<!--
Try to reduce the issue to a simple code sample exhibiting the problem.
Ideally, fork the project and add a test or an example.
-->

## Expected behavior
Built successfully.
<!--
A clear and concise description of what you expected to happen.
-->

## Error message

<!--
If applicable, add screenshots, gifs or videos to help explain your problem.
-->

```
cargo build --release
   Compiling ahash v0.8.6
error[E0635]: unknown feature `stdsimd`
  --> ~/.cargo/registry/src/rsproxy.cn-0dccff568467c15b/ahash-0.8.6/src/lib.rs:99:42
   |
99 | #![cfg_attr(feature = "stdsimd", feature(stdsimd))]
   |                                          ^^^^^^^

For more information about this error, try `rustc --explain E0635`.
error: could not compile `ahash` (lib) due to 1 previous error
```

## Environment

<!--
Add a description of the systems where you are observing the issue. For example:
- OS: Linux
- Terminal Emulator: xterm
- Font: Inconsolata (Patched)
- Crate version: 0.7
- Backend: termion
-->

- OS: Ubuntu 22.04.5 LTS on Windows 10 x86_64
- Terminal Emulator: vscode
- Font: consolas
- Crate version: 1.5.0
- Backend: none

## Additional context

Rustc: rustc 1.85.0-nightly (c44b3d50f 2024-12-03)

Update `ahash` to `0.89` and above may solve the problem. Run `cargo tree -i ahash` and we get:

```plaintext
ahash v0.8.6
└── hashbrown v0.14.3
    └── lru v0.12.1
        └── ratatui v0.28.1
            └── chess-tui v1.5.0 (/home/adamska/chess-tui)
```

So update `ratatui` may solve this problem, but I'm not sure which version the is most appropriate. Or just compile with stable rustc.

<!--
Add any other context about the problem here.
If you already looked into the issue, include all the leads you have explored.
-->

````

## 18. Multiplayer countdown timer displays incorrectly

quaver/quaver#3525

````text
The countdown in autohost games counts up to 90 instead of counting down to 0
````

## 19. Combat, the result of an instant combat is different from the result of a combat played in automatic mode from the very beginning of the combat, with Auto Spell Casting enabled (0.9.9 4551)

ihhub/fheroes2#4568

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2, the result of an instant combat is different from the result of a combat played in automatic mode from the very beginning of the combat, with Auto Spell Casting enabled.

In fheroes2:

![Instant and Auto combat 001](https://user-images.githubusercontent.com/43583994/140627664-eee7ab0a-5476-4e4e-95b1-0616e2ee9ff8.png)

Auto Spell Casting enabled.
![Instant and Auto combat 002](https://user-images.githubusercontent.com/43583994/140627666-d33db185-57fd-44d6-afe1-4517173f3694.png)

![Instant and Auto combat 003](https://user-images.githubusercontent.com/43583994/140627667-a3923b14-1669-4c6a-9767-8beef3f4bbef.png)

Auto Spell Casting enabled.
![Instant and Auto combat 004](https://user-images.githubusercontent.com/43583994/140627669-03d8fba4-13fd-46c8-bcd7-740e53aa69d0.png)

![Instant and Auto combat 005](https://user-images.githubusercontent.com/43583994/140627671-418b4e28-465a-4e18-8cb9-df7f9712d61b.png)

![Instant and Auto combat 006](https://user-images.githubusercontent.com/43583994/140627675-07c5235d-2ea9-4f22-b9f7-c651e0a932a1.png)

Halon attacks Myrini.

### Save file

Here is the save file:
[Before attack disrupting ray_.zip](https://github.com/ihhub/fheroes2/files/7491344/Before.attack.disrupting.ray_.zip)

### Additional info

Game started with version 0.9.8 4544 and continued with version 0.9.9 4551.
Related closed issue: https://github.com/ihhub/fheroes2/issues/4007.
````

## 20. Null pointer exception when trying to use load latest.

movingblocks/terasology#4092

````text
<!-- Thanks for taking the time to submit a thorough issue report for Terasology! :-)
Please fill out whichever details below seem relevant to your issue.
Note that suggestions, general questions & support should go in the forum:
* http://forum.terasology.org/forum/suggestions.21
* http://forum.terasology.org/forum/support.20/
Bug reports and crashes likely resulting from bugs in the engine go here on GitHub. -->

### What you were trying to do
Use the load latest configuration. 
### What actually happened
Null pointer exception in the Terasology java class
### How to reproduce

* Step 1
Try to use the load latest configuration.
* Step 2
Crash...

### Log details and game version
I think 3.2.0
### Computer details
i7 7700k
GTX 2080ti
16GB Ram
NVMe 128gb SSD

````

## 21. Bug: memory leaks after loading levels

lostartefacts/trx#389

````text
I have a very big custom level. Both me and beta testers have experienced this issue: After loading save files a lot, at one point when trying to load (and sometimes when trying to save) the game gives an error message saying something like "could not allocate enough memory". Game crashes. After restarting the game, it can be saved and loaded as normally, but the problem might occur again after loading many times.

Edit: I'm not 100% sure that requisite for the issue is "loading many times", it could be "saving many times" or just generally playing the level for a long time (which typically includes saving and loading a lot in this level).
````

## 22. Castle screen, Marketpace window, Select Recipients window, it should not be possible to give resources to a player who has been eliminated from the game

ihhub/fheroes2#4622

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2, it should not be possible to give resources to a player who has been eliminated from the game.
Only the colored buttons of players who have not been eliminated should be displayed in the Select Recipients window.

In fheroes2:
![Marketplace gift 001](https://user-images.githubusercontent.com/43583994/141466509-33c5acbd-e347-40c2-bcee-94f7ea7c52be.png)

![Marketplace gift 002](https://user-images.githubusercontent.com/43583994/141466539-ee8f785f-3c99-4a3f-966c-718f420a1bb5.png)

![Marketplace gift 003](https://user-images.githubusercontent.com/43583994/141466564-552e4cc9-2f8f-4177-9e9f-faaaf078789b.png)

### Save file

Not needed.

### Additional info

_No response_
````

## 23. GLA SCUD Launcher cannot fire its missile

theassemblyarmada/thyme#533

````text
GLA SCUD Launcher cannot fire its missile. It spawns shortly, but does not fly anywhere.

![shot_20220131_223133_2](https://user-images.githubusercontent.com/4720891/151877016-19c23c8d-d593-4933-a0f6-d0c82c693643.jpg)

````

## 24. [18GB] Market share of company in receivership does not show as purchased although funds deducted.

tobymao/18xx#11886

````text
https://18xx.games/game/217517

Okay, there's a bug in this game. I bought a share of GSWR from the market and it said that it exited receivership and that I was president. However, it doesn't show me owning the share.

The cash was deducted from my balance but the share isn't there.

This only happened while buying the share from the market.  Buying an IPO share worked normally.
````

## 25. ApcNets do not update without an Apc

space-wizards/space-station-14#3056

````text
They need to have their own system instead of being updated by `PowerApcSystem.cs`.
````

## 26. No indication of current position in computer analysis graph on broadcasts

lichess-org/lila#11617

````text
There is no indication of current position in computer analysis graph on broadcasts, see the image. Seems like an oversight and not intended

Broadcast: https://lichess.org/broadcast/julius-baer-generation-cup--meltwater-champions-chess-tour/final-match-2/yxECPbvy/W9nGHfOQ
Game: https://lichess.org/L6b2oSDR#30

![1 indication](https://user-images.githubusercontent.com/35734373/192259551-a35319b8-fa4c-4f84-bc16-92b29d528e68.png)

````

## 27. Chat is &#x27;hackable&#x27;

re-ss3d/ss3d#762

````text
<!-- The notes within these arrows are for you but can be deleted. -->

## Summary

You can hack the chat by customizing your text (and probably other things).

## Steps to Reproduce

Use `<size=70>Message` or `<color=blue>Message` and you will notice you can customize you text. I haven't tested this across multiple clients but I'm guessing it comes across the server like this too. The user should not be able to customize their chat text like this (later one when we get writing this will be possible in that system though).

![image](https://user-images.githubusercontent.com/41941008/126718225-56e855c2-088e-4913-94e7-6a9390402c3a.png)

*Experienced on version 0.3.95e*
````

## 28. Fix directly starting the microbe stage and editor scene from Godot

revolutionary-games/thrive#2814

````text
they both seem to fail due to SimulationParameters.Instance being null, I wonder why the autoloads don't work properly in this case...
Maybe simulation parameters can only be accessed in _Ready?
````

## 29. Make UI font size responsive

re-ss3d/ss3d#1036

````text
<!-- The notes within these arrows are for you but can be deleted. -->

## Summary

Depending on the size of the game window, some letters tend to disappear or at least vastly change, which make the text "flickers" when resizing and depending on the size, some letters can almost disappear.

## Current Behavior

See how it looks at a given size : 

![image](https://user-images.githubusercontent.com/14344825/221017128-6f0779e2-21a7-43da-b2df-bb77e7c244ed.png)

Now with barely stretching left to right, a few pixels : 

![image](https://user-images.githubusercontent.com/14344825/221017231-37ef8f92-c448-48de-adea-5f3d4dfbcfdf.png)

The letters look much wider on the second picture, it's particularly visible on the I letter.

That should not happen. It looks especially bad when the letters are small, to the point where it's not readable anymore.



````

## 30. The boat wipes out part of the whirlpool when the hero who was in it disembarks

ihhub/fheroes2#9141

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

Found during testing #9140. On the `master` branch:

https://github.com/user-attachments/assets/7330fecc-44aa-4621-9c1c-59a110a4e733

After the hero disembarks from a boat located on one of the tiles of the whirlpool, the `OBJ_BOAT` replaces the `OBJ_WHIRLPOOL` on that tile. On the `master` branch, another hero is still able to teleport to that tile with the `OBJ_BOAT`.  If the hero gets back into the boat and sails away from the whirlpool, the whirlpool object on that tile is not being restored, but another hero still can teleport to it:

https://github.com/user-attachments/assets/5f6d66a2-6b57-4761-b843-78ba96aca4e4

With the fixes from #9140, the situation is a little different - `OBJ_BOAT` still replaces the `OBJ_WHIRLPOOL` upon disembarking, but another hero cannot teleport to that tile anymore (regardless of whether it's occupied with the boat or not):

https://github.com/user-attachments/assets/126e2320-9a2c-4ec6-bcd9-ece111e41564


### Save file

Test map:

[!!TEST1.zip](https://github.com/user-attachments/files/17121630/TEST1.zip)


### Additional info

_No response_
````

## 31. Unintuitive functionality of SPELLCASTER bonus for mass spells

vcmi/vcmi#4577

````text
**Describe the bug**
Normally, a creature with a SPELLCASTER bonus and a spell with a range of 1+, or something like Chain Lightning, can cast it by targetting the friendly/enemy creature, with a welcome option to switch to the normal melee mode in the bottom bar. But with the mass spells, such as Armageddon, Death Ripple and Destroy Undead, the creature can't cast the spell by targeting enemy creature. This is very unintuitive. I've just learn that it's possible to trigger it by pressing "F", but this is obviously not the way to go and nobody will know of this functionality without the prior knowledge.

**To Reproduce**
Steps to reproduce the behavior:
1. Download "Tides of War" mod.
2. Start any scenario with Castle and recruit Templars or Paladins (alternative tier 7 units).
3. Battle a stack of undead creatures and observe the behaviour described above.

**Expected behavior**
Here are possible ways to make it work:
1) Either make the mass spells castable by just targetting a creature.
2) Delegate the casting of the mass offensive spell to the spell/ranged/melee button in the bottom bar. This would work the same way as pressing 'F'. Doing so, in both cases, should open a prompt window though (e.g. "Do you want to cast Destroy Undead?"), to not surprise a newbie player and still make it possible to cycle between ranged/melee (if the creature has those options) - declining of the cast will switch to the next mode.

**Actual behavior**
An average player will never know that you have to press a key to cast a mass spell, and this functionality is not conveyed at all in the description of the bonus - which is the same as any not-mass spell.
![image](https://github.com/user-attachments/assets/83bfac44-8e7b-4e6d-8b0b-dfc0939b3ce9)

**Version**
 - OS: Windows 11, Android
 - VCMI Version: 15.4 and 16.0
````

## 32. Sometimes &quot;no spells left&quot; shows but then you are presented with 1 spell later

jdoleary/spellmasons#767

````text
https://discord.com/channels/1032294536640200766/1242282412352999454/1242945965804093490
````

## 33. Mag boots let you walk in space now.

space-wizards/space-station-14#29029

````text
## Description
When you are walking around in space magboots magically walk around like you were on a grid.

**Reproduction**
- mag boots on
- walk around in space away from station.

**Screenshots**

https://github.com/space-wizards/space-station-14/assets/47093363/caff721e-d88d-4590-bccd-44dcb8cfd8fa

**Additional context**
NA

````

## 34. Castle screen, moat overlaps Captain&#x27;s Quarters in Warlock Castle

ihhub/fheroes2#4538

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

Captain's Quarters before moat being constructed:
![image](https://user-images.githubusercontent.com/55348946/139866858-35a57eac-d5cd-401c-9217-c0678917b948.png)
After:
![image](https://user-images.githubusercontent.com/55348946/139866922-bfb200aa-bbf5-47b7-9083-6c43887d1a61.png)


### Save file

Any Warlock Castle.

### Additional info

_No response_
````

## 35. Loading screen and underwater tunnel of Midas show briefly at level start

lostartefacts/trx#1240

````text

https://github.com/LostArtefacts/TR1X/assets/4934209/5aadff8e-87a2-4566-9edb-7ce7f8d62815

Haven't quite noticed this before. It happens in 30fps too. It seems related to the loading screens. It doesn't happen quite as noticeably in v3.1.1 (where there are no loading screens).

Here is the source clip: 

https://github.com/LostArtefacts/TR1X/assets/4934209/ecf708f5-4def-4821-b66e-6929b0033f39


````

## 36. [1817] Coal Mine ability failed with `undefined method &#x27;ability&#x27;`

tobymao/18xx#2151

````text
* Multiplayer? [https://www.18xx.games/game/13574?action=436](https://www.18xx.games/game/13574?action=436)

**Describe the bug**
Clicking on the coal mine abilities (in the Abilities list above the Undo/Redo/Skip buttons) fails to pop up the ability description or affect the UI in any other way.  The Javascript console has the following error:

```
main.js:2 Uncaught 
a {name: "ability", message: "undefined method `ability' for #<Engine::Step::G1817::SpecialTrack:0xd1ee0>", 
args: Array(1), stack: "ability: undefined method `ability' for #<Engine::…d (https://www.18xx.games/assets/main.js:1:15202)"}
```
````

## 37. Game crashes when music changes track whilst in hyperspace

pioneerspacesim/pioneer#344

````text
Big Red Error:

```
Error: data/modules/MusicPlayer.lua:58: attempt to index local 'near' (a nil value)
stack traceback:
```

IRC log:

```
[01:52] <Brianetta> ah
[01:52] <Brianetta> local near = Game.player.frameBody
[01:52] <Brianetta>     if near:isa("Planet") and Game.player.frameRotating then
[01:52] <Brianetta>         category = "near-planet"
[01:52] <Brianetta>     elseif near:isa("SpaceStation") then
[01:52] <Brianetta>         category = "near-spacestation"
[01:52] <Brianetta>     end
[01:52] <Brianetta> Track change was in hyperspace
[01:53] <robn> thats why
[01:53] <Brianetta> The second pasted line was the one it aborted on
[01:53] <robn> hyperspace frame has no body
[01:53] <robn> good catch
```

````

## 38. Bootstrap should ignore windows scale setting

pokeclicker/pokeclicker#16

````text
UI at scale 125%
![image](https://user-images.githubusercontent.com/9715314/27684623-0ae0b8a0-5ccb-11e7-8ba3-8a28b87af03c.png)

UI at scale 100%
![image](https://user-images.githubusercontent.com/9715314/27684640-1c2f9b3a-5ccb-11e7-9089-e0996837d4ed.png)


This is not the browser zoom, but a windows setting.
At ishadijcks.github.io we did not have this problem, so it is possible.
````

## 39. Surface Duo - keyboard input is laggy

ihhub/fheroes2#8910

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Android

### Describe the bug

On surface duo, keyboard input is slow / laggy.  I have to push 'h' or 't' , 5 or 6 times before a single click is registered.

### Save file

None

### Additional info

I suspect this is a niche issue considering it the application seems fast on my galaxy phone. I've tried multiple keyboards. It's slow with different keyboards.  And the keyboard input is fast in other applications on the surface duo.

Surface Duo is a great way to play the game portably otherwise.
````

## 40. キャラクター選択画面の背景が右上に消えて行っちゃう

kemokemo/kuronan-dash#42

````text
Oh...

![screen_go_away](https://user-images.githubusercontent.com/12206485/75351221-20daf200-58eb-11ea-83c5-216830c10511.gif)

````

## 41. Player global population is incorrectly applied to all patches

revolutionary-games/thrive#1236

````text
I noticed that when the player reproduces in another patch, all of the patches the player species is in, get set to the global total population, this is not intended. Instead the patches should preserve their individual populations.
````

## 42. 1817 - First bid in liquidation display bug

tobymao/18xx#2349

````text
https://18xx.games/game/15349?action=1381
The guy is the first to bid for the liquidation auction. The text box that allows that bid shows 10, and you can raise it up to 20. Even though you cannot bid 20 (it gives you an error), you shouldn't be able _at all_ to select 20, and only 10 should be displayed.
````

## 43. Many OH3 campaigns crash at start

vcmi/vcmi#3203

````text
**Describe the bug**
Some OH3 campaigns crash game at start (New Begginning, Long live the Queen, Armageddon's Blood), some - not (Dragon's Blood, Dungeon and Devils, Elixir of Life)

**To Reproduce**
Steps to reproduce the behavior:
1. Begin some campaigns

**Expected behavior**
Game should be played normallu

**Actual behavior**
Game crashes after selecting campaign

**Did it work earlier?**
Yes, in 1.3.2

**Version**
 - OS: [Windows]
 - Version: [develop -c0e54b3 from 16th November]

````

## 44. Trying to say &quot;...&quot; causes a chat sanitization exception.

space-wizards/space-station-14#10590

````text

````

## 45. Mobs in crit still snore

space-wizards/space-station-14#10393

````text
## Description
Mobs in crit still snore. I strongly believe that sleep should not mislead players about primary reason for mob being horizontal. Also something-something, snoring is related to breathing, breathing is impaired, mob in crit is suffocating.

**Reproduction**
- Get mob to sleep
- Get mob into crit
- Observe peaceful snoring as mob is slowly dying to crit

**Screenshots**
![critted_yet_snoring](https://user-images.githubusercontent.com/108953437/183311300-0838174c-dcf5-47e3-893f-aea191d4866f.png)

**Additional context**
See also issue #10293.
````

## 46. Disappearing wall when buying a new plot of land

corsixth/corsixth#451

````text
_From [mark.l1...@hotmail.co.uk](https://code.google.com/u/117099726060447259318/) on July 09, 2010 15:27:02_

What steps will reproduce the problem? 1.start game
2.build rooms
3.buy another plot of land What is the expected output? What do you see instead? At the moment you can't build across what will become corridors if/when you buy the adjacent plot.   You can build next to these plots if you are not blocking off an area of the hospital. To a certain extent the same could happen in the original, but what I did find odd was building against a plot that I did not own for a wall of a clinic to disappear when I did buy the plot. see screen shot

What version of CorsixTH are you using (e.g. "Beta 2", "SVN r123 ")? r942 What operating system / compile settings are you using? win XP
What level was this on (e.g. "Demo level", "Full game level 12")?
full version - L9 Please provide any additional information below. I think that in the original you could block off areas and when you did you could not place an object in the blocked off space.  You could not block off an area if someone was walking in the area. This was usefull at the start of a game to maximise the area you could build in.  Once you purchased another plot you would have to move or delete the objects doing the blocking before you could add objects to the new space.

**Attachment:** [screen.bmp](http://code.google.com/p/corsix-th/issues/detail?id=384)

_Original issue: http://code.google.com/p/corsix-th/issues/detail?id=384_

````

## 47. Thriveopedia page tree view control has wrong focused colour

revolutionary-games/thrive#5211

````text
When selecting a tree item and it is focused, it has a white outline around it:

![2024-06-12_15 24 14 2135](https://github.com/Revolutionary-Games/Thrive/assets/3796411/38d888a8-4339-4c56-a4ed-164914c7695e)



This should be fixed to match the focused state of other elements (a specific blue colour outline)
````

## 48. [1846 2p] mode creates extra empty token spots.

tobymao/18xx#6262

````text
https://18xx.games/game/54085?action=266

The yellow tile laid in Cleveland should have just 1 spot for a token - if NYC had been removed it would have 2 spots, one filled by an NYC token.

**How to Reproduce the Bug?**

Playing 1846 2 player variant, with NYC not removed from the game
Laid a gentle turn Z city in cleveland (tile #292)
Observe that a second token spot is present - it should not be.
![image](https://user-images.githubusercontent.com/3456680/130646147-d1e7d2e1-5c2c-40fa-8b7a-8e41b6e606fa.png)

````

## 49. Sky background is stretched and rotated incorrectly

colobot/colobot#1584

````text
When watching the cut scene before the first moon mission, or when looking up from the moon, the earth and moon appear as ellipses. I suspect this is related to my screen resolution. The background should be cropped or letterboxed, not stretched.

Also, when rotating my viewpoint, the sky background rotates in a weird way that doesn't match up. This is disconcerting and nauseating.
````

## 50. Arcade cleanup

space-wizards/space-station-14#2133

````text
Arcade Stuff that will have to get fixed
- [x] Ghosts & knocked out people can interact with the spacevillain arcade
- [x] ~~multiple people can use the spacevillain arcade at once~~ meh, just keep it this way
- [x] ~~spacevillain arcade is not using componentstates to update client on its gamestate (cause noone told me thats how i should do it)~~ just rework the networking a bit
- [x] ~~blockgamearcade is not using componentstates to update client on its gamestate (cause noone told me thats how i should do it)~~ no
- [x] add a randomarcadecomponent that adds either blockgamearcade or spacevillainarcade on mapinit
- [x] ~~preferably add some matching sprites~~
- [x] softdrop-speed should modify speed, not override it

- [x] have fieldtick & presstick have internal while loops to prevent accumulatedframetime going to infinity when checktime is smaller than frametime:
```
accFrameTime += frameTime;
while(accFrameTime > checkTime){
      Logic...
      accFrameTime -= checkTime;
}
```
- [x] fix tetris random piece generator (see "Random Generator" https://tetris.wiki/Tetris_Guideline)
- [x] implement missing things from here https://tetris.wiki/Tetris_Guideline
- [x] new keybinds are somehow blocking the old textmoveright/left ones (#2143), for suspected cause see review in #2131
- [x] blockgamearcade checks if the arcade can interact. it should check if the user can interact (also should probably use interacthand)
- [x] disable spacevillainarcade buttons if power is out (check if this might be an issue with tetris too?)
- [x] disable spacevillainarcade buttons if gameover
- [x] indicators for spacevillainarcade hacking

you're free to tackle any one of these since i'll be working on other stuff first
````
