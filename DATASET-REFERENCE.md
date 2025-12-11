# データセットリファレンス

## 概要

| 項目 | 値 |
|------|-----|
| データセット名 | NVIDIA Nemotron-Personas-Japan |
| レコード数 | 1,000,000 |
| フィールド数 | 22 |
| 形式 | Parquet（ストリーミング対応） |
| ライセンス | CC BY 4.0 |
| 言語 | 日本語 |

---

## フィールド一覧

### 識別子

| フィールド | 型 | 説明 | 例 |
|-----------|-----|------|-----|
| `uuid` | string | 一意識別子（UUID v4） | `"a1b2c3d4-e5f6-..."` |

### 人口統計

| フィールド | 型 | 説明 | 値/範囲 |
|-----------|-----|------|---------|
| `age` | int | 年齢 | 18歳以上（国勢調査分布に準拠） |
| `sex` | string | 性別 | `"男"`, `"女"` |
| `marital_status` | string | 婚姻状況 | `"既婚"`, `"未婚"`, `"離別"`, `"死別"` |
| `education_level` | string | 学歴 | `"高校卒"`, `"大学卒 文系"`, `"大学院卒"` 等 |
| `occupation` | string | 職業 | 1,500+カテゴリ（職位含む場合あり） |

### 地理

| フィールド | 説明 | 値 |
|-----------|------|-----|
| `country` | 国 | `"日本"`（固定） |
| `region` | 地域 | 8地域（下記参照） |
| `area` | 地区 | `"東日本"`, `"西日本"` |
| `prefecture` | 都道府県 | 47都道府県（接尾辞付き） |

### ペルソナナラティブ

各フィールドは100〜300文字の記述テキスト。

| フィールド | 内容 | 用途 |
|-----------|------|------|
| `professional_persona` | 仕事スタイル、キャリアアプローチ | ペインポイント分析、B2Bコンセプト |
| `sports_persona` | スポーツ・運動・フィットネス | 健康・ウェルネス系コンセプト |
| `arts_persona` | 芸術・文化・創造的活動 | 趣味・教養系コンセプト |
| `travel_persona` | 旅行スタイル、目的地の好み | 旅行・観光系コンセプト |
| `culinary_persona` | 食の好み、料理習慣 | 食品・飲食系コンセプト |
| `persona` | 統合ペルソナ要約 | 全体像の把握 |

### コンテキスト

| フィールド | 形式 | 説明 |
|-----------|------|------|
| `cultural_background` | テキスト | 文化的背景、世代的特徴 |
| `career_goals_and_ambitions` | テキスト | キャリア目標、野心 |
| `skills_and_expertise` | テキスト | 専門スキル（記述） |
| `skills_and_expertise_list` | JSON配列 | スキルリスト |
| `hobbies_and_interests` | テキスト | 趣味・関心（記述） |
| `hobbies_and_interests_list` | JSON配列 | 趣味リスト |

---

## 地域マッピング

| 地域 | 都道府県 |
|------|---------|
| 北海道地方 | 北海道 |
| 東北地方 | 青森県, 岩手県, 宮城県, 秋田県, 山形県, 福島県 |
| 関東地方 | 茨城県, 栃木県, 群馬県, 埼玉県, 千葉県, 東京都, 神奈川県 |
| 中部地方 | 新潟県, 富山県, 石川県, 福井県, 山梨県, 長野県, 岐阜県, 静岡県, 愛知県 |
| 近畿地方 | 三重県, 滋賀県, 京都府, 大阪府, 兵庫県, 奈良県, 和歌山県 |
| 中国地方 | 鳥取県, 島根県, 岡山県, 広島県, 山口県 |
| 四国地方 | 徳島県, 香川県, 愛媛県, 高知県 |
| 九州地方 | 福岡県, 佐賀県, 長崎県, 熊本県, 大分県, 宮崎県, 鹿児島県, 沖縄県 |

---

## ユースケース別推奨フィールド

### ペインポイントリサーチ
```
uuid, age, sex, occupation, prefecture,
professional_persona, career_goals_and_ambitions, skills_and_expertise_list
```

### コンセプトテスト（食品・料理）
```
uuid, age, sex, occupation, prefecture,
culinary_persona, hobbies_and_interests_list, marital_status
```

### コンセプトテスト（健康・ウェルネス）
```
uuid, age, sex, occupation, prefecture,
sports_persona, hobbies_and_interests_list
```

### コンセプトテスト（旅行）
```
uuid, age, sex, occupation, prefecture, region,
travel_persona, marital_status
```

### コンセプトテスト（専門ツール/SaaS）
```
uuid, age, sex, occupation, prefecture,
professional_persona, skills_and_expertise_list, career_goals_and_ambitions
```

---

## JSON配列フィールドのパース

`skills_and_expertise_list`と`hobbies_and_interests_list`はJSON文字列として格納されている。

```python
import json

# パース例
skills = json.loads(persona["skills_and_expertise_list"])
# ["ケアプラン作成", "身体機能評価", "Excelデータ集計"]

hobbies = json.loads(persona["hobbies_and_interests_list"])
# ["歴史散策", "季節の花観賞", "節約料理"]
```

---

## 職業の例

データセットには1,500以上の職業カテゴリが含まれる。職位（中堅、ベテラン等）が付く場合あり。

| カテゴリ | 例 |
|---------|-----|
| 医療・介護 | 看護師, 介護福祉業 中堅, 理学療法士 |
| IT・エンジニア | システムエンジニア, Webデザイナー, データアナリスト |
| 教育 | 教師, 塾講師, 保育士 |
| 営業・事務 | 営業職, 一般事務, 経理 |
| サービス | 調理師, 美容師, 販売員 |
| 製造・建設 | 工場作業員, 建築士, 電気工事士 |
