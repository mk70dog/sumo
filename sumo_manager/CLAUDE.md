# Grand Sumo Manager の作業ルール(Claude 向け)

このフォルダは、相撲部屋経営ゲーム「Grand Sumo Manager」(旧名 Sumo Manager。単一 HTML)の置き場所です。リポジトリ直下の `index.html` は Sumo Manager の最新版へ飛ぶ入口です。`judge/`(Judge Console Hub)は別のものなので、触らないでください。

## 再開するとき
1. `docs/` の中で番号がいちばん大きい引き継ぎ資料(`SumoManager_Handoff_*_vN.md`)を読む。claude.ai のプロジェクト「sumo」にも同じ資料と `claude/00_再開手順.md` がある。
2. 最新版の本体は、このフォルダの `sumo_manager_vNN.html`(番号がいちばん大きいもの)。
3. ダルマさん(ユーザー)が「続き」と言ったら、引き継ぎ資料の「残りの作業」から再開する。

## 進め方
1. Claude が設計案を書く → ダルマさんが「実施」と返す → 実装する。
   - 画面の見た目や操作を変えるときは、必ず先に見本(`samples/` の HTML と画面の写真)をダルマさんに見せ、どれにするか決めてもらってから実装する。(2026-11-17 に決めた決まり)
2. 実装は必ず新しい版のファイルとして作る(古い版は上書きしない)。前の版の HTML に `patches/patchNN.py`(文字列置換。一致数をチェック)を当てて作る。
3. 実装後の自動テスト:
   - 40 年(240 場所)の自動プレイ(`tests/auto.js`、実態の数字は `tests/real.js`)
   - 画面 3 サイズ(iPad 横 1180×820、iPad 縦 820×1180、スマホ 390×844)でエラーと横あふれ(`tests/ui.py`、Playwright)
   - 1 つ前の版の保存データの引き継ぎ(`tests/mig.js 前の版.html 新しい版.html 前の版の保存キー`)
4. リアルさを最優先にする。実在の規則・数値は実装前に検索して確かめ、出典を引き継ぎ資料に書く。推定値は推定と明記する。
5. 実在の人物の本名は登録しない。

## 版ができたら毎回すること
1. このフォルダに置く:本体 `sumo_manager_vNN.html`、`patches/patchNN.py`、新しい元データは `data/`、引き継ぎ資料の新版は `docs/`。
   入口の飛び先を新しい版に書き換える(リポジトリ直下の `index.html` とこのフォルダの `index.html`、それぞれ 2 か所)。公開 URL は https://mk70dog.github.io/sumo/
   このフォルダの `latest.json` も新しい版に書き換える(`{"v":版の番号,"file":"sumo_manager_vNN.html","note":"ひとことの説明"}`)。ゲームの「アプリを更新」ボタンはこれを見て新しい版へ切り替える。本体の `const APPV=` も版の番号にする。
2. `main` にコミットして push する(`git push origin main`)。
3. claude.ai のプロジェクト「sumo」に引き継ぎ資料の新版を保存し、`claude/00_再開手順.md` の「最新版」の行を更新する。
4. ダルマさんに本体と引き継ぎ資料のファイルも送る。

## GitHub に上げられないとき(新しいチャットでよく起きる)
1. まず `mcp__claude-code-remote__add_repo`(owner `mk70dog`、repo `sumo`、**access は `push`**)。読むだけ(read)で追加すると push できない。
2. 「許可されない(denied)」と出たら、回り道をせず、ダルマさんに「GitHub の mk70dog/sumo を追加する許可をください」と頼んで、もう一度 add_repo する(2026-11-19 も 1 回目は拒否、2 回目で通った)。
3. clone は 1 回だけ、時間を長めに:`git clone --depth 1 https://github.com/mk70dog/sumo /home/claude/sumo`(10 分まで待つ)。そのあと `register_repo_root`。
4. push の前に `git fetch --depth=50 origin main` → `git merge-base --is-ancestor origin/main HEAD` で確かめる。ほかのチャットが先に上げていたら `git merge --ff-only origin/main`(自分の変更があれば rebase)。push は `git -c push.negotiate=true push origin HEAD:main`。
5. 429(too many concurrent)は 5 秒待って 1 回だけやり直す。413(大きすぎる)は 4 のとおり fetch してから。
6. どうしても上げられないときは、本体と資料のファイルをダルマさんに送り、何が上がっていないかを資料と返事に書く。
7. コミットの最後には、そのときの system-reminder にある署名の行を付ける。
