#!/usr/bin/env python3
"""
Nemotron-Personas-Japan データセットからペルソナを取得するスクリプト

使用例:
    python fetch_personas.py --occupation "介護職" --sample 100
    python fetch_personas.py --prefecture "東京都" --age-min 20 --age-max 35
    python fetch_personas.py --occupation "エンジニア" --output csv
"""

import argparse
import json
import sys
import os
from typing import Optional, Iterator, Dict, Any

try:
    from datasets import load_dataset
except ImportError:
    print("エラー: datasetsパッケージがインストールされていません", file=sys.stderr)
    print("インストール: pip install datasets huggingface_hub", file=sys.stderr)
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(
        description="Nemotron-Personas-Japan データセットからペルソナを取得",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 介護職のペルソナを100件取得
  python fetch_personas.py --occupation "介護職" --sample 100

  # 東京都の20-35歳を取得
  python fetch_personas.py --prefecture "東京都" --age-min 20 --age-max 35

  # CSV形式で出力
  python fetch_personas.py --occupation "看護師" --output csv

  # 特定フィールドのみ取得
  python fetch_personas.py --occupation "教師" --fields uuid,age,occupation,persona
        """
    )

    # フィルタリングオプション
    parser.add_argument("--occupation", type=str, help="職業キーワードでフィルタリング（部分一致）")
    parser.add_argument("--prefecture", type=str, help="都道府県でフィルタリング（完全一致）")
    parser.add_argument("--region", type=str, help="地域でフィルタリング（例: 関東地方）")
    parser.add_argument("--age-min", type=int, help="最小年齢")
    parser.add_argument("--age-max", type=int, help="最大年齢")
    parser.add_argument("--sex", type=str, choices=["male", "female", "男", "女"], help="性別でフィルタリング")
    parser.add_argument("--education", type=str, help="学歴キーワードでフィルタリング（部分一致）")
    parser.add_argument("--marital-status", type=str, help="婚姻状況でフィルタリング")

    # 認証オプション
    parser.add_argument("--token", type=str, help="HuggingFaceアクセストークン（必須）")

    # 出力オプション
    parser.add_argument("--sample", type=int, default=100, help="取得するサンプル数（デフォルト: 100）")
    parser.add_argument("--output", type=str, choices=["json", "csv", "markdown"], default="json", help="出力形式（デフォルト: json）")
    parser.add_argument("--fields", type=str, help="出力するフィールド（カンマ区切り）")
    parser.add_argument("--seed", type=int, default=42, help="ランダムシード（デフォルト: 42）")
    parser.add_argument("--pretty", action="store_true", help="JSONを整形して出力")

    return parser.parse_args()


def normalize_sex(sex: Optional[str]) -> Optional[str]:
    """性別の値を正規化"""
    if sex is None:
        return None
    sex_map = {"male": "男", "female": "女", "男": "男", "女": "女"}
    return sex_map.get(sex.lower(), sex)


def matches_filter(persona: Dict[str, Any], args: argparse.Namespace) -> bool:
    """ペルソナがフィルタ条件に一致するかチェック"""
    # 職業フィルタ（部分一致）
    if args.occupation and args.occupation not in persona.get("occupation", ""):
        return False

    # 都道府県フィルタ（完全一致）
    if args.prefecture and persona.get("prefecture") != args.prefecture:
        return False

    # 地域フィルタ（完全一致）
    if args.region and persona.get("region") != args.region:
        return False

    # 年齢フィルタ
    age = persona.get("age", 0)
    if args.age_min and age < args.age_min:
        return False
    if args.age_max and age > args.age_max:
        return False

    # 性別フィルタ
    if args.sex:
        normalized_sex = normalize_sex(args.sex)
        if persona.get("sex") != normalized_sex:
            return False

    # 学歴フィルタ（部分一致）
    if args.education and args.education not in persona.get("education_level", ""):
        return False

    # 婚姻状況フィルタ（部分一致）
    if args.marital_status and args.marital_status not in persona.get("marital_status", ""):
        return False

    return True


def parse_list_field(value: str) -> list:
    """JSON配列形式のフィールドをパース"""
    if not value:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


def process_persona(persona: Dict[str, Any], fields: Optional[list] = None) -> Dict[str, Any]:
    """ペルソナデータを処理"""
    result = dict(persona)

    if "hobbies_and_interests_list" in result:
        result["hobbies_and_interests_list"] = parse_list_field(result["hobbies_and_interests_list"])
    if "skills_and_expertise_list" in result:
        result["skills_and_expertise_list"] = parse_list_field(result["skills_and_expertise_list"])

    if fields:
        result = {k: v for k, v in result.items() if k in fields}

    return result


def fetch_personas(args: argparse.Namespace) -> Iterator[Dict[str, Any]]:
    """データセットからペルソナを取得"""
    # --token オプション優先、なければ環境変数
    hf_token = args.token or os.environ.get("HF_TOKEN")
    if not hf_token:
        print("エラー: HuggingFaceトークンが必要です", file=sys.stderr)
        print("--token オプションで指定するか、HF_TOKEN環境変数を設定してください", file=sys.stderr)
        sys.exit(1)

    dataset = load_dataset(
        "nvidia/Nemotron-Personas-Japan",
        split="train",
        streaming=True,
        token=hf_token
    )

    dataset = dataset.shuffle(seed=args.seed)

    fields = None
    if args.fields:
        fields = [f.strip() for f in args.fields.split(",")]

    count = 0
    for persona in dataset:
        if matches_filter(persona, args):
            yield process_persona(persona, fields)
            count += 1
            if count >= args.sample:
                break


def output_json(personas: list, pretty: bool = False):
    """JSON形式で出力"""
    if pretty:
        print(json.dumps(personas, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(personas, ensure_ascii=False))


def output_csv(personas: list):
    """CSV形式で出力"""
    if not personas:
        return

    import csv
    import io

    fieldnames = list(personas[0].keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for persona in personas:
        row = {}
        for k, v in persona.items():
            if isinstance(v, list):
                row[k] = json.dumps(v, ensure_ascii=False)
            else:
                row[k] = v
        writer.writerow(row)

    print(output.getvalue())


def output_markdown(personas: list):
    """Markdown形式で出力"""
    print(f"# ペルソナ抽出結果\n")
    print(f"**取得件数**: {len(personas)}件\n")

    if personas:
        ages = [p.get("age", 0) for p in personas if p.get("age")]
        if ages:
            print(f"**年齢**: {min(ages)}歳 〜 {max(ages)}歳（平均: {sum(ages)/len(ages):.1f}歳）\n")

        sex_dist = {}
        for p in personas:
            sex = p.get("sex", "不明")
            sex_dist[sex] = sex_dist.get(sex, 0) + 1
        print("**性別分布**:", ", ".join([f"{k}: {v}人" for k, v in sex_dist.items()]))
        print()

    print("---\n")
    for i, persona in enumerate(personas[:10], 1):
        print(f"## ペルソナ {i}")
        print(f"- **UUID**: `{persona.get('uuid', 'N/A')}`")
        print(f"- **年齢**: {persona.get('age', 'N/A')}歳")
        print(f"- **性別**: {persona.get('sex', 'N/A')}")
        print(f"- **職業**: {persona.get('occupation', 'N/A')}")
        print(f"- **都道府県**: {persona.get('prefecture', 'N/A')}")
        print(f"- **学歴**: {persona.get('education_level', 'N/A')}")
        print(f"- **婚姻状況**: {persona.get('marital_status', 'N/A')}")

        if persona.get("persona"):
            print(f"\n**統合ペルソナ**:\n> {persona['persona'][:300]}...")

        if persona.get("professional_persona"):
            print(f"\n**職業ペルソナ**:\n> {persona['professional_persona'][:200]}...")

        hobbies = persona.get("hobbies_and_interests_list", [])
        if hobbies:
            print(f"\n**趣味・興味**: {', '.join(hobbies[:5])}")

        skills = persona.get("skills_and_expertise_list", [])
        if skills:
            print(f"\n**スキル**: {', '.join(skills[:5])}")

        print("\n---\n")

    if len(personas) > 10:
        print(f"\n*（他 {len(personas) - 10} 件は省略）*")


def main():
    args = parse_args()

    print(f"データセットからペルソナを取得中... (最大 {args.sample} 件)", file=sys.stderr)
    personas = list(fetch_personas(args))
    print(f"取得完了: {len(personas)} 件", file=sys.stderr)

    if args.output == "json":
        output_json(personas, args.pretty)
    elif args.output == "csv":
        output_csv(personas)
    elif args.output == "markdown":
        output_markdown(personas)

    # HuggingFace datasets + pyarrow のスレッド終了時エラーを回避
    # データ取得は完了しているので、クリーンアップをスキップして終了
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
