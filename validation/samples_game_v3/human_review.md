# 独立判定用50件（LLMの回答は含まない）

判定手引き `validation/codebook.md` を読み、各報告のタイトルと収録本文だけで判断する。
`human_answers.json` の is_actual_bug、primary_category、issue_domain、confidence、rationale を記入する。
development_labels.jsonl は回答が終わるまで開かない。画像・動画の中身や現在のGitHub本文では補完しない。
判断できないときは unknown とし、理由を残す。画像等の5項目は今回は記入不要。

## 1. Adventure map, wrong passability for large objects, trees, mountains, etc. with the Dimension Door spell

ihhub/fheroes2#4278

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2, there is wrong passability for large objects, trees, mountains, etc. with the Dimension Door spell.

In fheroes2:

![Wrong passability DD 001](https://user-images.githubusercontent.com/43583994/135071247-4597b4b8-b955-442b-8a05-9adfd7218cb4.png)
![Wrong passability DD 008](https://user-images.githubusercontent.com/43583994/135071405-8d99d483-4e58-4b2c-9af2-541d0c6f38d8.png)

![Wrong passability DD 002](https://user-images.githubusercontent.com/43583994/135071264-f09f8728-60cf-4f96-8941-538aa21a70dc.png)
![Wrong passability DD 009](https://user-images.githubusercontent.com/43583994/135071423-94fd8866-4e32-45c8-91c0-0c1e0a6f837e.png)

![Wrong passability DD 003](https://user-images.githubusercontent.com/43583994/135071281-c6b75585-7f70-4bb1-a288-b2c9601c3fa8.png)
![Wrong passability DD 010](https://user-images.githubusercontent.com/43583994/135071443-93c91ad3-ead8-4af5-8b5b-6c85a39739eb.png)

![Wrong passability DD 004](https://user-images.githubusercontent.com/43583994/135071290-492a1bb2-ae62-4f38-aec2-43c0d971c58a.png)
![Wrong passability DD 011](https://user-images.githubusercontent.com/43583994/135071474-26ea96a5-2703-47ac-ae1a-ac4d834370f9.png)

![Wrong passability DD 005](https://user-images.githubusercontent.com/43583994/135071303-4a238926-7a29-49e8-a75f-9afd6f32fb58.png)
![Wrong passability DD 012](https://user-images.githubusercontent.com/43583994/135071494-eb52a0df-9d61-47dc-b8fc-aeb6fd2eb9f9.png)

![Wrong passability DD 006](https://user-images.githubusercontent.com/43583994/135071315-66f91e8e-f9f1-4884-8934-3436f93b91e6.png)
![Wrong passability DD 013](https://user-images.githubusercontent.com/43583994/135071525-b6169b49-0bbd-4745-af84-03fb3cedd1f8.png)

![Wrong passability DD 007](https://user-images.githubusercontent.com/43583994/135071321-9fc38c30-9d70-4f2e-b353-d1ab9a24e034.png)
![Wrong passability DD 014](https://user-images.githubusercontent.com/43583994/135071550-7c1a6430-d25b-4228-83e1-bef6009b16b4.png)

![Wrong passability DD 015](https://user-images.githubusercontent.com/43583994/135071643-0e5d005c-d34f-47a9-b9f4-a072199e12a4.png)
![Wrong passability DD 016](https://user-images.githubusercontent.com/43583994/135071650-42ab4905-2e38-43df-9764-6039b3619bff.png)

![Wrong passability DD 017](https://user-images.githubusercontent.com/43583994/135071669-2e779a1b-4865-4f26-917e-47c6aceb60d4.png)
![Wrong passability DD 018](https://user-images.githubusercontent.com/43583994/135071674-75cd1d78-479f-4dd6-a8e1-b335330a9ff0.png)
![Wrong passability DD 019](https://user-images.githubusercontent.com/43583994/135071683-38b2de87-f83c-4746-933f-4c4078eba2e7.png)
![Wrong passability DD 020](https://user-images.githubusercontent.com/43583994/135071692-d3c04986-9c32-4a25-9aea-a525d2c96229.png)

### Save file

Here are the save files:
[Wrong passibility Dimension Door 01.zip](https://github.com/ihhub/fheroes2/files/7243176/Wrong.passibility.Dimension.Door.01.zip)

### Additional info

Version 0.9.7 4208
````

## 2. Pick 3 gold in hota map &#x27;the devil is in the detail&#x27;

vcmi/vcmi#4146

````text
**Describe the bug**
in hota map the devil is in the detail, this resouce seems to be a random resouce with 3 unit. When random result is gold, hero only pick 3 gold.
 ![1](https://github.com/vcmi/vcmi/assets/8289682/cbad6e95-9b4c-4c95-a7ee-c30a1693b390)

**Expected behavior**
pick 300 gold as hota does.

**Actual behavior**
pick 3 gold

**Did it work earlier?**
1.5.2 

**Version**
 - OS: All
 - Version: 1.5.2

**Additional context**
no

````

## 3. [1828.games] Merging.. Not Receiving money for selling

tobymao/18xx#3343

````text
Game ID:23137

Raymong should have received $115 from the bank when the OS&H was created but never received his money for the sale from the bank. When having the option to exchange or sell his share in my OS&H company, he opted to sell it. But he never got his $115 from the bank even though the log said so.


Code stuff...

{
  "id": 23137,
  "description": "open.liveForFourishHoursToAsyncMaybe?",
  "user": {
    "id": 2843,
    "name": "joeD"
  },
  "players": [
    {
      "id": 4267,
      "name": "Raymong"
    },
    {
      "id": 2843,
      "name": "joeD"
    },
    {
      "id": 5518,
      "name": "Aavar"
    }
  ],
  "max_players": 5,
  "title": "1828.Games",
  "settings": {
    "seed": 93068046,
    "unlisted": false,
    "optional_rules": []
  },
  "user_settings": null,
  "status": "active",
  "turn": 5,
  "round": "Stock Round",
  "acting": [
    4267
  ],
  "result": {},
  "actions": [
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 1,
      "created_at": 1610809623,
      "message": "it's a pretty big game for three people but I just kinda wanna play\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 2,
      "created_at": 1610809673,
      "message": "hf gl.. how familiar are we with the rules? I got a little bit with one solo play\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 3,
      "created_at": 1610809696,
      "message": "I read the rules...still need to figure out the merger details\n"
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 4,
      "created_at": 1610809714,
      "company": "M&H",
      "price": 125
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 5,
      "created_at": 1610809717,
      "message": "ah, yeah\n"
    },
    {
      "type": "bid",
      "entity": 2843,
      "entity_type": "player",
      "id": 6,
      "created_at": 1610809724,
      "company": "C&A",
      "price": 165
    },
    {
      "type": "bid",
      "entity": 5518,
      "entity_type": "player",
      "id": 7,
      "created_at": 1610809742,
      "company": "StCT",
      "price": 25
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 8,
      "created_at": 1610809783,
      "company": "C&P",
      "price": 85
    },
    {
      "type": "bid",
      "entity": 2843,
      "entity_type": "player",
      "id": 9,
      "created_at": 1610809855,
      "company": "D&H",
      "price": 85
    },
    {
      "type": "bid",
      "entity": 5518,
      "entity_type": "player",
      "id": 10,
      "created_at": 1610809865,
      "company": "M&H",
      "price": 130
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 11,
      "created_at": 1610809935,
      "company": "E&K",
      "price": 125
    },
    {
      "type": "bid",
      "entity": 2843,
      "entity_type": "player",
      "id": 12,
      "created_at": 1610809981,
      "company": "C&P",
      "price": 90
    },
    {
      "type": "bid",
      "entity": 5518,
      "entity_type": "player",
      "id": 13,
      "created_at": 1610809990,
      "company": "C&StL",
      "price": 45
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 14,
      "created_at": 1610810031,
      "company": "SVN",
      "price": 20
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 15,
      "created_at": 1610810035,
      "company": "C&P",
      "price": 95
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 16,
      "created_at": 1610810068
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 17,
      "created_at": 1610810091
    },
    {
      "type": "bid",
      "entity": 2843,
      "entity_type": "player",
      "id": 18,
      "created_at": 1610810096,
      "company": "NW",
      "price": 255
    },
    {
      "type": "bid",
      "entity": 5518,
      "entity_type": "player",
      "id": 19,
      "created_at": 1610810195,
      "company": "NKP",
      "price": 255
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 20,
      "created_at": 1610810316,
      "company": "GT",
      "price": 255
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 21,
      "created_at": 1610810347
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 22,
      "created_at": 1610810355
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 23,
      "created_at": 1610810376
    },
    {
      "type": "par",
      "entity": 4267,
      "entity_type": "player",
      "id": 24,
      "created_at": 1610810391,
      "corporation": "GT",
      "share_price": "79,9,5"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 25,
      "created_at": 1610810408,
      "message": "I know it says one, but you will actually have 3 shares at the beginning of the SR\n"
    },
    {
      "type": "par",
      "entity": 5518,
      "entity_type": "player",
      "id": 26,
      "created_at": 1610810408,
      "corporation": "NKP",
      "share_price": "79,9,5"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 27,
      "created_at": 1610810439
    },
    {
      "type": "par",
      "entity": 2843,
      "entity_type": "player",
      "id": 28,
      "created_at": 1610810463,
      "corporation": "NW",
      "share_price": "71,11,6"
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 29,
      "created_at": 1610810478
    },
    {
      "id": 30,
      "type": "bid",
      "price": 250,
      "entity": 4267,
      "company": "MC",
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610810538
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 31,
      "created_at": 1610810570,
      "message": "this is probably a terrible idea buying two of these...\n"
    },
    {
      "id": 32,
      "type": "undo",
      "entity": 4267,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610810579
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 33,
      "created_at": 1610810583,
      "message": "that's the idea though\n"
    },
    {
      "type": "bid",
      "entity": 4267,
      "entity_type": "player",
      "id": 34,
      "created_at": 1610810590,
      "company": "MC",
      "price": 250
    },
    {
      "type": "par",
      "entity": 4267,
      "entity_type": "player",
      "id": 35,
      "created_at": 1610810593,
      "corporation": "MC",
      "share_price": "67,13,7"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 36,
      "created_at": 1610810615,
      "message": "someone gets stuck with 2 BO type companies. There were some randomly removed, its always the number of players plus one\n"
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 37,
      "created_at": 1610810621,
      "shares": [
        "NW_2"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 38,
      "created_at": 1610810640,
      "shares": [
        "NKP_2"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 39,
      "created_at": 1610810727,
      "shares": [
        "MC_2"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 40,
      "created_at": 1610810733,
      "shares": [
        "NW_3"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 41,
      "created_at": 1610810738,
      "shares": [
        "NKP_3"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 42,
      "created_at": 1610810753,
      "shares": [
        "MC_3"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 43,
      "created_at": 1610810764,
      "shares": [
        "NW_4"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 44,
      "created_at": 1610810771,
      "shares": [
        "NKP_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 45,
      "created_at": 1610810784
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 46,
      "created_at": 1610810794,
      "message": "too bad none of the other companies floated at 67\n"
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 47,
      "created_at": 1610810820,
      "shares": [
        "MC_4"
      ],
      "percent": 10
    },
    {
      "id": 48,
      "type": "buy_shares",
      "entity": 5518,
      "shares": [
        "GT_2"
      ],
      "percent": 10,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610810908
    },
    {
      "id": 49,
      "type": "undo",
      "entity": 4267,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610810930
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 50,
      "created_at": 1610810935,
      "shares": [
        "NW_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 51,
      "created_at": 1610810956
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 52,
      "created_at": 1610810961,
      "shares": [
        "MC_5"
      ],
      "percent": 10
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 53,
      "created_at": 1610810977,
      "message": "so can you dump the MC on me and float the GT?\n"
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 54,
      "created_at": 1610810989,
      "shares": [
        "MC_6"
      ],
      "percent": 10
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 55,
      "created_at": 1610811004,
      "message": "Is that what you want?\n"
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 56,
      "created_at": 1610811010
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 57,
      "created_at": 1610811011,
      "message": "lets do it\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 58,
      "created_at": 1610811017,
      "message": "or not, okay\n"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 59,
      "created_at": 1610811020
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 60,
      "created_at": 1610811026
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 61,
      "created_at": 1610811031,
      "message": "I would rather run a company during the OR\n"
    },
    {
      "type": "lay_tile",
      "entity": "C&P",
      "entity_type": "minor",
      "id": 62,
      "created_at": 1610811049,
      "hex": "C17",
      "tile": "9-0",
      "rotation": 1
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 63,
      "created_at": 1610811053,
      "message": "but if you dumped the MC on me, you could the float the GT and run the GT instead\n"
    },
    {
      "type": "run_routes",
      "entity": "C&P",
      "entity_type": "minor",
      "id": 64,
      "created_at": 1610811060,
      "routes": [
        {
          "train": "2-1",
          "connections": [
            [
              "C15",
              "C17",
              "C19"
            ]
          ],
          "hexes": [
            "C19",
            "C15"
          ],
          "revenue": 30,
          "revenue_str": "C19-C15"
        }
      ]
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 65,
      "created_at": 1610811080,
      "hex": "G9",
      "tile": "9-1",
      "rotation": 0
    },
    {
      "type": "buy_train",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 66,
      "created_at": 1610811085,
      "train": "2-0",
      "price": 80,
      "variant": "2"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 67,
      "created_at": 1610811089
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 68,
      "created_at": 1610811125,
      "hex": "J18",
      "tile": "57-0",
      "rotation": 2
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 69,
      "created_at": 1610811136
    },
    {
      "type": "buy_train",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 70,
      "created_at": 1610811140,
      "train": "2-2",
      "price": 80,
      "variant": "2"
    },
    {
      "type": "buy_train",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 71,
      "created_at": 1610811141,
      "train": "2-3",
      "price": 80,
      "variant": "2"
    },
    {
      "type": "buy_train",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 72,
      "created_at": 1610811157,
      "train": "2-4",
      "price": 80,
      "variant": "2"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 73,
      "created_at": 1610811160
    },
    {
      "type": "lay_tile",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 74,
      "created_at": 1610811176,
      "hex": "B8",
      "tile": "8-0",
      "rotation": 0
    },
    {
      "type": "buy_train",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 75,
      "created_at": 1610811181,
      "train": "2-5",
      "price": 80,
      "variant": "2"
    },
    {
      "id": 76,
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610811222
    },
    {
      "id": 77,
      "type": "undo",
      "entity": 4267,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610811225
    },
    {
      "type": "buy_train",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 78,
      "created_at": 1610811238,
      "train": "2-6",
      "price": 80,
      "variant": "2"
    },
    {
      "type": "buy_train",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 79,
      "created_at": 1610811239,
      "train": "3-0",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "buy_company",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 80,
      "created_at": 1610811250,
      "company": "SVN",
      "price": 40
    },
    {
      "type": "buy_company",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 81,
      "created_at": 1610811274,
      "company": "E&K",
      "price": 230
    },
    {
      "type": "lay_tile",
      "entity": "E&K",
      "entity_type": "company",
      "id": 82,
      "created_at": 1610811302,
      "hex": "E7",
      "tile": "69-0",
      "rotation": 0
    },
    {
      "id": 83,
      "type": "buy_shares",
      "entity": 4267,
      "shares": [
        "GT_2"
      ],
      "percent": 10,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610811321
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 84,
      "created_at": 1610811357,
      "message": "now its a tough choice\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 85,
      "created_at": 1610811381,
      "message": "lol\n"
    },
    {
      "id": 86,
      "type": "sell_shares",
      "entity": 4267,
      "shares": [
        "MC_1",
        "MC_2",
        "MC_3",
        "MC_0"
      ],
      "percent": 50,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610811388
    },
    {
      "id": 87,
      "type": "undo",
      "entity": 4267,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610811397
    },
    {
      "id": 88,
      "type": "undo",
      "entity": 4267,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610811398
    },
    {
      "type": "sell_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 89,
      "created_at": 1610811402,
      "shares": [
        "MC_1",
        "MC_2",
        "MC_3",
        "MC_0"
      ],
      "percent": 50
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 90,
      "created_at": 1610811405,
      "message": "I'm all for pushing the boundaries in this game to fine bugs and stuff\n"
    },
    {
      "type": "par",
      "entity": 4267,
      "entity_type": "player",
      "id": 91,
      "created_at": 1610811456,
      "corporation": "B&O",
      "share_price": "79,9,5"
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 92,
      "created_at": 1610811464
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 93,
      "created_at": 1610811567,
      "shares": [
        "MC_1"
      ],
      "percent": 10
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 94,
      "created_at": 1610811580,
      "shares": [
        "MC_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 95,
      "created_at": 1610811583
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 96,
      "created_at": 1610811623
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 97,
      "created_at": 1610811652,
      "message": "crap- I did bad math- can I re-par BO?\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 98,
      "created_at": 1610811665,
      "message": "yes\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 99,
      "created_at": 1610811672,
      "message": "nvm\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 100,
      "created_at": 1610811679,
      "message": "ok\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 101,
      "created_at": 1610811684,
      "message": "I did it right the first time- just tricked myself\n"
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 102,
      "created_at": 1610811692,
      "shares": [
        "B&O_1"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 103,
      "created_at": 1610811700
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 104,
      "created_at": 1610811705
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 105,
      "created_at": 1610811717,
      "shares": [
        "B&O_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 106,
      "created_at": 1610811722
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 107,
      "created_at": 1610811779,
      "shares": [
        "GT_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 108,
      "created_at": 1610811782
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 109,
      "created_at": 1610811802
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 110,
      "created_at": 1610811805
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 111,
      "created_at": 1610811809,
      "shares": [
        "GT_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 112,
      "created_at": 1610811810
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 113,
      "created_at": 1610811814
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 114,
      "created_at": 1610811820
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 115,
      "created_at": 1610811835,
      "message": "can I go MM and pass for both of you? Im floating my companies and buying a NW\n"
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 116,
      "created_at": 1610811842,
      "shares": [
        "GT_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 117,
      "created_at": 1610811845
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 118,
      "created_at": 1610811848
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 119,
      "created_at": 1610811851
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 120,
      "created_at": 1610811858,
      "shares": [
        "NW_6"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 121,
      "created_at": 1610811860
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 122,
      "created_at": 1610811863
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 123,
      "created_at": 1610811868
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 124,
      "created_at": 1610811871,
      "shares": [
        "B&O_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 125,
      "created_at": 1610811873
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 126,
      "created_at": 1610811876
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 127,
      "created_at": 1610811879
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 128,
      "created_at": 1610811887,
      "shares": [
        "B&O_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 129,
      "created_at": 1610811890
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 130,
      "created_at": 1610811892
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 131,
      "created_at": 1610811894
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 132,
      "created_at": 1610811903
    },
    {
      "type": "lay_tile",
      "entity": "C&P",
      "entity_type": "minor",
      "id": 133,
      "created_at": 1610811927,
      "hex": "B20",
      "tile": "57-1",
      "rotation": 0
    },
    {
      "type": "run_routes",
      "entity": "C&P",
      "entity_type": "minor",
      "id": 134,
      "created_at": 1610811939,
      "routes": [
        {
          "train": "2-1",
          "connections": [
            [
              "B20",
              "C19"
            ]
          ],
          "hexes": [
            "C19",
            "B20"
          ],
          "revenue": 30,
          "revenue_str": "C19-B20"
        }
      ]
    },
    {
      "type": "lay_tile",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 135,
      "created_at": 1610811959,
      "hex": "D6",
      "tile": "57-2",
      "rotation": 2
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 136,
      "created_at": 1610811966
    },
    {
      "type": "buy_train",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 137,
      "created_at": 1610811971,
      "train": "3-1",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "buy_train",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 138,
      "created_at": 1610812020,
      "train": "3-2",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 139,
      "created_at": 1610812022
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 140,
      "created_at": 1610812030
    },
    {
      "type": "lay_tile",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 141,
      "created_at": 1610812038,
      "hex": "I21",
      "tile": "8-1",
      "rotation": 1
    },
    {
      "type": "buy_train",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 142,
      "created_at": 1610812044,
      "train": "3-3",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "buy_train",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 143,
      "created_at": 1610812058,
      "train": "3-4",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 144,
      "created_at": 1610812059
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 145,
      "created_at": 1610812063
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 146,
      "created_at": 1610812070,
      "hex": "H8",
      "tile": "57-3",
      "rotation": 0
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 147,
      "created_at": 1610812072
    },
    {
      "type": "run_routes",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 148,
      "created_at": 1610812077,
      "routes": [
        {
          "train": "2-0",
          "connections": [
            [
              "F10",
              "G9",
              "H8"
            ]
          ],
          "hexes": [
            "H8",
            "F10"
          ],
          "revenue": 50,
          "revenue_str": "H8-F10"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 149,
      "created_at": 1610812079,
      "kind": "payout"
    },
    {
      "type": "buy_train",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 150,
      "created_at": 1610812081,
      "train": "3-5",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 151,
      "created_at": 1610812083
    },
    {
      "type": "buy_company",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 152,
      "created_at": 1610812092,
      "company": "StCT",
      "price": 40
    },
    {
      "type": "buy_company",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 153,
      "created_at": 1610812100,
      "company": "C&StL",
      "price": 80
    },
    {
      "type": "pass",
      "entity": "C&StL",
      "entity_type": "company",
      "id": 154,
      "created_at": 1610812108
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 155,
      "created_at": 1610812112
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 156,
      "created_at": 1610812126,
      "hex": "J18",
      "tile": "205-0",
      "rotation": 2
    },
    {
      "type": "place_token",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 157,
      "created_at": 1610812127,
      "city": "205-0-0",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 158,
      "created_at": 1610812150,
      "routes": [
        {
          "train": "2-2",
          "connections": [
            [
              "J18",
              "I19"
            ]
          ],
          "hexes": [
            "I19",
            "J18"
          ],
          "revenue": 60,
          "revenue_str": "I19-J18"
        },
        {
          "train": "2-3",
          "connections": [
            [
              "J18",
              "K19"
            ]
          ],
          "hexes": [
            "K19",
            "J18"
          ],
          "revenue": 60,
          "revenue_str": "K19-J18"
        },
        {
          "train": "2-4",
          "connections": [
            [
              "K19",
              "L18"
            ]
          ],
          "hexes": [
            "L18",
            "K19"
          ],
          "revenue": 40,
          "revenue_str": "L18-K19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 159,
      "created_at": 1610812153,
      "kind": "payout"
    },
    {
      "type": "buy_train",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 160,
      "created_at": 1610812165,
      "train": "3-6",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 161,
      "created_at": 1610812193
    },
    {
      "type": "lay_tile",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 162,
      "created_at": 1610812206,
      "hex": "C7",
      "tile": "8-2",
      "rotation": 3
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 163,
      "created_at": 1610812230
    },
    {
      "type": "run_routes",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 164,
      "created_at": 1610812243,
      "routes": [
        {
          "train": "3-0",
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "revenue": 110,
          "revenue_str": "A3-A5-A7"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 165,
      "created_at": 1610812258,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 166,
      "created_at": 1610812275
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 167,
      "created_at": 1610812284
    },
    {
      "type": "lay_tile",
      "entity": "C&P",
      "entity_type": "minor",
      "id": 168,
      "created_at": 1610812351,
      "hex": "C13",
      "tile": "8-3",
      "rotation": 4
    },
    {
      "type": "run_routes",
      "entity": "C&P",
      "entity_type": "minor",
      "id": 169,
      "created_at": 1610812367,
      "routes": [
        {
          "train": "2-1",
          "connections": [
            [
              "C19",
              "C17",
              "C15"
            ]
          ],
          "hexes": [
            "C15",
            "C19"
          ],
          "revenue": 30,
          "revenue_str": "C15-C19"
        }
      ]
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 170,
      "created_at": 1610812376,
      "hex": "F8",
      "tile": "57-4",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 171,
      "created_at": 1610812379
    },
    {
      "type": "run_routes",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 172,
      "created_at": 1610812385,
      "routes": [
        {
          "train": "2-0",
          "connections": [
            [
              "F10",
              "G9",
              "H8"
            ]
          ],
          "hexes": [
            "F10",
            "H8"
          ],
          "revenue": 50,
          "revenue_str": "F10-H8"
        },
        {
          "train": "3-5",
          "connections": [
            [
              "F8",
              "F10"
            ]
          ],
          "hexes": [
            "F10",
            "F8"
          ],
          "revenue": 50,
          "revenue_str": "F10-F8"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 173,
      "created_at": 1610812386,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 174,
      "created_at": 1610812389
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 175,
      "created_at": 1610812394
    },
    {
      "type": "lay_tile",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 176,
      "created_at": 1610812450,
      "hex": "E9",
      "tile": "59-0",
      "rotation": 1
    },
    {
      "id": 177,
      "city": "57-2-0",
      "slot": 0,
      "type": "place_token",
      "entity": "GT",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812475
    },
    {
      "id": 178,
      "type": "undo",
      "entity": "GT",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812487
    },
    {
      "type": "place_token",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 179,
      "created_at": 1610812490,
      "city": "59-0-0",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 180,
      "created_at": 1610812509,
      "routes": [
        {
          "train": "3-1",
          "connections": [
            [
              "E7",
              "D6"
            ],
            [
              "E9",
              "E7"
            ]
          ],
          "hexes": [
            "D6",
            "E7",
            "E9"
          ],
          "revenue": 70,
          "revenue_str": "D6-E7-E9"
        },
        {
          "train": "3-2",
          "connections": [
            [
              "C5",
              "D6"
            ],
            [
              "D4",
              "C5"
            ]
          ],
          "hexes": [
            "D6",
            "C5",
            "D4"
          ],
          "revenue": 60,
          "revenue_str": "D6-C5-D4"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 181,
      "created_at": 1610812510,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 182,
      "created_at": 1610812513
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 183,
      "created_at": 1610812515
    },
    {
      "type": "lay_tile",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 184,
      "created_at": 1610812536,
      "hex": "I19",
      "tile": "53-0",
      "rotation": 0
    },
    {
      "id": 185,
      "type": "run_routes",
      "entity": "B&O",
      "routes": [
        {
          "hexes": [
            "J18",
            "I19"
          ],
          "train": "3-3",
          "revenue": 80,
          "connections": [
            [
              "I19",
              "J18"
            ]
          ],
          "revenue_str": "J18-I19"
        }
      ],
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812562
    },
    {
      "id": 186,
      "kind": "payout",
      "type": "dividend",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812565
    },
    {
      "id": 187,
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812568
    },
    {
      "id": 188,
      "type": "buy_company",
      "price": 160,
      "entity": "B&O",
      "company": "C&P",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812575
    },
    {
      "id": 189,
      "city": "C15-0-0",
      "slot": 0,
      "type": "place_token",
      "entity": "C&P",
      "entity_type": "company",
      "user": 4267,
      "created_at": 1610812592
    },
    {
      "id": 190,
      "type": "undo",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812622
    },
    {
      "id": 191,
      "type": "undo",
      "entity": "C&P",
      "entity_type": "company",
      "user": 4267,
      "created_at": 1610812627
    },
    {
      "id": 192,
      "type": "undo",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812628
    },
    {
      "id": 193,
      "type": "undo",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812631
    },
    {
      "id": 194,
      "type": "undo",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610812633
    },
    {
      "type": "buy_company",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 195,
      "created_at": 1610812649,
      "company": "C&P",
      "price": 160
    },
    {
      "type": "place_token",
      "entity": "C&P",
      "entity_type": "company",
      "id": 196,
      "created_at": 1610812653,
      "city": "C15-0-0",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 197,
      "created_at": 1610812681,
      "routes": [
        {
          "train": "3-3",
          "connections": [
            [
              "C19",
              "B20"
            ],
            [
              "C15",
              "C17",
              "C19"
            ]
          ],
          "hexes": [
            "B20",
            "C19",
            "C15"
          ],
          "revenue": 50,
          "revenue_str": "B20-C19-C15"
        },
        {
          "train": "3-4",
          "connections": [
            [
              "I19",
              "J18"
            ]
          ],
          "hexes": [
            "J18",
            "I19"
          ],
          "revenue": 80,
          "revenue_str": "J18-I19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 198,
      "created_at": 1610812682,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 199,
      "created_at": 1610812683
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 200,
      "created_at": 1610812684
    },
    {
      "id": 201,
      "hex": "K17",
      "tile": "7-0",
      "type": "lay_tile",
      "entity": "NW",
      "rotation": 5,
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610812711
    },
    {
      "id": 202,
      "type": "undo",
      "entity": "NW",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610812743
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 203,
      "created_at": 1610812753,
      "hex": "K17",
      "tile": "8-4",
      "rotation": 4
    },
    {
      "type": "run_routes",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 204,
      "created_at": 1610812767,
      "routes": [
        {
          "train": "2-2",
          "connections": [
            [
              "J18",
              "I19"
            ]
          ],
          "hexes": [
            "J18",
            "I19"
          ],
          "revenue": 80,
          "revenue_str": "J18-I19"
        },
        {
          "train": "2-3",
          "connections": [
            [
              "J18",
              "K19"
            ]
          ],
          "hexes": [
            "J18",
            "K19"
          ],
          "revenue": 60,
          "revenue_str": "J18-K19"
        },
        {
          "train": "2-4",
          "connections": [
            [
              "K19",
              "L18"
            ]
          ],
          "hexes": [
            "K19",
            "L18"
          ],
          "revenue": 40,
          "revenue_str": "K19-L18"
        },
        {
          "train": "3-6",
          "connections": [
            [
              "K19",
              "K17",
              "L16"
            ]
          ],
          "hexes": [
            "L16",
            "K19"
          ],
          "revenue": 60,
          "revenue_str": "L16-K19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 205,
      "created_at": 1610812777,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 206,
      "created_at": 1610812791
    },
    {
      "type": "lay_tile",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 207,
      "created_at": 1610812798,
      "hex": "D8",
      "tile": "57-5",
      "rotation": 2
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 208,
      "created_at": 1610812800
    },
    {
      "type": "run_routes",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 209,
      "created_at": 1610812819,
      "routes": [
        {
          "train": "3-0",
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "revenue": 110,
          "revenue_str": "A3-A5-A7"
        },
        {
          "train": "2-6",
          "connections": [
            [
              "A7",
              "B8",
              "C7",
              "D8"
            ]
          ],
          "hexes": [
            "D8",
            "A7"
          ],
          "revenue": 50,
          "revenue_str": "D8-A7"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 210,
      "created_at": 1610812827,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 211,
      "created_at": 1610812835
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 212,
      "created_at": 1610812857
    },
    {
      "type": "par",
      "entity": 2843,
      "entity_type": "player",
      "id": 213,
      "created_at": 1610812981,
      "corporation": "PRR",
      "share_price": "86,7,4"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 214,
      "created_at": 1610812997
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 215,
      "created_at": 1610813059,
      "shares": [
        "NW_7"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 216,
      "created_at": 1610813061
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 217,
      "created_at": 1610813102,
      "shares": [
        "MC_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 218,
      "created_at": 1610813126
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 219,
      "created_at": 1610813134,
      "shares": [
        "PRR_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 220,
      "created_at": 1610813140
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 221,
      "created_at": 1610813145,
      "shares": [
        "NW_8"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 222,
      "created_at": 1610813151
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 223,
      "created_at": 1610813170,
      "shares": [
        "B&O_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 224,
      "created_at": 1610813172
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 225,
      "created_at": 1610813177,
      "shares": [
        "PRR_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 226,
      "created_at": 1610813186
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 227,
      "created_at": 1610813212,
      "shares": [
        "GT_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 228,
      "created_at": 1610813214
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 229,
      "created_at": 1610813228,
      "shares": [
        "NKP_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 230,
      "created_at": 1610813231
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 231,
      "created_at": 1610813244,
      "shares": [
        "PRR_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 232,
      "created_at": 1610813245
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 233,
      "created_at": 1610813256,
      "shares": [
        "PRR_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 234,
      "created_at": 1610813256
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 235,
      "created_at": 1610813262,
      "shares": [
        "PRR_6"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 236,
      "created_at": 1610813264
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 237,
      "created_at": 1610813271
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 238,
      "created_at": 1610813297
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 239,
      "created_at": 1610813301
    },
    {
      "type": "lay_tile",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 240,
      "created_at": 1610813358,
      "hex": "H18",
      "tile": "7-0",
      "rotation": 0
    },
    {
      "type": "buy_train",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 241,
      "created_at": 1610813386,
      "train": "2-5",
      "price": 1
    },
    {
      "type": "pass",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 242,
      "created_at": 1610813388
    },
    {
      "type": "pass",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 243,
      "created_at": 1610813432
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 244,
      "created_at": 1610813459,
      "hex": "F6",
      "tile": "8-5",
      "rotation": 4
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 245,
      "created_at": 1610813462
    },
    {
      "type": "run_routes",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 246,
      "created_at": 1610813466,
      "routes": [
        {
          "train": "2-0",
          "connections": [
            [
              "F10",
              "G9",
              "H8"
            ]
          ],
          "hexes": [
            "F10",
            "H8"
          ],
          "revenue": 50,
          "revenue_str": "F10-H8"
        },
        {
          "train": "3-5",
          "connections": [
            [
              "F8",
              "F10"
            ]
          ],
          "hexes": [
            "F8",
            "F10"
          ],
          "revenue": 50,
          "revenue_str": "F8-F10"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 247,
      "created_at": 1610813467,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 248,
      "created_at": 1610813473
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 249,
      "created_at": 1610813475
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 250,
      "created_at": 1610813505,
      "hex": "I17",
      "tile": "8-6",
      "rotation": 3
    },
    {
      "type": "run_routes",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 251,
      "created_at": 1610813538,
      "routes": [
        {
          "train": "2-2",
          "connections": [
            [
              "J18",
              "I19"
            ]
          ],
          "hexes": [
            "I19",
            "J18"
          ],
          "revenue": 80,
          "revenue_str": "I19-J18"
        },
        {
          "train": "2-3",
          "connections": [
            [
              "K19",
              "K17",
              "L16"
            ]
          ],
          "hexes": [
            "L16",
            "K19"
          ],
          "revenue": 60,
          "revenue_str": "L16-K19"
        },
        {
          "train": "2-4",
          "connections": [
            [
              "K19",
              "L18"
            ]
          ],
          "hexes": [
            "L18",
            "K19"
          ],
          "revenue": 40,
          "revenue_str": "L18-K19"
        },
        {
          "train": "3-6",
          "connections": [
            [
              "J18",
              "I17",
              "H18",
              "H16"
            ],
            [
              "K19",
              "J18"
            ]
          ],
          "hexes": [
            "H16",
            "J18",
            "K19"
          ],
          "revenue": 80,
          "revenue_str": "H16-J18-K19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 252,
      "created_at": 1610813546,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 253,
      "created_at": 1610813555
    },
    {
      "type": "lay_tile",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 254,
      "created_at": 1610813579,
      "hex": "D6",
      "tile": "14-0",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 255,
      "created_at": 1610813582
    },
    {
      "type": "run_routes",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 256,
      "created_at": 1610813588,
      "routes": [
        {
          "train": "3-1",
          "connections": [
            [
              "E7",
              "D6"
            ],
            [
              "E9",
              "E7"
            ]
          ],
          "hexes": [
            "D6",
            "E7",
            "E9"
          ],
          "revenue": 80,
          "revenue_str": "D6-E7-E9"
        },
        {
          "train": "3-2",
          "connections": [
            [
              "C5",
              "D6"
            ],
            [
              "D4",
              "C5"
            ]
          ],
          "hexes": [
            "D6",
            "C5",
            "D4"
          ],
          "revenue": 70,
          "revenue_str": "D6-C5-D4"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 257,
      "created_at": 1610813589,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 258,
      "created_at": 1610813595
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 259,
      "created_at": 1610813597
    },
    {
      "type": "lay_tile",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 260,
      "created_at": 1610813607,
      "hex": "H18",
      "tile": "28-0",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 261,
      "created_at": 1610813610
    },
    {
      "type": "run_routes",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 262,
      "created_at": 1610813622,
      "routes": [
        {
          "train": "3-3",
          "connections": [
            [
              "H16",
              "H18",
              "I19"
            ]
          ],
          "hexes": [
            "I19",
            "H16"
          ],
          "revenue": 70,
          "revenue_str": "I19-H16"
        },
        {
          "train": "3-4",
          "connections": [
            [
              "I19",
              "J18"
            ]
          ],
          "hexes": [
            "I19",
            "J18"
          ],
          "revenue": 80,
          "revenue_str": "I19-J18"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 263,
      "created_at": 1610813623,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 264,
      "created_at": 1610813625
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 265,
      "created_at": 1610813626
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 266,
      "created_at": 1610813933,
      "message": "?\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 267,
      "created_at": 1610814051,
      "message": "the game was broken\n"
    },
    {
      "id": 268,
      "hex": "D8",
      "tile": "14-1",
      "type": "lay_tile",
      "entity": "MC",
      "rotation": 1,
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814057
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 269,
      "created_at": 1610814065,
      "message": "nvm, it's fine now, sorry\n"
    },
    {
      "id": 270,
      "type": "undo",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814132
    },
    {
      "type": "lay_tile",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 271,
      "created_at": 1610814147,
      "hex": "D8",
      "tile": "206-0",
      "rotation": 5
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 272,
      "created_at": 1610814176
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 273,
      "created_at": 1610814188
    },
    {
      "type": "run_routes",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 274,
      "created_at": 1610814192,
      "routes": [
        {
          "train": "3-0",
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "revenue": 110,
          "revenue_str": "A3-A5-A7"
        },
        {
          "train": "2-6",
          "connections": [
            [
              "A7",
              "B8",
              "C7",
              "D8"
            ]
          ],
          "hexes": [
            "A7",
            "D8"
          ],
          "revenue": 60,
          "revenue_str": "A7-D8"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 275,
      "created_at": 1610814197,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 276,
      "created_at": 1610814200
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 277,
      "created_at": 1610814203
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 278,
      "created_at": 1610814247,
      "hex": "H14",
      "tile": "4-0",
      "rotation": 1
    },
    {
      "type": "run_routes",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 279,
      "created_at": 1610814254,
      "routes": [
        {
          "train": "2-2",
          "connections": [
            [
              "J18",
              "I19"
            ]
          ],
          "hexes": [
            "J18",
            "I19"
          ],
          "revenue": 80,
          "revenue_str": "J18-I19"
        },
        {
          "train": "2-3",
          "connections": [
            [
              "K19",
              "K17",
              "L16"
            ]
          ],
          "hexes": [
            "K19",
            "L16"
          ],
          "revenue": 60,
          "revenue_str": "K19-L16"
        },
        {
          "train": "2-4",
          "connections": [
            [
              "K19",
              "L18"
            ]
          ],
          "hexes": [
            "K19",
            "L18"
          ],
          "revenue": 40,
          "revenue_str": "K19-L18"
        },
        {
          "train": "3-6",
          "connections": [
            [
              "J18",
              "I17",
              "H18",
              "H16"
            ],
            [
              "K19",
              "J18"
            ]
          ],
          "hexes": [
            "H16",
            "J18",
            "K19"
          ],
          "revenue": 80,
          "revenue_str": "H16-J18-K19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 280,
      "created_at": 1610814256,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 281,
      "created_at": 1610814260
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 282,
      "created_at": 1610814269,
      "hex": "G5",
      "tile": "8-7",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 283,
      "created_at": 1610814271
    },
    {
      "type": "run_routes",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 284,
      "created_at": 1610814282,
      "routes": [
        {
          "train": "2-0",
          "connections": [
            [
              "F10",
              "G9",
              "H8"
            ]
          ],
          "hexes": [
            "F10",
            "H8"
          ],
          "revenue": 50,
          "revenue_str": "F10-H8"
        },
        {
          "train": "3-5",
          "connections": [
            [
              "F8",
              "F6",
              "G5",
              "G3"
            ],
            [
              "F8",
              "F10"
            ]
          ],
          "hexes": [
            "G3",
            "F8",
            "F10"
          ],
          "revenue": 90,
          "revenue_str": "G3-F8-F10"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 285,
      "created_at": 1610814283,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 286,
      "created_at": 1610814288
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 287,
      "created_at": 1610814303
    },
    {
      "type": "lay_tile",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 288,
      "created_at": 1610814326,
      "hex": "E5",
      "tile": "9-2",
      "rotation": 2
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 289,
      "created_at": 1610814328
    },
    {
      "type": "run_routes",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 290,
      "created_at": 1610814330,
      "routes": [
        {
          "train": "3-1",
          "connections": [
            [
              "E7",
              "D6"
            ],
            [
              "E9",
              "E7"
            ]
          ],
          "hexes": [
            "D6",
            "E7",
            "E9"
          ],
          "revenue": 80,
          "revenue_str": "D6-E7-E9"
        },
        {
          "train": "3-2",
          "connections": [
            [
              "C5",
              "D6"
            ],
            [
              "D4",
              "C5"
            ]
          ],
          "hexes": [
            "D6",
            "C5",
            "D4"
          ],
          "revenue": 70,
          "revenue_str": "D6-C5-D4"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 291,
      "created_at": 1610814348,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 292,
      "created_at": 1610814350
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 293,
      "created_at": 1610814352
    },
    {
      "type": "lay_tile",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 294,
      "created_at": 1610814374,
      "hex": "H12",
      "tile": "57-6",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 295,
      "created_at": 1610814383
    },
    {
      "type": "run_routes",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 296,
      "created_at": 1610814396,
      "routes": [
        {
          "train": "3-3",
          "connections": [
            [
              "H14",
              "H12"
            ],
            [
              "I19",
              "H18",
              "H16",
              "H14"
            ]
          ],
          "hexes": [
            "H12",
            "H14",
            "I19"
          ],
          "revenue": 80,
          "revenue_str": "H12-H14-I19"
        },
        {
          "train": "3-4",
          "connections": [
            [
              "I19",
              "J18"
            ]
          ],
          "hexes": [
            "I19",
            "J18"
          ],
          "revenue": 80,
          "revenue_str": "I19-J18"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 297,
      "created_at": 1610814397,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 298,
      "created_at": 1610814398
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 299,
      "created_at": 1610814399
    },
    {
      "type": "buy_company",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 300,
      "created_at": 1610814546,
      "company": "D&H",
      "price": 160
    },
    {
      "type": "lay_tile",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 301,
      "created_at": 1610814589,
      "hex": "F20",
      "tile": "57-7",
      "rotation": 2
    },
    {
      "type": "place_token",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 302,
      "created_at": 1610814591,
      "city": "57-7-0",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 303,
      "created_at": 1610814600,
      "routes": [
        {
          "train": "2-5",
          "connections": [
            [
              "H16",
              "H18",
              "I19"
            ]
          ],
          "hexes": [
            "I19",
            "H16"
          ],
          "revenue": 70,
          "revenue_str": "I19-H16"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 304,
      "created_at": 1610814606,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 305,
      "created_at": 1610814636
    },
    {
      "type": "pass",
      "entity": "PRR",
      "entity_type": "corporation",
      "id": 306,
      "created_at": 1610814645
    },
    {
      "id": 307,
      "hex": "D10",
      "tile": "3-0",
      "type": "lay_tile",
      "entity": "MC",
      "rotation": 0,
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814664
    },
    {
      "id": 308,
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814671
    },
    {
      "id": 309,
      "city": "59-0-1",
      "slot": 0,
      "type": "place_token",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814673
    },
    {
      "id": 310,
      "type": "undo",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814725
    },
    {
      "id": 311,
      "type": "undo",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814734
    },
    {
      "id": 312,
      "type": "undo",
      "entity": "MC",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610814740
    },
    {
      "type": "lay_tile",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 313,
      "created_at": 1610814762,
      "hex": "D10",
      "tile": "3-0",
      "rotation": 0
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 314,
      "created_at": 1610814766
    },
    {
      "type": "place_token",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 315,
      "created_at": 1610814768,
      "city": "59-0-1",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 316,
      "created_at": 1610814776,
      "routes": [
        {
          "train": "3-0",
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "revenue": 110,
          "revenue_str": "A3-A5-A7"
        },
        {
          "train": "2-6",
          "connections": [
            [
              "A7",
              "B8",
              "C7",
              "D8"
            ]
          ],
          "hexes": [
            "A7",
            "D8"
          ],
          "revenue": 60,
          "revenue_str": "A7-D8"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 317,
      "created_at": 1610814779,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 318,
      "created_at": 1610814783
    },
    {
      "type": "pass",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 319,
      "created_at": 1610814786
    },
    {
      "type": "par",
      "entity": 2843,
      "entity_type": "player",
      "id": 320,
      "created_at": 1610814822,
      "corporation": "OS&H",
      "share_price": "94,5,3"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 321,
      "created_at": 1610814826
    },
    {
      "type": "sell_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 322,
      "created_at": 1610814872,
      "shares": [
        "NW_5",
        "NW_7"
      ],
      "percent": 20
    },
    {
      "type": "par",
      "entity": 5518,
      "entity_type": "player",
      "id": 323,
      "created_at": 1610814891,
      "corporation": "NYH",
      "share_price": "94,5,3"
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 324,
      "created_at": 1610814895
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 325,
      "created_at": 1610815120,
      "message": "hrm\n"
    },
    {
      "type": "par",
      "entity": 4267,
      "entity_type": "player",
      "id": 326,
      "created_at": 1610815201,
      "corporation": "NYC",
      "share_price": "94,5,3"
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 327,
      "created_at": 1610815245
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 328,
      "created_at": 1610815253,
      "shares": [
        "OS&H_1"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 329,
      "created_at": 1610815276
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 330,
      "created_at": 1610815283,
      "shares": [
        "NYH_1"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 331,
      "created_at": 1610815299
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 332,
      "created_at": 1610815338,
      "shares": [
        "NYC_1"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 333,
      "created_at": 1610815341
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 334,
      "created_at": 1610815355,
      "shares": [
        "OS&H_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 335,
      "created_at": 1610815357
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 336,
      "created_at": 1610815362,
      "shares": [
        "NYH_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 337,
      "created_at": 1610815363
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 338,
      "created_at": 1610815385,
      "shares": [
        "NYC_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 339,
      "created_at": 1610815386
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 340,
      "created_at": 1610815392,
      "shares": [
        "OS&H_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 341,
      "created_at": 1610815394
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 342,
      "created_at": 1610815400,
      "shares": [
        "NYH_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 343,
      "created_at": 1610815402
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 344,
      "created_at": 1610815413,
      "shares": [
        "NYC_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 345,
      "created_at": 1610815462
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 346,
      "created_at": 1610815469,
      "shares": [
        "OS&H_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 347,
      "created_at": 1610815475
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 348,
      "created_at": 1610815484,
      "shares": [
        "NYH_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 349,
      "created_at": 1610815498
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 350,
      "created_at": 1610815539,
      "shares": [
        "NYC_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 351,
      "created_at": 1610815540
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 352,
      "created_at": 1610815565,
      "shares": [
        "MC_7"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 353,
      "created_at": 1610815572
    },
    {
      "id": 354,
      "type": "choose",
      "choice": "NYH",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815594
    },
    {
      "id": 355,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815615
    },
    {
      "id": 356,
      "type": "choose",
      "choice": "NW",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815619
    },
    {
      "id": 357,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815646
    },
    {
      "id": 358,
      "type": "choose",
      "choice": "NKP",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815649
    },
    {
      "id": 359,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815660
    },
    {
      "id": 360,
      "type": "choose",
      "choice": "NYH",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815674
    },
    {
      "id": 361,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610815686
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 362,
      "created_at": 1610815703,
      "shares": [
        "NYC_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 363,
      "created_at": 1610815704
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 364,
      "created_at": 1610815810
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 365,
      "created_at": 1610815832,
      "shares": [
        "MC_8"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 366,
      "created_at": 1610815838
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 367,
      "created_at": 1610815849
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 368,
      "created_at": 1610815887
    },
    {
      "id": 369,
      "type": "choose",
      "choice": "OS&H",
      "entity": 2843,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610815898
    },
    {
      "id": 370,
      "type": "undo",
      "entity": 2843,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610815954
    },
    {
      "id": 371,
      "type": "choose",
      "choice": "MC",
      "entity": 2843,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610815959
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 372,
      "created_at": 1610816039,
      "message": "hmm, per the rules I should be able to merge the green OSHA company with the MC'\n"
    },
    {
      "id": 373,
      "type": "undo",
      "entity": 2843,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610816047
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 374,
      "created_at": 1610816067,
      "message": "nope- MC was floated in a prior SR\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 375,
      "created_at": 1610816081,
      "message": "ohhhh\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 376,
      "created_at": 1610816081,
      "message": "yup\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 377,
      "created_at": 1610816110,
      "message": "Both companies have to 1) both floated in a prior SR, or 2) floated (or not yet floated) in this SR\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 378,
      "created_at": 1610816120,
      "message": "I believe\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 379,
      "created_at": 1610816180,
      "message": "\"A pair of public companies, neither of which were floated in a previous SR, but one or both have been floated this SR\n"
    },
    {
      "type": "choose",
      "entity": 2843,
      "entity_type": "player",
      "id": 380,
      "created_at": 1610816209,
      "choice": "MC"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 381,
      "created_at": 1610816214,
      "message": "i think that means you can merge a company that floated this SR with one that hasn't floated yet\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 382,
      "created_at": 1610816232,
      "message": "yeah\n"
    },
    {
      "type": "merge",
      "entity": "MC",
      "entity_type": "corporation",
      "id": 383,
      "created_at": 1610816265,
      "corporation": "PRR"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 384,
      "created_at": 1610816268,
      "message": "which I could have done with my 2 30% companies at the start\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 385,
      "created_at": 1610816277,
      "message": "if I could float one\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 386,
      "created_at": 1610816284,
      "message": "right\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 387,
      "created_at": 1610816289,
      "message": "interesting\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 388,
      "created_at": 1610816296,
      "message": "but you lose value in merging\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 389,
      "created_at": 1610816350,
      "message": "just like I did by putting myself in second by merging the PRR and the MC\n"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 390,
      "created_at": 1610816352
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 391,
      "created_at": 1610816372
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 392,
      "created_at": 1610816431
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 393,
      "created_at": 1610816445
    },
    {
      "id": 394,
      "hex": "G21",
      "tile": "56-0",
      "type": "lay_tile",
      "entity": "MC-PRR",
      "rotation": 1,
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816478
    },
    {
      "id": 395,
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816527
    },
    {
      "id": 396,
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816534
    },
    {
      "id": 397,
      "type": "run_routes",
      "entity": "MC-PRR",
      "routes": [
        {
          "hexes": [
            "D8",
            "A7"
          ],
          "train": "2-6",
          "revenue": 60,
          "connections": [
            [
              "A7",
              "B8",
              "C7",
              "D8"
            ]
          ],
          "revenue_str": "D8-A7"
        },
        {
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "train": "3-0",
          "revenue": 110,
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "revenue_str": "A3-A5-A7"
        },
        {
          "hexes": [
            "I19",
            "H16"
          ],
          "train": "2-5",
          "revenue": 70,
          "connections": [
            [
              "H16",
              "H18",
              "I19"
            ]
          ],
          "revenue_str": "I19-H16"
        }
      ],
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816626
    },
    {
      "id": 398,
      "kind": "payout",
      "type": "dividend",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816630
    },
    {
      "id": 399,
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816644
    },
    {
      "id": 400,
      "type": "undo",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816679
    },
    {
      "id": 401,
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816682
    },
    {
      "id": 402,
      "type": "buy_train",
      "price": 160,
      "shell": "PRR",
      "train": "3-7",
      "entity": "MC-PRR",
      "variant": "3",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816702
    },
    {
      "id": 403,
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816724
    },
    {
      "id": 404,
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816734
    },
    {
      "id": 405,
      "type": "undo",
      "entity": "NW",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610816760
    },
    {
      "id": 406,
      "type": "undo",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816764
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 407,
      "created_at": 1610816774,
      "message": "just remembered a system can lay two tiles\n"
    },
    {
      "id": 408,
      "type": "undo",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816784
    },
    {
      "id": 409,
      "type": "undo",
      "entity": "MC-PRR",
      "action_id": 394,
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816793
    },
    {
      "id": 410,
      "type": "undo",
      "entity": "MC-PRR",
      "entity_type": "system",
      "user": 2843,
      "created_at": 1610816802
    },
    {
      "type": "lay_tile",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 411,
      "created_at": 1610816824,
      "hex": "G21",
      "tile": "1-0",
      "rotation": 1
    },
    {
      "type": "lay_tile",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 412,
      "created_at": 1610816830,
      "hex": "G23",
      "tile": "54-0",
      "rotation": 0
    },
    {
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 413,
      "created_at": 1610816835
    },
    {
      "type": "place_token",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 414,
      "created_at": 1610816840,
      "city": "54-0-0",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 415,
      "created_at": 1610816892,
      "routes": [
        {
          "train": "2-6",
          "connections": [
            [
              "A7",
              "B8",
              "C7",
              "D8"
            ]
          ],
          "hexes": [
            "D8",
            "A7"
          ],
          "revenue": 60,
          "revenue_str": "D8-A7"
        },
        {
          "train": "3-0",
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "revenue": 110,
          "revenue_str": "A3-A5-A7"
        },
        {
          "train": "2-5",
          "connections": [
            [
              "G23",
              "G21"
            ]
          ],
          "hexes": [
            "G21",
            "G23"
          ],
          "revenue": 70,
          "revenue_str": "G21-G23"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 416,
      "created_at": 1610816894,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 417,
      "created_at": 1610816896
    },
    {
      "type": "buy_train",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 418,
      "created_at": 1610816900,
      "train": "3-7",
      "price": 160,
      "variant": "3",
      "shell": "PRR"
    },
    {
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 419,
      "created_at": 1610816901
    },
    {
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 420,
      "created_at": 1610816904
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 421,
      "created_at": 1610816939,
      "hex": "H10",
      "tile": "9-3",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 422,
      "created_at": 1610816944
    },
    {
      "type": "run_routes",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 423,
      "created_at": 1610816953,
      "routes": [
        {
          "train": "2-2",
          "connections": [
            [
              "J18",
              "I19"
            ]
          ],
          "hexes": [
            "J18",
            "I19"
          ],
          "revenue": 80,
          "revenue_str": "J18-I19"
        },
        {
          "train": "2-3",
          "connections": [
            [
              "K19",
              "K17",
              "L16"
            ]
          ],
          "hexes": [
            "K19",
            "L16"
          ],
          "revenue": 60,
          "revenue_str": "K19-L16"
        },
        {
          "train": "2-4",
          "connections": [
            [
              "K19",
              "L18"
            ]
          ],
          "hexes": [
            "K19",
            "L18"
          ],
          "revenue": 40,
          "revenue_str": "K19-L18"
        },
        {
          "train": "3-6",
          "connections": [
            [
              "J18",
              "I17",
              "H18",
              "H16"
            ],
            [
              "K19",
              "J18"
            ]
          ],
          "hexes": [
            "H16",
            "J18",
            "K19"
          ],
          "revenue": 80,
          "revenue_str": "H16-J18-K19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 424,
      "created_at": 1610816954,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 425,
      "created_at": 1610816956
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 426,
      "created_at": 1610816976,
      "hex": "H8",
      "tile": "14-1",
      "rotation": 0
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 427,
      "created_at": 1610816979
    },
    {
      "type": "run_routes",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 428,
      "created_at": 1610816992,
      "routes": [
        {
          "train": "2-0",
          "connections": [
            [
              "F10",
              "G9",
              "H8"
            ]
          ],
          "hexes": [
            "F10",
            "H8"
          ],
          "revenue": 60,
          "revenue_str": "F10-H8"
        },
        {
          "train": "3-5",
          "connections": [
            [
              "F8",
              "F6",
              "G5",
              "G3"
            ],
            [
              "F8",
              "F10"
            ]
          ],
          "hexes": [
            "G3",
            "F8",
            "F10"
          ],
          "revenue": 90,
          "revenue_str": "G3-F8-F10"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 429,
      "created_at": 1610816994,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 430,
      "created_at": 1610817000
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 431,
      "created_at": 1610817003
    },
    {
      "id": 432,
      "hex": "B16",
      "tile": "8-8",
      "type": "lay_tile",
      "entity": "OS&H",
      "rotation": 2,
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610817101
    },
    {
      "id": 433,
      "type": "pass",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610817108
    },
    {
      "id": 434,
      "type": "pass",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610817117
    },
    {
      "id": 435,
      "type": "undo",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610817127
    },
    {
      "id": 436,
      "type": "undo",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610817132
    },
    {
      "id": 437,
      "type": "undo",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610817136
    },
    {
      "type": "lay_tile",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 438,
      "created_at": 1610817140,
      "hex": "B16",
      "tile": "8-8",
      "rotation": 0
    },
    {
      "type": "pass",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 439,
      "created_at": 1610817143
    },
    {
      "type": "pass",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 440,
      "created_at": 1610817145
    },
    {
      "type": "lay_tile",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 441,
      "created_at": 1610817163,
      "hex": "F22",
      "tile": "8-9",
      "rotation": 5
    },
    {
      "id": 442,
      "hex": "F24",
      "tile": "56-0",
      "type": "lay_tile",
      "entity": "NYH",
      "rotation": 0,
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817185
    },
    {
      "id": 443,
      "type": "undo",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817195
    },
    {
      "id": 444,
      "hex": "F24",
      "tile": "56-0",
      "type": "lay_tile",
      "entity": "NYH",
      "rotation": 0,
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817226
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 445,
      "created_at": 1610817246,
      "message": "I think that's a bug\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 446,
      "created_at": 1610817264,
      "message": "?\n"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 447,
      "created_at": 1610817275,
      "message": "Am I supposed to be able to lay 2 track?\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 448,
      "created_at": 1610817318,
      "message": "with a system\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 449,
      "created_at": 1610817319,
      "message": "yes\n"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 450,
      "created_at": 1610817338,
      "message": "NYH is not a system though\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 451,
      "created_at": 1610817347,
      "message": "oh wait\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 452,
      "created_at": 1610817363,
      "message": "the NYH and the B&M get extra tile lays\n"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 453,
      "created_at": 1610817372,
      "message": "oh ok\n"
    },
    {
      "id": 454,
      "type": "buy_train",
      "price": 160,
      "train": "3-8",
      "entity": "NYH",
      "variant": "3",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817396
    },
    {
      "id": 455,
      "type": "buy_train",
      "price": 250,
      "train": "5-0",
      "entity": "NYH",
      "variant": "5",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817397
    },
    {
      "id": 456,
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817405
    },
    {
      "id": 457,
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817409
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 458,
      "created_at": 1610817413,
      "message": "looks like it's says in the company box as an ability\n"
    },
    {
      "id": 459,
      "type": "undo",
      "entity": "NYC",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817435
    },
    {
      "id": 460,
      "type": "undo",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817439
    },
    {
      "id": 461,
      "type": "undo",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817443
    },
    {
      "id": 462,
      "type": "undo",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817447
    },
    {
      "id": 463,
      "type": "undo",
      "entity": "NYH",
      "entity_type": "corporation",
      "user": 5518,
      "created_at": 1610817454
    },
    {
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 464,
      "created_at": 1610817457
    },
    {
      "type": "buy_train",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 465,
      "created_at": 1610817464,
      "train": "3-8",
      "price": 160,
      "variant": "3"
    },
    {
      "type": "buy_train",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 466,
      "created_at": 1610817465,
      "train": "5-0",
      "price": 250,
      "variant": "5"
    },
    {
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 467,
      "created_at": 1610817467
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 468,
      "created_at": 1610817472,
      "message": "I see it now\n"
    },
    {
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 469,
      "created_at": 1610817479
    },
    {
      "type": "lay_tile",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 470,
      "created_at": 1610817517,
      "hex": "E23",
      "tile": "57-0",
      "rotation": 2
    },
    {
      "type": "buy_train",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 471,
      "created_at": 1610817524,
      "train": "5-1",
      "price": 250,
      "variant": "5"
    },
    {
      "type": "buy_train",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 472,
      "created_at": 1610817687,
      "train": "5-2",
      "price": 250,
      "variant": "5"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 473,
      "created_at": 1610817766,
      "message": "sorry- trying to do train-jitsu\n"
    },
    {
      "type": "buy_train",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 474,
      "created_at": 1610817785,
      "train": "5-3",
      "price": 250,
      "variant": "5"
    },
    {
      "type": "buy_train",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 475,
      "created_at": 1610817802,
      "train": "3-3",
      "price": 190
    },
    {
      "type": "lay_tile",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 476,
      "created_at": 1610817822,
      "hex": "F6",
      "tile": "25-0",
      "rotation": 0
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 477,
      "created_at": 1610817871
    },
    {
      "type": "run_routes",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 478,
      "created_at": 1610817887,
      "routes": [
        {
          "train": "3-1",
          "connections": [
            [
              "D4",
              "E5",
              "F6",
              "G5",
              "G3"
            ],
            [
              "D6",
              "D4"
            ]
          ],
          "hexes": [
            "G3",
            "D4",
            "D6"
          ],
          "revenue": 100,
          "revenue_str": "G3-D4-D6"
        },
        {
          "train": "3-2",
          "connections": [
            [
              "E7",
              "D6"
            ],
            [
              "E9",
              "E7"
            ]
          ],
          "hexes": [
            "D6",
            "E7",
            "E9"
          ],
          "revenue": 80,
          "revenue_str": "D6-E7-E9"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 479,
      "created_at": 1610817889,
      "kind": "payout"
    },
    {
      "type": "buy_train",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 480,
      "created_at": 1610817910,
      "train": "5-1",
      "price": 110
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 481,
      "created_at": 1610817912
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 482,
      "created_at": 1610817913
    },
    {
      "id": 483,
      "hex": "H12",
      "tile": "14-2",
      "type": "lay_tile",
      "entity": "B&O",
      "rotation": 3,
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610817956
    },
    {
      "id": 484,
      "type": "undo",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610817965
    },
    {
      "type": "lay_tile",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 485,
      "created_at": 1610817973,
      "hex": "H12",
      "tile": "15-0",
      "rotation": 4
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 486,
      "created_at": 1610817981
    },
    {
      "type": "run_routes",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 487,
      "created_at": 1610817994,
      "routes": [
        {
          "train": "3-4",
          "connections": [
            [
              "I19",
              "H18",
              "H16"
            ],
            [
              "I19",
              "J18"
            ]
          ],
          "hexes": [
            "H16",
            "I19",
            "J18"
          ],
          "revenue": 100,
          "revenue_str": "H16-I19-J18"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 488,
      "created_at": 1610818002,
      "kind": "payout"
    },
    {
      "type": "buy_train",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 489,
      "created_at": 1610818006,
      "train": "3+D-0",
      "price": 350,
      "variant": "3+D"
    },
    {
      "type": "buy_train",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 490,
      "created_at": 1610818042,
      "train": "5-2",
      "price": 15
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 491,
      "created_at": 1610818090,
      "message": "Buying all these non-permanents is such a bad idea\n"
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 492,
      "created_at": 1610818093
    },
    {
      "type": "buy_company",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 493,
      "created_at": 1610818125,
      "company": "C&A",
      "price": 320
    },
    {
      "type": "lay_tile",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 494,
      "created_at": 1610818132,
      "hex": "H22",
      "tile": "59-1",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 495,
      "created_at": 1610818137
    },
    {
      "type": "place_token",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 496,
      "created_at": 1610818140,
      "city": "59-1-1",
      "slot": 0
    },
    {
      "type": "run_routes",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 497,
      "created_at": 1610818167,
      "routes": [
        {
          "train": "3-0",
          "connections": [
            [
              "A5",
              "A3"
            ],
            [
              "A7",
              "A5"
            ]
          ],
          "hexes": [
            "A3",
            "A5",
            "A7"
          ],
          "revenue": 110,
          "revenue_str": "A3-A5-A7"
        },
        {
          "train": "3-7",
          "connections": [
            [
              "G23",
              "G21"
            ],
            [
              "H22",
              "G23"
            ]
          ],
          "hexes": [
            "G21",
            "G23",
            "H22"
          ],
          "revenue": 110,
          "revenue_str": "G21-G23-H22"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 498,
      "created_at": 1610818174,
      "kind": "payout"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 499,
      "created_at": 1610818174,
      "message": "dammit- did not realize you had bought in the CA\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 500,
      "created_at": 1610818185,
      "message": "nvm- just did it\n"
    },
    {
      "type": "swap_train",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 501,
      "created_at": 1610818204,
      "train": "3-7"
    },
    {
      "type": "pass",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 502,
      "created_at": 1610818211
    },
    {
      "type": "buy_train",
      "entity": "MC-PRR",
      "entity_type": "system",
      "id": 503,
      "created_at": 1610818223,
      "train": "3+D-1",
      "price": 350,
      "variant": "3+D",
      "shell": "PRR"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 504,
      "created_at": 1610818240,
      "message": "yeah I've been saving that\n"
    },
    {
      "type": "lay_tile",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 505,
      "created_at": 1610818256,
      "hex": "I19",
      "tile": "61-0",
      "rotation": 0
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 506,
      "created_at": 1610818273,
      "message": "i noticed...\n"
    },
    {
      "type": "place_token",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 507,
      "created_at": 1610818289,
      "city": "15-0-0",
      "slot": 1
    },
    {
      "type": "run_routes",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 508,
      "created_at": 1610818307,
      "routes": [
        {
          "train": "3-6",
          "connections": [
            [
              "J18",
              "I17",
              "H18",
              "H16"
            ],
            [
              "J18",
              "I19"
            ]
          ],
          "hexes": [
            "H16",
            "J18",
            "I19"
          ],
          "revenue": 120,
          "revenue_str": "H16-J18-I19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 509,
      "created_at": 1610818309,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 510,
      "created_at": 1610818333
    },
    {
      "type": "pass",
      "entity": "NW",
      "entity_type": "corporation",
      "id": 511,
      "created_at": 1610818337
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 512,
      "created_at": 1610818349,
      "message": "heheh\n"
    },
    {
      "type": "lay_tile",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 513,
      "created_at": 1610818404,
      "hex": "F8",
      "tile": "14-2",
      "rotation": 0
    },
    {
      "type": "place_token",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 514,
      "created_at": 1610818405,
      "city": "15-0-0",
      "slot": 1
    },
    {
      "type": "run_routes",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 515,
      "created_at": 1610818420,
      "routes": [
        {
          "train": "3-5",
          "connections": [
            [
              "F8",
              "F6",
              "G5",
              "G3"
            ],
            [
              "F8",
              "F10"
            ]
          ],
          "hexes": [
            "G3",
            "F8",
            "F10"
          ],
          "revenue": 140,
          "revenue_str": "G3-F8-F10"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 516,
      "created_at": 1610818421,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 517,
      "created_at": 1610818431
    },
    {
      "type": "pass",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 518,
      "created_at": 1610818433
    },
    {
      "id": 519,
      "hex": "E9",
      "tile": "66-0",
      "type": "lay_tile",
      "entity": "GT",
      "rotation": 1,
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610818574
    },
    {
      "id": 520,
      "type": "undo",
      "entity": "GT",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610818597
    },
    {
      "type": "lay_tile",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 521,
      "created_at": 1610818603,
      "hex": "D8",
      "tile": "449-0",
      "rotation": 1
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 522,
      "created_at": 1610818610
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 523,
      "created_at": 1610818635,
      "message": "each corner of the map has it's own mess going on. I love it\n"
    },
    {
      "type": "run_routes",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 524,
      "created_at": 1610818674,
      "routes": [
        {
          "train": "3-1",
          "connections": [
            [
              "D4",
              "E5",
              "F6",
              "G5",
              "G3"
            ],
            [
              "D4",
              "C5"
            ]
          ],
          "hexes": [
            "G3",
            "D4",
            "C5"
          ],
          "revenue": 110,
          "revenue_str": "G3-D4-C5"
        },
        {
          "train": "3-2",
          "connections": [
            [
              "E7",
              "D6"
            ],
            [
              "E9",
              "E7"
            ]
          ],
          "hexes": [
            "D6",
            "E7",
            "E9"
          ],
          "revenue": 80,
          "revenue_str": "D6-E7-E9"
        },
        {
          "train": "5-1",
          "connections": [
            [
              "D6",
              "D4"
            ],
            [
              "D6",
              "D8"
            ],
            [
              "D8",
              "D10"
            ],
            [
              "D10",
              "E9"
            ]
          ],
          "hexes": [
            "D4",
            "D6",
            "D8",
            "D10",
            "E9"
          ],
          "revenue": 150,
          "revenue_str": "D4-D6-D8-D10-E9"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 525,
      "created_at": 1610818678,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "GT",
      "entity_type": "corporation",
      "id": 526,
      "created_at": 1610818681
    },
    {
      "type": "lay_tile",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 527,
      "created_at": 1610818703,
      "hex": "H22",
      "tile": "64-0",
      "rotation": 3
    },
    {
      "id": 528,
      "city": "64-0-1",
      "slot": 0,
      "type": "place_token",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610818719
    },
    {
      "id": 529,
      "type": "undo",
      "entity": "B&O",
      "entity_type": "corporation",
      "user": 4267,
      "created_at": 1610818727
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 530,
      "created_at": 1610818767
    },
    {
      "type": "run_routes",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 531,
      "created_at": 1610818817,
      "routes": [
        {
          "train": "3-4",
          "connections": [
            [
              "C19",
              "C17",
              "C15"
            ],
            [
              "B20",
              "C19"
            ]
          ],
          "hexes": [
            "C15",
            "C19",
            "B20"
          ],
          "revenue": 50,
          "revenue_str": "C15-C19-B20"
        },
        {
          "train": "3+D-0",
          "connections": [
            [
              "I19",
              "J18"
            ],
            [
              "H22",
              "I21",
              "I19"
            ]
          ],
          "hexes": [
            "J18",
            "I19",
            "H22"
          ],
          "revenue": 280,
          "revenue_str": "J18-I19-H22"
        },
        {
          "train": "5-2",
          "connections": [
            [
              "H14",
              "H12"
            ],
            [
              "I19",
              "H18",
              "H16",
              "H14"
            ]
          ],
          "hexes": [
            "H12",
            "H14",
            "I19"
          ],
          "revenue": 100,
          "revenue_str": "H12-H14-I19"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 532,
      "created_at": 1610818823,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 533,
      "created_at": 1610818826
    },
    {
      "id": 534,
      "hex": "B16",
      "tile": "25-1",
      "type": "lay_tile",
      "entity": "OS&H",
      "rotation": 2,
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610818846
    },
    {
      "id": 535,
      "type": "buy_train",
      "price": 350,
      "train": "3+D-2",
      "entity": "OS&H",
      "variant": "3+D",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610818850
    },
    {
      "id": 536,
      "type": "buy_train",
      "price": 350,
      "train": "3+D-3",
      "entity": "OS&H",
      "variant": "3+D",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610818852
    },
    {
      "id": 537,
      "type": "undo",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610818871
    },
    {
      "id": 538,
      "type": "undo",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610818876
    },
    {
      "id": 539,
      "type": "undo",
      "entity": "OS&H",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610818891
    },
    {
      "type": "lay_tile",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 540,
      "created_at": 1610818900,
      "hex": "C15",
      "tile": "14-3",
      "rotation": 0
    },
    {
      "type": "place_token",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 541,
      "created_at": 1610818902,
      "city": "14-3-0",
      "slot": 1
    },
    {
      "type": "buy_train",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 542,
      "created_at": 1610818911,
      "train": "3+D-2",
      "price": 350,
      "variant": "3+D"
    },
    {
      "type": "buy_train",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 543,
      "created_at": 1610818915,
      "train": "3+D-3",
      "price": 350,
      "variant": "3+D"
    },
    {
      "type": "pass",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 544,
      "created_at": 1610818919
    },
    {
      "type": "pass",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 545,
      "created_at": 1610818922
    },
    {
      "type": "lay_tile",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 546,
      "created_at": 1610818947,
      "hex": "F20",
      "tile": "14-4",
      "rotation": 1
    },
    {
      "type": "place_token",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 547,
      "created_at": 1610818948,
      "city": "14-4-0",
      "slot": 1
    },
    {
      "type": "run_routes",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 548,
      "created_at": 1610818974,
      "routes": [
        {
          "train": "3-8",
          "connections": [
            [
              "G23",
              "F22",
              "F20"
            ]
          ],
          "hexes": [
            "F20",
            "G23"
          ],
          "revenue": 90,
          "revenue_str": "F20-G23"
        },
        {
          "train": "5-0",
          "connections": [
            [
              "G21",
              "F20"
            ],
            [
              "G21",
              "G23"
            ]
          ],
          "hexes": [
            "F20",
            "G21",
            "G23"
          ],
          "revenue": 100,
          "revenue_str": "F20-G21-G23"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 549,
      "created_at": 1610818981,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 550,
      "created_at": 1610818987
    },
    {
      "type": "pass",
      "entity": "NYH",
      "entity_type": "corporation",
      "id": 551,
      "created_at": 1610818989
    },
    {
      "type": "lay_tile",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 552,
      "created_at": 1610819005,
      "hex": "F24",
      "tile": "56-0",
      "rotation": 0
    },
    {
      "type": "run_routes",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 553,
      "created_at": 1610819014,
      "routes": [
        {
          "train": "5-3",
          "connections": [
            [
              "F24",
              "G23"
            ],
            [
              "E23",
              "F24"
            ]
          ],
          "hexes": [
            "G23",
            "F24",
            "E23"
          ],
          "revenue": 90,
          "revenue_str": "G23-F24-E23"
        }
      ]
    },
    {
      "type": "dividend",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 554,
      "created_at": 1610819016,
      "kind": "payout"
    },
    {
      "type": "pass",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 555,
      "created_at": 1610819022
    },
    {
      "type": "pass",
      "entity": "NYC",
      "entity_type": "corporation",
      "id": 556,
      "created_at": 1610819024
    },
    {
      "type": "par",
      "entity": 4267,
      "entity_type": "player",
      "id": 557,
      "created_at": 1610819286,
      "corporation": "WAB",
      "share_price": "120,1,1"
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 558,
      "created_at": 1610819368
    },
    {
      "type": "choose",
      "entity": 5518,
      "entity_type": "player",
      "id": 559,
      "created_at": 1610819389,
      "choice": "NKP"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 560,
      "created_at": 1610819394,
      "message": "I hate it when I want to have priority, but then I dont want to make a decision\n"
    },
    {
      "type": "merge",
      "entity": "NKP",
      "entity_type": "corporation",
      "id": 561,
      "created_at": 1610819395,
      "corporation": "NYH"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 562,
      "created_at": 1610819512,
      "message": "pass until our cash is exhausted, then buy, then pass last. then you won't have priority\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 563,
      "created_at": 1610819578,
      "message": "I don't get what's going on right now\n"
    },
    {
      "type": "choose",
      "entity": 4267,
      "entity_type": "player",
      "id": 564,
      "created_at": 1610819590,
      "choice": "Exchange"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 565,
      "created_at": 1610819595,
      "message": "Raymong has a share\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 566,
      "created_at": 1610819607,
      "message": "ah\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 567,
      "created_at": 1610819611,
      "message": "odd share\n"
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 568,
      "created_at": 1610819636
    },
    {
      "type": "par",
      "entity": 2843,
      "entity_type": "player",
      "id": 569,
      "created_at": 1610819708,
      "corporation": "B&M",
      "share_price": "105,3,2"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 570,
      "created_at": 1610819719
    },
    {
      "type": "choose",
      "entity": 4267,
      "entity_type": "player",
      "id": 571,
      "created_at": 1610819743,
      "choice": "B&O"
    },
    {
      "type": "merge",
      "entity": "B&O",
      "entity_type": "corporation",
      "id": 572,
      "created_at": 1610819748,
      "corporation": "NYC"
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 573,
      "created_at": 1610819793
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 574,
      "created_at": 1610819807,
      "shares": [
        "NKP-NYH_6"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 575,
      "created_at": 1610819827
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 576,
      "created_at": 1610819837,
      "shares": [
        "B&M_1"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 577,
      "created_at": 1610819839
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 578,
      "created_at": 1610819892,
      "shares": [
        "WAB_1"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 579,
      "created_at": 1610819895
    },
    {
      "type": "buy_shares",
      "entity": "M&H",
      "entity_type": "company",
      "id": 580,
      "created_at": 1610819943,
      "shares": [
        "NKP-NYH_7"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 581,
      "created_at": 1610819947
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 582,
      "created_at": 1610819960,
      "shares": [
        "B&M_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 583,
      "created_at": 1610819963
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 584,
      "created_at": 1610819977,
      "shares": [
        "WAB_2"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 585,
      "created_at": 1610819980
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 586,
      "created_at": 1610820058,
      "shares": [
        "B&O-NYC_6"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 587,
      "created_at": 1610820065
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 588,
      "created_at": 1610820080,
      "shares": [
        "B&M_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 589,
      "created_at": 1610820083
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 590,
      "created_at": 1610820091,
      "shares": [
        "WAB_3"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 591,
      "created_at": 1610820093
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 592,
      "created_at": 1610820105,
      "shares": [
        "MC-PRR_7"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 593,
      "created_at": 1610820121
    },
    {
      "type": "buy_shares",
      "entity": 2843,
      "entity_type": "player",
      "id": 594,
      "created_at": 1610820129,
      "shares": [
        "B&M_4"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 595,
      "created_at": 1610820132
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 596,
      "created_at": 1610820133,
      "message": "what;s the ipo reserved share?\n"
    },
    {
      "type": "buy_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 597,
      "created_at": 1610820173,
      "shares": [
        "WAB_4"
      ],
      "percent": 10
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 598,
      "created_at": 1610820174,
      "message": "when you merge, the president has to donate a 10% share in company\n"
    },
    {
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "id": 599,
      "created_at": 1610820177
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 600,
      "created_at": 1610820189,
      "message": "it pays to the company treasury\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 601,
      "created_at": 1610820193,
      "message": "cant buy it- just sits there and pays in and prevents floating\n"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 602,
      "created_at": 1610820201,
      "message": "ahh\n"
    },
    {
      "type": "buy_shares",
      "entity": 5518,
      "entity_type": "player",
      "id": 603,
      "created_at": 1610820251,
      "shares": [
        "B&M_5"
      ],
      "percent": 10
    },
    {
      "type": "pass",
      "entity": 5518,
      "entity_type": "player",
      "id": 604,
      "created_at": 1610820253
    },
    {
      "type": "choose",
      "entity": 2843,
      "entity_type": "player",
      "id": 605,
      "created_at": 1610820272,
      "choice": "OS&H"
    },
    {
      "id": 606,
      "type": "merge",
      "entity": "OS&H",
      "corporation": "NW",
      "entity_type": "corporation",
      "user": 2843,
      "created_at": 1610820277
    },
    {
      "id": 607,
      "type": "choose",
      "choice": "Exchange",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610820289
    },
    {
      "id": 608,
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610820297
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 609,
      "created_at": 1610820359,
      "message": "where is my 115?\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 610,
      "created_at": 1610820367,
      "message": "im still at 37 in cash\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 611,
      "created_at": 1610820376,
      "message": "err, 36\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 612,
      "created_at": 1610820409,
      "message": "thats a bug\n"
    },
    {
      "id": 613,
      "type": "undo",
      "entity": 4267,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610820444
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 614,
      "created_at": 1610820449,
      "message": "yeah\n"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 615,
      "created_at": 1610820478,
      "message": "undo\n"
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 616,
      "created_at": 1610820490,
      "message": "?\n"
    },
    {
      "id": 617,
      "type": "undo",
      "entity": 2843,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610820523
    },
    {
      "id": 618,
      "type": "redo",
      "entity": 5518,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610820527
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 619,
      "created_at": 1610820532,
      "message": "I'm trying\n"
    },
    {
      "id": 620,
      "type": "undo",
      "entity": 2843,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610820579
    },
    {
      "id": 621,
      "type": "choose",
      "choice": "Exchange",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610820598
    },
    {
      "id": 622,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 2843,
      "created_at": 1610820602
    },
    {
      "id": 623,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610820615
    },
    {
      "type": "merge",
      "entity": "OS&H",
      "entity_type": "corporation",
      "id": 624,
      "created_at": 1610820643,
      "corporation": "NW"
    },
    {
      "id": 625,
      "type": "choose",
      "choice": "Sell",
      "entity": 5518,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610820665
    },
    {
      "id": 626,
      "type": "undo",
      "entity": 2843,
      "entity_type": "player",
      "user": 5518,
      "created_at": 1610820672
    },
    {
      "type": "choose",
      "entity": 5518,
      "entity_type": "player",
      "id": 627,
      "created_at": 1610820674,
      "choice": "Exchange"
    },
    {
      "type": "pass",
      "entity": 2843,
      "entity_type": "player",
      "id": 628,
      "created_at": 1610820677
    },
    {
      "type": "message",
      "entity": 5518,
      "entity_type": "player",
      "id": 629,
      "created_at": 1610820684,
      "message": "looks like nothing we can do\n"
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 630,
      "created_at": 1610820689,
      "message": "Yup, thats a bug\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 631,
      "created_at": 1610820793,
      "message": "ok- we can move on\n"
    },
    {
      "type": "message",
      "entity": 4267,
      "entity_type": "player",
      "id": 632,
      "created_at": 1610820808,
      "message": "just remember this if I lose by exactly 115\n"
    },
    {
      "id": 633,
      "type": "pass",
      "entity": 4267,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610820813
    },
    {
      "id": 634,
      "type": "undo",
      "entity": 5518,
      "entity_type": "player",
      "user": 4267,
      "created_at": 1610820820
    },
    {
      "type": "message",
      "entity": 2843,
      "entity_type": "player",
      "id": 635,
      "created_at": 1610820834,
      "message": "I'm filing an issue now\n"
    },
    {
      "type": "sell_shares",
      "entity": 4267,
      "entity_type": "player",
      "id": 636,
      "created_at": 1610820837,
      "shares": [
        "NKP-NYH_5"
      ],
      "percent": 10
    }
  ],
  "loaded": true,
  "created_at": 1610806037,
  "updated_at": 1610820837
}



````

## 4. Crash on the turn ballista

vcmi/vcmi#5848

````text
A strange crash. On the turn of ballista begin to aim the arrow at the wyverns, tail and up, in a circular motion. An crash occurs.

https://youtu.be/faJ8TCTwEOQ

save [CRASHBallista.zip](https://github.com/user-attachments/files/20884801/CRASHBallista.zip)
mods: Hota, vcmi extras



(may be related https://github.com/vcmi/vcmi/issues/5831 I noticed that there is some kind of crash related to the AI battle)
````

## 5. Mini window &#x27;view person at work&#x27; doesn&#x27;t work anymore

corsixth/corsixth#846

````text
Selecting a staff member doesn't show them working in the staff info dialog, anymore 
It shows a different place, also there is an artifact under the dialog.

![bildschirmfoto von 2015-08-01 11 25 11](https://cloud.githubusercontent.com/assets/4523264/9021405/f08b7c3e-3840-11e5-956e-963bbbf07b03.png)

And the 'view person at work' window within the staff management is black

![bildschirmfoto von 2015-08-01 11 29 22](https://cloud.githubusercontent.com/assets/4523264/9021406/f4e72dbe-3840-11e5-918d-df8a62ba1b1f.png)

CorsixTH trunk ee23df1fb7ae5a0842854f3aea7a2cddb8e3a711 / Lua 5.1 / Debian Jessie 64 bit & 32 bit

````

## 6. Bugs in Feather, the Redeemed

magefree/mage#13227

````text
While working on implementing Gandalf of the Secret Fire, I've found a few problems with Feather, the Redeemed.
I've made a pull request ( #13226) to propose a fix. I'll detail the problems here ; please let me know if this isn't the right way to do this.

Some of these problems also affect Lilah, Undefeated Slingshot, which was implemented based on Feather.

Problems :
1. Feather's replacement effect never checks if the spell changing zone is the same that triggered its ability. This leads to the following bug
a. cast an instant or sorcery on any creature you control with Feather on the battlefield
b. let the ability resolve
c. before the instant/sorcery resolves, any new instant or sorcery you cast will trigger the replacement effect, be exiled and sent back to your hand at eot, which it clearly shouldn't. 

2. Feather only checks that the spell is an instant or sorcery in the replacement effect, not in the triggered ability. This means that casting say Rancor one of your creatures with Feather present will trigger Feather. The replacement effect will not apply, but the ability should nonetheless not trigger.

3. Feather's effect seems to last forever, even after it has exiled and bounced the original spell. It never applies again, but that means a whole lot of tests are happening needlessly.

I have tried to fixed these issues in the pull request referenced above ; please advise if the fix isn't correct.

````

## 7. Game settings window, the option &quot;world: use unique artifacts for resource affecting&quot; does not work

ihhub/fheroes2#2337

````text
This option does not currently work.

This option should affects the bonus of the artifacts related to the generation of resources (Gold, Wood, Ore, Mercury, Crystal, Sulfur and Gems).

When the option is activated, the bonus of these artifacts should only be counted once when there is several times the same artifact in the inventory of the same hero:
- Endless Purse of Gold
- Endless Bag of Gold
- Endless Sack of Gold
- Endless Cord of Wood
- Endless Cart of Ore
- Endless Vial of Mercury
- Endless Pouch of Crystal
- Endless Pouch of Sulfur
- Endless Pouch of Gems
````

## 8. Restore ability to rotate slab/stairs textures

luanti-org/minetest_game#2216

````text
I would like to invite you to look at this nicely decorative wooden floor:
![tile_before](https://user-images.githubusercontent.com/7035183/45823005-a0bb6080-bce4-11e8-85df-957be9d05c37.png)

It took less than five minutes to make, but I think we can agree that it is somewhat interesting, especially when compared to the alternative:

![tile_after](https://user-images.githubusercontent.com/7035183/45823052-b6c92100-bce4-11e8-9ab9-f80b70083c53.png)

#1935 was merged back in November 2017, but I assume has not really been playtested much because it's not in stable. The idea - prevent upsidedown stairs looking so weird - is great. The problem is that it changes the nicely decorative flooring above into the rather more plain and boring non-decorative version when you update an existing world to current dev version of MTG.

Personally I find this kind of breakage of existing builds, and removal of creative potential, completely unacceptable.

 I don't believe enough consideration was given before merging and I would like this reverted, or some adjustment made so that this change in behaviour is optional, not default.
````

## 9. Castle screen, incorrect resource gift text

ihhub/fheroes2#9543

````text
### Preliminary checks

- [x] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [x] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

There's a weirdly looking formula in the resource gift window in marketplace:

![Image](https://github.com/user-attachments/assets/7d833912-dcd5-4159-baab-960e8e13e597)

### Save file

None.

### Additional info

_No response_
````

## 10. Adventure map, path changes each time hero moves one cell

ihhub/fheroes2#4838

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

Path is constantly changes, when hero moves. Right during movement.
![image](https://user-images.githubusercontent.com/55348946/147371596-76a66473-dcb6-4fe1-a78d-1954a1f8c5ce.png)
![image](https://user-images.githubusercontent.com/55348946/147371637-7ce21e58-e3e1-410b-a307-1ff4b2fde14c.png)
![image](https://user-images.githubusercontent.com/55348946/147371666-2426f060-1e64-40a9-8f55-3f80f6ad8c1e.png)



### Save file

[Path.zip](https://github.com/ihhub/fheroes2/files/7775105/Path.zip)


### Additional info

_No response_
````

## 11. NPC/Medibot exceptions

space-wizards/space-station-14#22604

````text
From grafan:
```
System.Collections.Generic.KeyNotFoundException: The given key 'Dead' was not present in the dictionary.
   at Content.Server.NPC.HTN.PrimitiveTasks.Operators.Specific.MedibotInjectOperator.Update(NPCBlackboard blackboard, Single frameTime) in /home/runner/work/space-station-14/space-station-14/Content.Server/NPC/HTN/PrimitiveTasks/Operators/Specific/MedibotInjectOperator.cs:line 50
   at Content.Server.NPC.HTN.HTNSystem.Update(HTNComponent component, Single frameTime) in /home/runner/work/space-station-14/space-station-14/Content.Server/NPC/HTN/HTNSystem.cs:line 335
   at Content.Server.NPC.HTN.HTNSystem.UpdateNPC(Int32& count, Int32 maxUpdates, Single frameTime) in /home/runner/work/space-station-14/space-station-14/Content.Server/NPC/HTN/HTNSystem.cs:line 247
   at Robust.Shared.GameObjects.EntitySystemManager.TickUpdate(Single frameTime, Boolean noPredictions) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Shared/GameObjects/EntitySystemManager.cs:line 306
 Catcher=entsys Sawmill=runtime
```
````

## 12. Flagship on load screen can mismatch with active flagship

endless-sky/endless-sky#5637

````text
**Describe the bug**
The top ship in the player's fleet will always be the ship shown on the load panel, even if your active flagship is lower on the list.

**To Reproduce**
1. Have a fleet of multiple ships
2. Have another ship hold position outside of the system and land, or land and park another ship
3. Move said ship above your active flagship
4. Observe the active ship change when clicking on "Load/Save..." or "Back to Menu"

**Expected behavior**
The displayed ship will be your active flagship on both panels.

**Screenshots**
![image](https://user-images.githubusercontent.com/4471575/104705466-8db3d200-56df-11eb-85c0-effad816d9ef.png)

**System (please complete the following information):**
 - OS: Windows 10
 - Game Source: Self-compiled
 - Version: 6de8d68

**Link to save file**
[Test Pilot.txt](https://github.com/endless-sky/endless-sky/files/5819464/Test.Pilot.txt)

````

## 13. Dead players sometimes not considered dead

lykoss/lykos#256

````text
Happened in maelstrom. Mayor with desperation totem was lynched, causing totem to fire and killing player A. Player A was assassin targeting player B, and thus caused B to die as well. The mayor was then revealed as mayor, A and B were not devoiced but were also considered dead (could use !revealroles, were not given a role pm at night). At the end of night, they were devoiced and joined to deadchat.
````

## 14. Room in army is made for Joining creatures but not for dwelling creatures

vcmi/vcmi#1986

````text
**Describe the bug**
Even if all 7 slots are full, If possible stacks will be combined to make room for joining creatures but not from dwelling creatures.

**To Reproduce**
Steps to reproduce the behavior:
1. Start attached map

[A Joining Creatures test.zip](https://github.com/vcmi/vcmi/files/11235695/A.Joining.Creatures.test.zip)

````

## 15. Army bar: Don&#x27;t show text about redistributing troops when there is only one unit in the troop

ihhub/fheroes2#5358

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Other

### Describe the bug

If there is only one unit in a troop the message shouldn't say that you can right-click to redistribute since you can't.

It should only say `"Move the %{name}"`

![image](https://user-images.githubusercontent.com/12501091/166262511-59323d19-0b89-451c-b310-e9197daebfeb.png)

This is found in two places in the army_bar.cpp for the castle garrison and hero army.

Also "the" should be added for the plural case as seen in the picture above.



### Save file

Just open any castle/hero army.

### Additional info

_No response_
````

## 16. [18NY] game didn’t allow a company action during SR

tobymao/18xx#6574

````text
https://18xx.games/game/63389?action=370

If you look at the log, it says “Eonthar has no valid actions and passes” before the end of the SR, but D&H could have issued or redeemed a share, which this player wanted to do. 
````

## 17. Team set in PlayerReference is ignored for unplayable players

openra/openra#8623

````text
E.g. https://github.com/abcdefg30/OpenRA/commit/6b393c3cceee8d136b4cd729ecf8c2626f120226 gives me
![lockteam](https://cloud.githubusercontent.com/assets/7704140/8486156/1617f32e-2103-11e5-95b6-b0b647af21d3.png)
(I forced the Soviets team to `2` actually.)

````

## 18. Incorrect allies set in games with &#x27;Defeat the other side&#x27; victory condition (Voyage Home #4 and some other maps affected)

ihhub/fheroes2#5001

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

Steps to reproduce:
a) Start Voyage Home, map 4: load 'vh2_Complete.savc' from zip, select map 4.
b) You can see Red player map is visible to you

1) I met this issue during playing Voyage Home map 4. In FHeroes2 Red computer player acts as an ally to a human player. You can see that instantly as all their territory is opened to you, then they fight on your side.
![image](https://user-images.githubusercontent.com/58906397/153488849-8d952dd4-8212-47d4-a878-0f5ac3c896e7.png)
This felt wrong and broken. I cannot check it in the original game, since it has a different save file format (if I understand correctly). But according to the walk through below, Red indeed should be your enemy.
https://mightandmagic.fandom.com/wiki/Blood_is_Thicker

2) Allies with 'Defeat the other side' victory conditions are determined by wins1 field in the map structure (offset 0x20..0x21) and FHeroes2 handles it and treats it like index of a color which starts the second union, i.e. all the colors <wins1 - side1, all colors >= wins1 - side2. This seems incorrect and correct meaning is a number of players in side1. This often does not make a difference, but when players colors are assigned not in sequential order this does make a difference.

It can be proven in OG Map Editor on 'Last Hope' map for example. There are three players: Blue, Orange and Purple. Original union settings is Blue vs Orange+Purple, wins1=1. However after setting in Map Editor specs Blue+Orange vs Purple it can be seen that wins1 is set to 2. So it proves that wins1 is a number of players in side1.
![image](https://user-images.githubusercontent.com/58906397/153491728-5797ae73-336b-4259-bbe6-73aae142149c.png)
![image](https://user-images.githubusercontent.com/58906397/153492219-dbf5b50f-61b1-4bc6-b98f-1ca3135f7aae.png)

3) So I think it should be fixed in Maps::FileInfo::ReadMP2:
![image](https://user-images.githubusercontent.com/58906397/153495048-5df6a94d-35cf-4dce-9cd0-7533bae9a236.png)

With that change Voyage Home map 4 does not have Red played allied with a human:
![image](https://user-images.githubusercontent.com/58906397/153494025-d8de1d97-f047-4c9b-af4f-38688c200595.png)




### Save file

[saves.zip](https://github.com/ihhub/fheroes2/files/8044179/saves.zip)


### Additional info

_No response_
````

## 19. 1817 Loan Payoff Bug

tobymao/18xx#9166

````text
![1817 Bug - game id](https://user-images.githubusercontent.com/98102209/236697265-02b15133-bb3f-4131-b29f-be31c2530880.png)
![1817 Bug - before paying off one loan](https://user-images.githubusercontent.com/98102209/236697269-b6ea9ddb-d48b-4474-8dcf-28bcff2ff0d3.png)
![1817 Bug - after paying off one loan - loans down to 8 not 9](https://user-images.githubusercontent.com/98102209/236697274-440c5df1-c85e-4453-9a6e-0a1bbfbdbfb2.png)

I found a bug.  In the game above, I pay off one loan, but my loan number drops from 10 to 8.  I have included screen shots.
````

## 20. Analysis: unexpected wikibook API answer on 1.d4 a5

lichess-org/lila#13877

````text
<img width="1073" alt="image" src="https://github.com/lichess-org/lila/assets/56031107/dea20940-a4a3-43e4-9000-6c22a763bf32">
Reported on the forums: https://lichess.org/forum/lichess-feedback/error-in-analysis

My guess is it’s because the page exists but has no text. Gracious failure like page does not exist or only display the title would be better in that case.
````

## 21. Wrong Lara rotation during UW twist

lostartefacts/trx#1242

````text
During the underwater roll/twist animation, Lara appears to be rotated at a random angle for a single frame in the second half of the animation.

@lahm86 can you please check? This is more evident with 60 fps and turbo=-2 in the latest develop.
````

## 22. Pressing back button in main menu submenu fails while animating

revolutionary-games/thrive#2655

````text
If the animation is still playing for a main menu sub menu, and the user manages to press the "back" button, it fails to do anything. It seems that somehow the animation playing prevents the submenu from being exited before it is complete.

After my PR adding a second GUI sound player, you can also hear the button press sound activating confirming the fact that I managed to press the button, but still after the animation finishes a fraction of a second later, I'm left looking at the submenu:
![2021-10-15_15 24 25 6086](https://user-images.githubusercontent.com/3796411/137486280-5da12fef-65c9-48b5-935e-2ed4a2541ef8.png)


````

## 23. On the patch map screen clicking below the background plays the invalid place sound

revolutionary-games/thrive#1704

````text
It shouldn't play that sound when clicked there.
````

## 24. Utility attach points are destroyed when their attachment is acided

rmc-14/rmc-14#7910

````text
## Description
When one of these attachments is acided by a xeno, it will also melt the utility attach point permanently removing it from play
````

## 25. Hercules can still pick up unit when disarmed

zerok-rts/zero-k#3949

````text
http://zero-k.info/Battles/Detail/901986?

about 3-4 mins in firepluk comm nap
````

## 26. Flagellum animation doesn&#x27;t play anymore

revolutionary-games/thrive#2959

````text
Looks like in the latest version the flagellum animation does not play for some reason. This is a pretty bad regression and should be investigated ASAP and fixed.
Might have something to do with new Godot import settings or animation naming.
````

## 27. File Options window, this window is not centered vertically in the screen

ihhub/fheroes2#5509

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2, the File Options window is not centered vertically in the screen.

In fheroes2:

![Windows on load 01](https://user-images.githubusercontent.com/43583994/172167830-3c245d6c-ad12-4f1f-9f91-81adf73a79ba.png)

### Save file

Not needed.

### Additional info

_No response_
````

## 28. Table climbing leads to the player getting stuck

space-wizards/space-station-14#1802

````text

````

## 29. Pressing the restart key crashes the game when spectating

quaver/quaver#1252

````text
You shouldn't be allowed to press the restart key while spectating
````

## 30. Extended telescopic shield glows in the dark

space-wizards/space-station-14#20199

````text
## Description
It's fine when it isn't extended

**Screenshots**
![baetdr](https://github.com/space-wizards/space-station-14/assets/104418166/cd674f18-2e5d-4e6b-aa71-a3a19f69d56c)

````

## 31. puzzle accepts wrong move and no following move

lichess-org/lila#4617

````text
https://lichess.org/training/82169 *(now disabled)*

> not sure whats going on here, the incorrect Rh1 is shown as correct

On mobile, but same on website:
https://imgur.com/a/LQhTSUQ
````

## 32. globalThis.freeSpells should be player.freeSpells

jdoleary/spellmasons#109

````text
A player reported losing Summon spells.  I think this is because freeSpells is stored on the global and not on the player so it doesn't get serialized.

I need to reproduce this, but this may be why.
````

## 33. Can&#x27;t steal weapon from enemy on roof

ja2-stracciatella/ja2-stracciatella#1676

````text
vanilla, master branch 0.20
This bug is from vanilla game
When on roof, you can't steal enemy weapon - it always returns nothing

Another bug was introduced somehow by one of latest commits - now if you fail to steal weapon, you get text like:
IGOR FAILED TO STEAL IGOR - the placeholder for weapon name always contains character name
````

## 34. Game, multiplayer, difference in functioning compared to the original game

ihhub/fheroes2#4721

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2 currently, for the multiplayer, it doesn't work like in the original game.

After switching the position of the Blue player and the Orange player.
In the original game, the order of play of the player colors has been changed and the Orange player plays first and at the Orange player position on the adventure map.

https://user-images.githubusercontent.com/43583994/143768348-09041b73-18d7-4f97-a930-b7938ba295b3.mp4

Note that the player color graphic is not updated in the original game when the player swaps the Blue and Orange players.
I think it should be in fheroes2.

In fheroes2, this is not the case.

https://user-images.githubusercontent.com/43583994/143768416-1d24e872-d62c-439c-8f5f-d42dbfd5d950.mp4

### Save file

Not needed.

### Additional info

_No response_
````

## 35. Make the deck creator able to add cards from the neutral class

lunartides/hearthstone.js#47

````text
The deck creator seems to have a hard time adding cards from the neutral class to the deck.
````

## 36. 18EU prompted to choose city incorrectly

tobymao/18xx#7414

````text
https://18xx.games/game/73809?action=604

ChrisShaffer just bought 10% of GSR and is now being prompted to select a city for its home token. However, GSR already has tokens and trains. Also, when ChrisShaffer chooses any hex, this error pops up:

<img width="733" alt="Screen Shot 2022-03-07 at 22 18 45" src="https://user-images.githubusercontent.com/8732435/157178514-fb3be1e4-5c51-422b-9fd3-ccb0ece26d24.png">
 
````

## 37. Options Menu Shouldn&#x27;t Be Visible on Android

movingblocks/destinationsol#490

````text
### Description
The Options menu is visible on the Android build and shows settings that aren't applicable, such as changing resolution and input. Previously this menu had been hidden on Android, but there are additional items that may be useful to change on Android, e.g. map scroll speed.

### Log details and game version
version 2.0.0

### Computer details
Android Emulator - API 28
````

## 38. OpenRA - crashes with exception: &quot;some units like &quot;vislrg&quot; and &quot;vissml&quot; doesnt have sequences like &quot;die2&quot; and &quot;die3&quot;

openra/openra#6476

````text
Tiberian Sun Mod at Version {DEV_VERSION}

<pre>Operating System: Linux (Unix 3.16.2.0)
Runtime Version: Mono 3.2.8 (Debian 3.2.8+dfsg-4ubuntu1) CLR 4.0.30319.17020
Exception of type `System.InvalidOperationException`: Unit `vislrg` does not have a sequence named `die2`
  at OpenRA.Graphics.SequenceProvider.GetSequence (System.String unitName, System.String sequenceName) [0x00000] in <filename unknown>:0 
  at OpenRA.Graphics.Animation.PlayThen (System.String sequenceName, System.Action after) [0x00000] in <filename unknown>:0 
  at OpenRA.Mods.RA.Effects.Corpse..ctor (OpenRA.World world, WPos pos, System.String image, System.String sequence, System.String paletteName) [0x00000] in <filename unknown>:0 
  at OpenRA.Mods.RA.Render.WithDeathAnimation+<SpawnDeathAnimation>c__AnonStorey0.<>m__0 (OpenRA.World w) [0x00000] in <filename unknown>:0 
  at OpenRA.World.Tick () [0x00000] in <filename unknown>:0 
  at OpenRA.Game.InnerLogicTick (OpenRA.Network.OrderManager orderManager) [0x00000] in <filename unknown>:0 
  at OpenRA.Game.LogicTick () [0x00000] in <filename unknown>:0 
  at OpenRA.Game.Loop () [0x00000] in <filename unknown>:0 
  at OpenRA.Game.Run () [0x00000] in <filename unknown>:0 
  at OpenRA.Program.Run (System.String[] args) [0x00000] in <filename unknown>:0 
  at OpenRA.Program.Main (System.String[] args) [0x00000] in <filename unknown>:0 
</pre>


````

## 39. Bagel atmos device issues.

space-wizards/space-station-14#33488

````text
**Screenshots**
![bagel chef freezer](https://github.com/user-attachments/assets/6783a6d5-6912-428c-b64e-b688dbda9cc9)
Nothing in chef freezer is connected.

![bagel ex checkpoint](https://github.com/user-attachments/assets/79b55b3a-1a16-440a-af44-72f899242cc4)
Area where sec checkpoint used to be have not connected stuff too.

![bagel QM cargo front](https://github.com/user-attachments/assets/058936df-8f70-461f-94a2-b1e6da34ac70)
QM and cargo front desk both have not connected atmos.

![bagel janitor](https://github.com/user-attachments/assets/9d7dda35-d829-40be-943b-0493be176d24)
Janitor as well.

![bagel sec front sec south half](https://github.com/user-attachments/assets/f7be8c26-7192-4a34-af2c-021408700537)
> South sec of main area and sec entrance too.

Should be done now in sec changes PR.

![bagel CE](https://github.com/user-attachments/assets/fd28eda6-c414-40d5-842d-16bbe2285b19)
None of CE rooms have any atmos device connections... No atmos in head of atmos? :(




````

## 40. Arrow on upcoming train list not robust with optional trains

tobymao/18xx#5120

````text
Because the code in the GameInfo UI uses train.name instead of train.sym, games that implement optional train variants will not always display the current train arrow. This happens when the first train in a type has been bought as one of the options.

For example in this 1846 game (https://18xx.games/game/38510?action=74), the first phase II train was bought as a 3/5. The arrow disappears:
![missing_arrow](https://user-images.githubusercontent.com/8494213/115911615-8a8d5800-a42b-11eb-91f8-4bd3b4c4634f.png)

It should look like this:
![arrow](https://user-images.githubusercontent.com/8494213/115911788-c0324100-a42b-11eb-8bad-76ce8cc93490.png)

````

## 41. Trees do not render correctly

theassemblyarmada/thyme#863

````text
Trees do not render correctly. Polygons stretch through world. Moving camera over trees will reduce FPS from 400 to 40 on my machine.

Tested with RelWithDebInfo. On map Manic Aggression (4).

![shot_20230218_004045_4](https://user-images.githubusercontent.com/4720891/219817428-17360a8c-a4b3-49d0-abd6-af599f84f6e1.jpg)

![shot_20230218_004159_5](https://user-images.githubusercontent.com/4720891/219817434-7564b437-33f7-4c37-9e0d-bda030e03dfe.jpg)

````

## 42. [BUG] Daily Deal Menu Not Showing Correct Inventory Count on Leaf Stone (And Possibly More)

pokeclicker/pokeclicker#2801

````text
**Info**
 - OS: Windows 10
 - Browser Chrome
 - Version 0.9.10

**Description:**
When looking at the daily deals available in the underground, the number that represents my inventory when looking at leaf stones for today says I have 0, but I actually have 83. All other items I have seen are normal.

**Steps to Reproduce:**
1. Go to Underground
2. Click on Daily Deals
3. See error
(I do not know if this is a problem for anyone else, I have not seen other posts about it, and this is the first time it has happened to me, right after this update came out)

**Screenshots:**
![Deals](https://user-images.githubusercontent.com/76641261/182525676-08a5597f-50cd-4af2-8ecb-474bc9b19f6b.PNG)

![Items](https://user-images.githubusercontent.com/76641261/182525711-4f94e7fb-c758-40d7-9edf-55790d9882f9.PNG)

(My SS are looking odd on my end before posting, so I apologize if they do not appear)

**Additional Information:**
Doing the trade (this specific trade being 3 Sky Plates for 1 Leaf Stone) does not change the Inventory number, it remains 0. I have not been able to check if it happens to other evolution items as there is not a trade for them today.

````

## 43. Cells don&#x27;t despawn properly on patch change

revolutionary-games/thrive#854

````text
For some reason sometimes (or seemingly very often if you are Kinesis) the cells that should despawn on patch change don't despawn. My guess is that they are somehow missing the SpawnedComponent as `ThriveGame::playerMovedToPatch` method queues all entities with a SpawnedComponent or TimedLife component to despawn. Maybe chunk component should be added to the list as well?
````

## 44. RMG: Few empty zones are generated

vcmi/vcmi#2081

````text
Template 3SM3d
Seed: 1682627278
72x72x1
players: 2, cpus: 0
water: none, monsters: strong
red: Forge, blue: random

Mods
<img width="455" alt="Снимок экрана 2023-04-28 в 00 33 09" src="https://user-images.githubusercontent.com/9308612/234984281-7866590f-531c-4e7a-b516-548cd113e450.png">


**Did it work earlier?**
**Screenshots**
<img width="853" alt="Снимок экрана 2023-04-28 в 00 29 59" src="https://user-images.githubusercontent.com/9308612/234983676-77e0fc07-120f-4315-93b3-68399048272b.png">


**Version**
 - OS: [e.g. Windows, macOS Intel, macOS ARM, Android, Linux, iOS]
 - Version: VCMI-1.2

**Additional context**
[rmg_issue_save.zip](https://github.com/vcmi/vcmi/files/11347657/rmg_issue_save.zip)

````

## 45. Save file, problem when loading a save file in a different language than the currently selected language

ihhub/fheroes2#4793

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2, there is a problem when loading a save file in a different language than the currently selected language.

In fheroes2:

When loading a French language save from the game set to English, I got this Warning window which does not indicate the current language selected (English, 'en').
![Warning language window 001](https://user-images.githubusercontent.com/43583994/146237102-33a3cf1b-5ad4-4b29-a36f-fac655e13161.png)

By selecting "Deutsch", the text in the window remains in English.
The term 'de' is correctly indicated.
![Warning language window 002](https://user-images.githubusercontent.com/43583994/146237178-341f5fa0-f7e4-4128-a3e7-36350655ba0d.png)

By selecting "Polsky", everything seems to be correct, although I don't read Polish. :)
![Warning language window 003](https://user-images.githubusercontent.com/43583994/146237226-1ccb20c3-c797-40b4-8c1a-8d73fc64cea4.png)

### Save file

Here is the save file:
[Broken_Alliance_0017.zip](https://github.com/ihhub/fheroes2/files/7721590/Broken_Alliance_0017.zip)

### Additional info

_No response_
````

## 46. Incorrect character in fr.po file

ihhub/fheroes2#5503

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Linux

### Describe the bug

fr.po is the modified ASCII, but it contains [non-ASCII and non-mapped char Ç](https://github.com/ihhub/fheroes2/blob/cf315a9c7df9a2a996ece91e94b46b6979ca3899/files/lang/fr.po#L4853).
Thanks @hgdagon for finding it.

![Снимок экрана от 2022-06-05 11-51-27](https://user-images.githubusercontent.com/71143197/172043225-5f37f6d1-7cf6-4833-8aa3-55a597885682.png)

### Save file

[bug.zip](https://github.com/ihhub/fheroes2/files/8839628/bug.zip)

### Additional info

_No response_
````

## 47. Maps aren&#x27;t marked as ranked automatically

quaver/quaver#827

````text
**Describe the bug**
When a mapset is downloaded and imported its ranked status isn't updated automatically. This means that searches such as `status=ranked` don't show newly downloaded ranked maps, for example.

**Expected behavior**
The maps' ranked status should be checked and cached on import.

````

## 48. Adventure map and View World screen, wrong position of the reticule on the minimap

ihhub/fheroes2#4200

````text
### Preliminary checks

- [X] I've checked that there aren't [**other open issues**](https://github.com/ihhub/fheroes2/issues?q=is%3Aissue) on the same topic.
- [X] I've checked that this issue is reproducible on the [**latest snapshot build**](https://ihhub.github.io/fheroes2/INSTALL.html#snapshots-latest-builds).

### Platform

Windows

### Describe the bug

In fheroes2, there is a  wrong position of the reticule on the minimap.
E.g. look at the resource piles to the south of the adventure map.

In fheroes2:

![Wrong reticule position 001](https://user-images.githubusercontent.com/43583994/132984944-739c550d-01ff-4e63-8a0b-966d683cfc68.png)

![Wrong reticule position 002](https://user-images.githubusercontent.com/43583994/132984945-557b2c1d-8334-46f9-b4a6-6ebd5365320a.png)

**Edit 2021/12/11.**

Rephrased for a better description:
The reticle area of the minimap does not match what is displayed on the representation of the adventure map.

In fheroes2:

![Reticule to map 01](https://user-images.githubusercontent.com/43583994/145679544-13da8bda-0023-4ba7-adc8-b4872a94a40d.png)

### Save file

Here is the save file (0.9.7 4180):
[Position reticule view world 0.zip](https://github.com/ihhub/fheroes2/files/7149463/Position.reticule.view.world.0.zip)

### Additional info

_No response_
````

## 49. Allied &amp; Soviet&#x27;s Super-weapons shouldn&#x27;t be able to capture.

cookgreen/yuris-revenge#157

````text
Allied & Soviet's Super-weapons shouldn't be able to capture.

Maybe we could modify super-weapons' inherits  as `SupportBuilding`?
````

## 50. Artifact analyer exception spam

space-wizards/space-station-14#22602

````text
Unlike #21734 this was in a tick update and was spamming out errors. However the root cause might be the same?

From grafana:
```
Can't resolve "Robust.Shared.GameObjects.MetaDataComponent" on entity 97938!
   at Content.Server.Xenoarchaeology.Equipment.Systems.ArtifactAnalyzerSystem.UpdateUserInterface(EntityUid uid, AnalysisConsoleComponent component) in /home/runner/work/space-station-14/space-station-14/Content.Server/Xenoarchaeology/Equipment/Systems/ArtifactAnalyzerSystem.cs:line 217
   at Content.Server.Xenoarchaeology.Equipment.Systems.ArtifactAnalyzerSystem.Update(Single frameTime) in /home/runner/work/space-station-14/space-station-14/Content.Server/Xenoarchaeology/Equipment/Systems/ArtifactAnalyzerSystem.cs:line 83
   at Robust.Shared.GameObjects.EntitySystemManager.TickUpdate(Single frameTime, Boolean noPredictions) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Shared/GameObjects/EntitySystemManager.cs:line 306
   at Robust.Shared.GameObjects.EntityManager.TickUpdate(Single frameTime, Boolean noPredictions, Histogram histogram) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Shared/GameObjects/EntityManager.cs:line 239
   at Robust.Server.GameObjects.ServerEntityManager.TickUpdate(Single frameTime, Boolean noPredictions, Histogram histogram) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Server/GameObjects/ServerEntityManager.cs:line 160
   at Robust.Server.BaseServer.Update(FrameEventArgs frameEventArgs) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Server/BaseServer.cs:line 702
   at Robust.Shared.Timing.GameLoop.Run() in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Shared/Timing/GameLoop.cs:line 235
   at Robust.Server.BaseServer.MainLoop() in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Server/BaseServer.cs:line 569
   at Robust.Server.Program.ParsedMain(CommandLineArgs args, Boolean contentStart, ServerOptions options) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Server/Program.cs:line 78
   at Robust.Server.Program.Start(String[] args, ServerOptions options, Boolean contentStart) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Server/Program.cs:line 46
   at Robust.Server.Program.Main(String[] args) in /home/runner/work/space-station-14/space-station-14/RobustToolbox/Robust.Server/Program.cs:line 25

 Sawmill=resolve
```
````
