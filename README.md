# SimilarityChecker とは
文章の類似度をTF-idfで判別し最も近い文章のタグを返します。<br>
S3に配置された文章と対応するタグを書いたテキストファイルを元データとし、HTTPリクエストで送る文章との類似度を判別します。<br>

# 使用技術
* Python3.8
  * scikit-learn
  * Mecab 
* AWS 
  * Lambda
  * S3
  * API Gateway
* serverless Framework
* docker

# フォルダ構成
|  名前  |  内容  |
| ---- | ---- |
|  learn/Dockerfile  | SimilarityCheckerの環境  |
|  learn/learn.py  | SimilarityChecker。lambda内で動かす  |
|  line.py  |  SimilarityCheckerをLINEで利用できるように。  |
|  serverless.yml  |  AWSの構成や設定などの記述。 |
|  test.txt  |  元データのサンプル。S3に配置する。実際に運用するときはここを適切に変える |


# 制作理由など
- #### Q&Aチャットにおいてパターン化した問いを判別する事ができます。<br>
Q&Aのチャットにてパターン化した問いを判別する事が簡単です。

- #### 多くの学習データを必要としません<br>
一般的にチャットボットで利用する機械学習には多くのデータが必要とされますが文章の類似度の判別には多くの学習データを必要としません。

# 試す
LINEでの利用例です(下記QRから友達登録することで利用可能です)<br><br>
<img width="200" alt="スクリーンショット 2022-06-22 23 15 35" src="https://user-images.githubusercontent.com/84945656/175055590-d1542c96-06b9-4279-ad6c-40e3388b9165.png">

- #### 元データ<br>
mail メールが届きません<br>
mail メールが届かない<br>
pass パスワードを忘れた<br>
pass　サインインできない <br>
account アカウントを作成したい<br>
account アカウントはどこで作成できる？<br><br><br>
![IMG_6887](https://user-images.githubusercontent.com/84945656/175068004-40ee9c6d-e8cb-4373-8640-2c238956743d.jpg)


