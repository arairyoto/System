# Model for Research

## Description
下記のプログラムが含まれています．

- ReverseAutoExtend(RAE)による多言語概念空間構築に必要な元データの構築プログラム（5章）
- 多言語概念空間妥当性検証プログラム（5章）
- コーパスからWSDをして語彙素の頻度をカウントするプログラム（6章）
- 多言語概念空間を用いた実験プログラム（6,7章）

exWordNetに使用するデータは下記からダウンロードしてください．

datafile：https://www.dropbox.com/sh/ckylez7t5x3ecm5/AAA7yizJ5CA3mF8nE5Teo2ARa?dl=0

datafileのfolderのパスをexWordNetの定義の時に指定してください．


### RAEの構築

1. 元となる分散表現の準備(txtデータ)

2. 元となる分散表現のデータから，AutoExtend学習時に必要なデータの構築

3. AutoExtendによる学習(AutoExtendの元のプログラムを用いてMatlab上で学習)

4. AutoExtendによって学習されたSynsetの分散表現を準備

5. Synsetの分散表現のデータから，AutoExtend学習時に必要なデータの構築

6. AutoExtendによる学習(AutoExtendの元のプログラムを用いてMatlab上で学習)

7. 分散表現を獲得したい言語に対して5,6を繰り返す

### 多言語概念空間の検証
-> config.pyのCorpusFolderに指定してあるフォルダにRAEで構築した多言語概念空間データを保存

-> Validationフォルダ

### 語彙素の頻度情報の獲得

-> WSDフォルダ

### 構築したデータの保存

-> config.pyのCorpusFolderに指定してあるフォルダにRAEで構築した多言語概念空間データや語彙素の頻度情報を保存

### 多言語概念空間を用いたデザインプロセス応用

-> Experimentフォルダ
