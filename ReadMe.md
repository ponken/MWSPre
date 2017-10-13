■guest_binmatch.py
ゲスト（VM）側のファイル。
トラフィックに対してパターンマッチングを行う。

・pcap_traffick_matching(filename)
　pcapファイル（filename）を読み込み、パケットのペイロード内にwindowsの実行ファイルに共通する文字列（例えば”This program cannot be run in DOS mode”）があるか確認する。

■guest_crawler.py
ゲスト（VM）側のファイル。
Googleの検索結果をクロールするためのGoogleWebCrawlerクラスがある。

・GoogleWebCrawler::search(search_words)
　検索ワード（search_words）をブラウザの検索フォームに入力し、検索を行う関数。

・GoogleWebCrawler::restore(raw_url, current_pagenum)
　ブラウザが異常終了したときのため。検索結果１ページから得られるページ番号の入っていないURL（raw_url）とページ番号（current_pagenum）を指定し、ブラウザの動作を復旧する関数。

・GoogleWebCrawler::get_links()
　Google検索結果ページから、クロール対象のURLリストを取得し、返す関数。

・GoogleWebCrawler::open_links(links=[])
　クロール対象のURLリスト（links=[]）を与え、各URLにブラウザでアクセスする関数。

・GoogleWebCrawler::goto_next_page()
　次の検索結果ページに移動する関数。

・GoogleWebCrawler::get_raw_url()
　検索結果１ページから得られるページ番号の入っていないURLを取得し、返す関数。

・GoogleWebCrawler::get_current_pagenum()
　現在開いている検索結果ページのページ番号を取得し、返す関数。

■guest_honeypot.py
ゲスト（VM）側のファイル。
クローラの管理とホストとの情報共有を行う。

・Crawler::run()
　クローラスレッド。クロールが中断されたときのために、インスタンス生成時のrestoreフラグが存在する。
　restoreフラグがTrueの場合、中断前の状態からクロールを開始する。
　restoreフラグがFalseの場合、ホスト側から渡された検索ワードを読み込み、クロールを開始する。
　また、検索結果のページ数に制限を設けることが可能。

・__main__
　初めにtsharkを起動しパケットキャプチャを開始。その後別スレッドでクローラを起動。
　ブラウザの強制終了等によりクローラが異常停止していないか監視し、停止しているようならクローラの再起動を行う。
　クロールが正常に終了した後、パケットキャプチャを停止し、パケット内に実行ファイルが現れたか確認。
　実行ファイルの存在が確認できれば、当該のpcapファイルをNASに移してゲストをシャットダウンする。

■host_vmcontroller.py
ホスト側のファイル。
ゲスト（VM）の状態を管理するスクリプト。

・__main__
　検索ワードリストのファイルが必要。スクリプト開始時にどの単語から検索を始めるか指定できるので、中断した際に続きから検索することが可能。
　ゲストとはNASを介して情報共有を行う。ホスト上にある検索ワードから１つ指定してNASに転送し、ゲストを起動してクロールを開始する。
　ゲストのクロールが終了したらスナップショットをリストアし、次の検索ワードを指定、ゲストを再起動する。

■startup.bat
ゲスト（VM）側のファイル。
Windows起動後に自動的にバッチが起動され、guest_honeypot.pyが実行される。
