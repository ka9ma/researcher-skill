# Nemotron Researcher

NVIDIA Nemotron-Personas-Japan データセット（100万人の日本人合成ペルソナ）を活用した、Claude Desktop用ペルソナベースリサーチスキル。

## 概要

このスキルを使うと、100万人の日本人ペルソナデータを活用して以下のリサーチを高速に実行できます：

- **ペルソナ抽出**: 職業・地域・年齢等でフィルタリングしてペルソナを取得
- **ペインポイント分析**: 特定セグメントの課題・ストレスを発見
- **コンセプトテスト**: 製品/サービスの受容性を多様なペルソナで評価

従来のユーザーリサーチでは数週間かかる調査を、数分で実行できます。

## 特徴

- **100万人の日本人ペルソナ**: 国勢調査データに基づく多様なデモグラフィック
- **22のペルソナフィールド**: 職業、趣味、スキル、キャリア目標など豊富な属性
- **柔軟なフィルタリング**: 1,500以上の職業カテゴリ、47都道府県、8地域
- **LLMシミュレーション**: ペルソナ視点での回答を自動生成
- **セグメント分析**: 年齢層・性別・職業・地域別のクロス集計
- **レポートテンプレート**: そのまま使えるMarkdownレポート雛形

## 必要なもの

- **Claude Desktop** (スキル機能が有効)
- **HuggingFaceアカウント** とアクセストークン

## インストール

### 1. HuggingFaceトークンを取得

1. [HuggingFace](https://huggingface.co/) でアカウントを作成
2. [Settings > Access Tokens](https://huggingface.co/settings/tokens) でトークンを生成
3. トークンはスキル使用時にClaudeに伝えます

### 2. Claude Desktopにスキルを追加

このリポジトリをZIP化してClaude Desktopにアップロードします。

```bash
git clone https://github.com/YOUR_USERNAME/nemotron-researcher-skill.git
cd nemotron-researcher-skill
zip -r ../nemotron-researcher-skill.zip .
```

または、[Releases](https://github.com/YOUR_USERNAME/nemotron-researcher-skill/releases)からZIPファイルをダウンロードしてください。

## ファイル構成

```
nemotron-researcher-skill/
├── SKILL.md                      # メイン: 概要・ワークフロー・使い方
├── DATASET-REFERENCE.md          # データセット: 22フィールドの詳細リファレンス
├── METHODOLOGY.md                # 手法: サンプルサイズ、質問設計、バイアス対策
├── README.md                     # このファイル
├── scripts/
│   ├── fetch_personas.py         # ペルソナ取得スクリプト
│   └── requirements.txt          # Python依存パッケージ
└── templates/
    ├── pain-point-report.md      # ペインポイント分析レポート雛形
    └── concept-test-report.md    # コンセプトテストレポート雛形
```

## 使い方

### ペルソナ抽出

Claudeに以下のように依頼します：

```
介護職のペルソナを100人抽出して
```

Claudeが条件を確認し、HuggingFaceトークンを聞いた後、スクリプトを実行してペルソナを取得します。

### ペインポイント分析

```
看護師のペインポイントを調査して
```

Claudeがターゲットセグメントと質問を確認し、ペルソナを抽出、各ペルソナの視点で回答をシミュレートし、テーマ別にクラスタリングしてレポートを生成します。

### コンセプトテスト

```
「AI搭載の料理アプリ」というコンセプトをテストして
```

Claudeがコンセプトの詳細を確認し、多様なペルソナからの反応をシミュレートし、セグメント別の受容性分析レポートを生成します。

## データセットについて

### Nemotron-Personas-Japan

| 項目 | 値 |
|------|-----|
| 提供元 | NVIDIA |
| レコード数 | 1,000,000 |
| フィールド数 | 22 |
| ライセンス | CC BY 4.0 |
| 言語 | 日本語 |

### 主なフィールド

| カテゴリ | フィールド |
|---------|-----------|
| 人口統計 | age, sex, marital_status, education_level, occupation |
| 地理 | country, region, area, prefecture |
| ペルソナ | professional_persona, sports_persona, arts_persona, travel_persona, culinary_persona, persona |
| コンテキスト | cultural_background, career_goals_and_ambitions, skills_and_expertise, hobbies_and_interests |

詳細は `DATASET-REFERENCE.md` を参照してください。

## 適切なユースケース

### 推奨される用途

- **探索的リサーチ**: 本格調査前のペインポイント発見
- **仮説生成**: 実ユーザーでテストする仮説の作成
- **コンセプトスクリーニング**: 製品アイデアの初期フィルタリング
- **セグメント探索**: 大規模なセグメント差異の理解

### 限界

- 実ユーザーリサーチの代替ではない
- シミュレート回答はLLMの学習パターンを反映
- 真に新しい・予期せぬインサイトは得られにくい
- 一次調査を補完するものとして使用

詳細は `METHODOLOGY.md` を参照してください。

## ライセンス

MIT License

## 免責事項

- このスキルは**合成データによるシミュレーション**を行います
- シミュレート回答を実ユーザーの引用として提示しないでください
- 重要なインサイトは必ず実際のユーザーリサーチで検証してください
- データセットの利用は[NVIDIA Nemotron-Personas-Japan](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Japan)のライセンス条件に従います

## 参考リンク

- [NVIDIA Nemotron-Personas-Japan (HuggingFace)](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Japan)
- [Claude Desktop](https://claude.ai/download)
- [HuggingFace Access Tokens](https://huggingface.co/settings/tokens)
