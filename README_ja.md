# Simple OpenAI Speech-to-Text and Summarization

[English version](README.md)

このプロジェクトは、OpenAIのWhisperモデルを使用してオーディオファイルをテキストに変換し、OpenAIのGPT-4モデルを使用してテキストを要約する簡単な方法を提供します。

## 前提条件

*   Python 3.7+
*   OpenAI APIキー
*   OpenAI組織

## インストール

1.  リポジトリをクローンします:

    ```bash
    git clone https://github.com/masykur8d/simple_openai_speech_to_text.git
    cd simple_openai_speech_to_text
    ```
2.  仮想環境を作成します:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
    ```
3.  依存関係をインストールします:

    ```bash
    pip install -r requirements.txt
    ```

## 使い方

1.  `simple_openai_speech_to_text.py` で OpenAI 組織と API キーを設定します。
2.  オーディオファイルを `/audio_files` ディレクトリに配置します。
3.  スクリプトを実行します:

    ```bash
    python simple_openai_speech_to_text.py
    ```

    これにより、オーディオファイルがテキストに変換され、テキストが要約され、結果が `all_translation_result.xlsx` に保存されます。


## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細については `LICENSE` ファイルを参照してください。
