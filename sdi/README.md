# SDI Animation PoC 01

最初のStatic–Dynamic Interface実験。

## 仮説

同じStatic Worldに対して、Dynamic Behaviorだけを交換できる。

```text
world.json
  Entity / Relation / Capability
          ↓
         SDI
          ↓
  orbit | pulse | attract
          ↓
       animation
```

`world.json` は静的な意味構造、`index.html` の `behaviors` は動的規則として分離している。

## 実験

`index.html` をブラウザで開き、`orbit / pulse / attract` を切り替える。同じEntity/Relationを変更せず、振る舞いだけが変化することを確認する。

## 次の検証

- behaviorを外部JSONで定義する
- capabilityに応じたbehavior選択を行う
- Event / State / TransitionをSDIに追加する
- Architecture由来のStatic Worldを投入する
