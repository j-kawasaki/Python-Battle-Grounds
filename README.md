# Python-Battle-Grounds

プレイヤーの動きをプログラム可能な多人数参加型見下ろしシューティングゲーム

# 遊び方

`python Client.py -ip [IPアドレス]` でサーバーに接続
ClientAction.pyに書かれた行動方針に従ってプレイヤー機が動く．
**目指せサーバーNo.1**

# プレイヤーの可能な操


# プレイヤーに与えられる情報

プレイヤーは周囲の情報を知覚できる．
知覚したデータはSense辞書としてActionClient.py内で参照できる．
参照にはデフォルトで定義されているsense関数を使うことを推奨する．
視界内の敵の情報リストが欲しい場合は`enemies = self.sense('sight', 'enemies')`とする．
知覚できるデータは以下の通りである．

## sight: 視覚に関するデータ．最も重要だが指向性が強い

- 視覚はプレイヤーの向きの+-60度のデータを得ることができる．
- この内，+-30度の範囲は中心視野として正確なデータ(敵の詳細位置，敵の向き，弾の種類など)を得る．
- 中心視野以外の範囲は周辺視野としてあいまいなデータ(ランダムノイズを含んだ敵の位置，弾の有無)を得る．


## hearing: 聴覚に関するデータ，

- 聴覚はプレイヤーの向きの+=180度のデータを得ることができる．
- 視覚情報は音源から離れるにつれてランダムノイズが含まれる．
- 聴覚が得られるデータは音発生時の一度きりである．

