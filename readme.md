# ouchi-gpt-llamaapi-backend

「AI チャットアプリを作って学ぶアプリ開発」のバックエンド（LLM）部分です。

## 環境準備

### 仮想環境

仮想環境で実行する場合は以下です。

```bash
python -m venv .venv
. bin/activate
```

### gguf の準備

tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf などの GGUF を同ディレクトリに格納してください。

### ライブラリ

```bash
pip install -r requirements.txt
```

## 実行

以下コマンドにてポート 8080 番で起動します。

```bash
python uvicorn main:app --host 0.0.0.0 --port 8080
```
