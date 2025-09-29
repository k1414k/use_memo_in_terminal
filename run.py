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

    def save(self, text):
        today = str(datetime.datetime.now().strftime("%Y%m%d"))

        if today not in self.memo:
            self.memo[today] = []
        
        self.memo[today].append(text)

        self._save_log()
        print("メモを保存しました")

    def read(self):
        if not self.memo:
            print("メモが存在しません")
            return
        
        latest_date = max(int(k) for k in self.memo.keys()) #一番最新の日付取得
        for text in self.memo[str(latest_date)]:
            print(f"({latest_date}) {text}")


if __name__ == '__main__':
    mode = 'read'
    manager = MemoManager()

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode == 'save':
        new_memo = input("新しいメモ作成：  ")
        manager.save(new_memo)
    elif mode == 'read':
        manager.read()
    else: 
        print("引数が間違っています")

