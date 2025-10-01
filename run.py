import sys, json, os, datetime


class MemoManager:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.LOG_FILE = os.path.join(self.BASE_DIR, 'log.json')
        self.memo = self._load_log()

    def _load_log(self):
        """jsonからメモを読み込みなければ空辞書"""
        if not os.path.exists(self.LOG_FILE):
            return {}
        with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
            
    def _save_log(self):
        """メモをjsonに書き込む"""
        with open(self.LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.memo, f, ensure_ascii=False, indent=2)

    def write(self, text):
        today = str(datetime.datetime.now().strftime("%Y%m%d"))

        if today not in self.memo:
            self.memo[today] = []
        
        self.memo[today].append(text)

        self._save_log()
        print("メモを保存しました")

    def read(self, read_mode):
        if not self.memo:
            print("メモが存在しません")
            return
        
        if read_mode == 1:
            for k in self.memo.keys():
                print("---------------------")
                print(k)
                for idx,val in enumerate(self.memo[str(k)]):
                    print(f"({idx}) {val}")
                print("")
        else:
            latest_date = max(int(k) for k in self.memo.keys()) #一番最新の日付取得
            print(latest_date)
            for idx,val in enumerate(self.memo[str(latest_date)]):
                print(f"({idx}) {val}")
    def edit(self, date, idx, text):
        print(f"{date},{idx},{text}")

    def delete(self, date, idx):
        print(self.memo[date][int(idx)])
        

    def explanation(self):
        print("""
    -w: inputされた内容を日付で保存
    -r :最新内容確認
    -a: すべての内容確認（最新順降ろす）
    -e: inputで日付と番号と内容を指定し修正
    -d: inputで日付と番号を指定し削除
""")
        


if __name__ == '__main__':
    manager = MemoManager()

    if len(sys.argv) > 1:
        argument = sys.argv[1].lower()
    else:
        argument = ""

    if argument == '-w':
        new_memo = input("新しいメモ作成: ")
        manager.write(new_memo)
    elif argument == '-r':
        manager.read(0)
    elif argument == '-a':
        manager.read(1)
    elif argument == '-e':
        date = input("修正する日付: ")
        idx = input("インデックス番号: ")
        new_memo = input("新しいメモ作成: ")
        manager.edit(date, idx, new_memo)
    elif argument == '-d':
        date = input("削除する日付: ")
        idx = input("インデックス番号: ")
        manager.delete(date, idx)
    else: 
        manager.explanation()