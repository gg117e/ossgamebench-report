# 本人による確認シート：上位 30 プロジェクト（2026-11-15）

分析対象 10,082 件のうち、この 30 プロジェクトで **86%** を占める。LLM の分類が正しいかを確認し、「確認」の列に ○ か、正しい分類を書く。
プロジェクトの GitHub のページ（https://github.com/<プロジェクト名>）を見て判断してよい。

- **ゲーム本体か**：ゲームそのもの（移植・再実装を含む）なら game。汎用のエンジンやツールなら engine_tool。
- **種類**：discrete = 手番・選択で進む。continuous = リアルタイムで進む。mixed = 両方が中心。
- **Web**：ブラウザやチャットのボットで遊ぶなら True。

| # | プロジェクト | 修正 | テストあり | ゲーム本体か | 種類 | Web | LLM の根拠 | 確認 |
|---:|---|---:|---:|---|---|---|---|---|
| 1 | tobymao/18xx | 1375 | 149 | game | discrete | True | board game website (18xx) | |
| 2 | ihhub/fheroes2 | 1262 | 0 | game | discrete | False | turn-based strategy (HoMM II) | |
| 3 | space-wizards/space-station-14 | 964 | 46 | game | continuous | False | real-time multiplayer SS13 remake | |
| 4 | vcmi/vcmi | 772 | 63 | game | discrete | False | HoMM III engine, turn-based strategy | |
| 5 | openra/openra | 680 | 9 | game | continuous | False | real-time strategy engine | |
| 6 | revolutionary-games/thrive | 421 | 10 | game | continuous | False | real-time evolution simulation | |
| 7 | lichess-org/lila | 409 | 11 | game | discrete | True | online chess server | |
| 8 | quaver/quaver | 242 | 5 | game | continuous | False | rhythm game | |
| 9 | corsixth/corsixth | 230 | 5 | game | continuous | False | real-time business sim (Theme Hospital) | |
| 10 | endless-sky/endless-sky | 218 | 6 | game | continuous | False | real-time space exploration/combat | |
| 11 | freeorion/freeorion | 216 | 4 | game | discrete | False | turn-based 4X | |
| 12 | ja2-stracciatella/ja2-stracciatella | 209 | 3 | game | mixed | False | real-time exploration, turn-based tactical combat | |
| 13 | magefree/mage | 202 | 110 | game | discrete | False | Magic card game engine | |
| 14 | pokeclicker/pokeclicker | 172 | 1 | game | discrete | True | idle clicker in browser | |
| 15 | lostartefacts/trx | 126 | 0 | game | continuous | False | Tomb Raider action-adventure | |
| 16 | re-ss3d/ss3d | 114 | 1 | game | continuous | False | real-time 3D SS13 | |
| 17 | gemrb/gemrb | 109 | 5 | game | continuous | False | Infinity Engine, real-time with pause | |
| 18 | triplea-game/triplea | 107 | 22 | game | discrete | False | turn-based strategy/board engine | |
| 19 | jdoleary/spellmasons | 93 | 6 | game | discrete | False | turn-based tactical roguelike | |
| 20 | cuttle-cards/cuttle | 92 | 31 | game | discrete | True | pvp card game web app | |
| 21 | rmc-14/rmc-14 | 92 | 1 | game | continuous | False | real-time SS14-based game | |
| 22 | teeworlds/teeworlds | 87 | 1 | game | continuous | False | multiplayer shooter | |
| 23 | crownicles/crownicles | 74 | 2 | game | discrete | True | text adventure Discord bot | |
| 24 | colobot/colobot | 73 | 7 | game | continuous | False | real-time programming strategy | |
| 25 | aottg-2/aottg-2 | 70 | 1 | game | continuous | False | real-time action (AoTTG) | |
| 26 | sfttech/openage | 69 | 10 | game | continuous | False | RTS engine (Age of Empires) | |
| 27 | movingblocks/terasology | 62 | 12 | game | continuous | False | voxel sandbox | |
| 28 | ekolis/freee | 61 | 3 | game | discrete | False | turn-based 4X (Space Empires IV) | |
| 29 | eternagame/eternajs | 54 | 7 | game | discrete | True | RNA design puzzle in browser | |
| 30 | anthonytornetta/cosmos | 54 | 6 | game | continuous | False | real-time block space game | |
